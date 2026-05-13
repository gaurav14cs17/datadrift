"""
Statistical drift detection tests for YOLOX Nano.
Implements KS, PSI, Chi-Square, MMD, Wasserstein, and JS Divergence.
"""

from typing import Dict, Tuple

import numpy as np
from scipy import stats


class DriftTestResult:
    """Container for a single drift test result."""

    def __init__(
        self,
        test_name: str,
        statistic: float,
        p_value: float,
        is_drift: bool,
        severity: str = "none",
        details: dict = None,
    ):
        self.test_name = test_name
        self.statistic = statistic
        self.p_value = p_value
        self.is_drift = is_drift
        self.severity = severity
        self.details = details or {}

    def __repr__(self):
        icon = "DRIFT" if self.is_drift else "OK"
        return (
            f"[{icon}] {self.test_name}: "
            f"stat={self.statistic:.4f}, p={self.p_value:.4f}, "
            f"severity={self.severity}"
        )


def ks_test(reference: np.ndarray, production: np.ndarray, alpha: float = 0.05) -> DriftTestResult:
    """Kolmogorov-Smirnov two-sample test per feature, returns worst-case."""
    if reference.ndim == 1:
        reference = reference.reshape(-1, 1)
        production = production.reshape(-1, 1)

    worst_stat, worst_p = 0.0, 1.0
    per_feature = {}

    for i in range(reference.shape[1]):
        stat, p_val = stats.ks_2samp(reference[:, i], production[:, i])
        per_feature[f"feature_{i}"] = {"statistic": stat, "p_value": p_val}
        if stat > worst_stat:
            worst_stat = stat
            worst_p = p_val

    n_drifted = sum(1 for v in per_feature.values() if v["p_value"] < alpha)
    drift_ratio = n_drifted / len(per_feature)

    is_drift = drift_ratio > 0.1
    severity = _severity_from_ratio(drift_ratio)

    return DriftTestResult(
        test_name="Kolmogorov-Smirnov",
        statistic=worst_stat,
        p_value=worst_p,
        is_drift=is_drift,
        severity=severity,
        details={
            "drifted_features": n_drifted,
            "total_features": len(per_feature),
            "drift_ratio": drift_ratio,
        },
    )


def psi_test(
    reference: np.ndarray,
    production: np.ndarray,
    bins: int = 10,
    warn_threshold: float = 0.1,
    critical_threshold: float = 0.25,
) -> DriftTestResult:
    """Population Stability Index (PSI) test."""
    if reference.ndim == 1:
        reference = reference.reshape(-1, 1)
        production = production.reshape(-1, 1)

    psi_values = []
    for i in range(reference.shape[1]):
        psi_val = _compute_psi(reference[:, i], production[:, i], bins)
        psi_values.append(psi_val)

    mean_psi = float(np.mean(psi_values))
    max_psi = float(np.max(psi_values))

    if max_psi >= critical_threshold:
        severity = "critical"
    elif max_psi >= warn_threshold:
        severity = "warning"
    else:
        severity = "none"

    return DriftTestResult(
        test_name="Population Stability Index (PSI)",
        statistic=mean_psi,
        p_value=1.0 - min(mean_psi / critical_threshold, 1.0),
        is_drift=max_psi >= warn_threshold,
        severity=severity,
        details={
            "mean_psi": mean_psi,
            "max_psi": max_psi,
            "per_feature_psi": psi_values,
        },
    )


def chi_square_test(
    reference: np.ndarray,
    production: np.ndarray,
    bins: int = 10,
    alpha: float = 0.05,
) -> DriftTestResult:
    """Chi-Square test for categorical / binned distributions."""
    if reference.ndim == 1:
        reference = reference.reshape(-1, 1)
        production = production.reshape(-1, 1)

    worst_stat, worst_p = 0.0, 1.0
    n_drifted = 0

    for i in range(reference.shape[1]):
        combined = np.concatenate([reference[:, i], production[:, i]])
        bin_edges = np.histogram_bin_edges(combined, bins=bins)
        ref_hist, _ = np.histogram(reference[:, i], bins=bin_edges)
        prod_hist, _ = np.histogram(production[:, i], bins=bin_edges)

        ref_hist = ref_hist.astype(np.float64) + 1e-8
        prod_hist = prod_hist.astype(np.float64) + 1e-8

        ref_hist = ref_hist / ref_hist.sum()
        prod_hist = prod_hist / prod_hist.sum()

        stat, p_val = stats.chisquare(prod_hist, f_exp=ref_hist)
        if stat > worst_stat:
            worst_stat = stat
            worst_p = p_val
        if p_val < alpha:
            n_drifted += 1

    drift_ratio = n_drifted / reference.shape[1]
    return DriftTestResult(
        test_name="Chi-Square",
        statistic=worst_stat,
        p_value=worst_p,
        is_drift=drift_ratio > 0.1,
        severity=_severity_from_ratio(drift_ratio),
        details={"drifted_features": n_drifted, "drift_ratio": drift_ratio},
    )


def mmd_test(
    reference: np.ndarray,
    production: np.ndarray,
    n_permutations: int = 1000,
    alpha: float = 0.05,
) -> DriftTestResult:
    """Maximum Mean Discrepancy (MMD) test with RBF kernel."""
    mmd_obs = _compute_mmd(reference, production)

    combined = np.vstack([reference, production])
    n_ref = len(reference)
    count_greater = 0

    rng = np.random.default_rng(42)
    for _ in range(n_permutations):
        perm = rng.permutation(len(combined))
        perm_ref = combined[perm[:n_ref]]
        perm_prod = combined[perm[n_ref:]]
        mmd_perm = _compute_mmd(perm_ref, perm_prod)
        if mmd_perm >= mmd_obs:
            count_greater += 1

    p_value = (count_greater + 1) / (n_permutations + 1)

    return DriftTestResult(
        test_name="Maximum Mean Discrepancy (MMD)",
        statistic=mmd_obs,
        p_value=p_value,
        is_drift=p_value < alpha,
        severity="critical" if p_value < 0.01 else ("warning" if p_value < alpha else "none"),
        details={"n_permutations": n_permutations},
    )


def wasserstein_test(
    reference: np.ndarray,
    production: np.ndarray,
    threshold: float = 0.1,
) -> DriftTestResult:
    """Wasserstein (Earth Mover's) distance per feature."""
    if reference.ndim == 1:
        reference = reference.reshape(-1, 1)
        production = production.reshape(-1, 1)

    distances = []
    for i in range(reference.shape[1]):
        d = stats.wasserstein_distance(reference[:, i], production[:, i])
        distances.append(d)

    mean_dist = float(np.mean(distances))
    max_dist = float(np.max(distances))

    return DriftTestResult(
        test_name="Wasserstein Distance",
        statistic=mean_dist,
        p_value=max(0.0, 1.0 - mean_dist / (threshold + 1e-8)),
        is_drift=mean_dist > threshold,
        severity="critical" if mean_dist > threshold * 2 else (
            "warning" if mean_dist > threshold else "none"
        ),
        details={"mean_distance": mean_dist, "max_distance": max_dist},
    )


def js_divergence_test(
    reference: np.ndarray,
    production: np.ndarray,
    bins: int = 50,
    threshold: float = 0.1,
) -> DriftTestResult:
    """Jensen-Shannon divergence per feature."""
    if reference.ndim == 1:
        reference = reference.reshape(-1, 1)
        production = production.reshape(-1, 1)

    js_values = []
    for i in range(reference.shape[1]):
        combined = np.concatenate([reference[:, i], production[:, i]])
        bin_edges = np.histogram_bin_edges(combined, bins=bins)
        ref_hist, _ = np.histogram(reference[:, i], bins=bin_edges, density=True)
        prod_hist, _ = np.histogram(production[:, i], bins=bin_edges, density=True)

        ref_hist = ref_hist + 1e-10
        prod_hist = prod_hist + 1e-10
        ref_hist = ref_hist / ref_hist.sum()
        prod_hist = prod_hist / prod_hist.sum()

        m = 0.5 * (ref_hist + prod_hist)
        js = 0.5 * stats.entropy(ref_hist, m) + 0.5 * stats.entropy(prod_hist, m)
        js_values.append(js)

    mean_js = float(np.mean(js_values))

    return DriftTestResult(
        test_name="Jensen-Shannon Divergence",
        statistic=mean_js,
        p_value=max(0.0, 1.0 - mean_js / (threshold + 1e-8)),
        is_drift=mean_js > threshold,
        severity="critical" if mean_js > threshold * 2 else (
            "warning" if mean_js > threshold else "none"
        ),
        details={"mean_js": mean_js, "per_feature_js": js_values},
    )


# ── Helpers ──────────────────────────────────────────────────────────────────

def _compute_psi(reference: np.ndarray, production: np.ndarray, bins: int = 10) -> float:
    combined = np.concatenate([reference, production])
    bin_edges = np.histogram_bin_edges(combined, bins=bins)
    ref_hist, _ = np.histogram(reference, bins=bin_edges)
    prod_hist, _ = np.histogram(production, bins=bin_edges)

    ref_pct = (ref_hist + 1) / (ref_hist.sum() + bins)
    prod_pct = (prod_hist + 1) / (prod_hist.sum() + bins)

    psi = np.sum((prod_pct - ref_pct) * np.log(prod_pct / ref_pct))
    return float(psi)


def _compute_mmd(x: np.ndarray, y: np.ndarray) -> float:
    """MMD^2 with RBF kernel using median heuristic for bandwidth."""
    combined = np.vstack([x, y])
    dists = np.sum((combined[:, None] - combined[None, :]) ** 2, axis=-1)
    sigma = np.median(dists[dists > 0])
    if sigma < 1e-10:
        sigma = 1.0

    gamma = 1.0 / (2.0 * sigma)
    kxx = np.exp(-gamma * np.sum((x[:, None] - x[None, :]) ** 2, axis=-1))
    kyy = np.exp(-gamma * np.sum((y[:, None] - y[None, :]) ** 2, axis=-1))
    kxy = np.exp(-gamma * np.sum((x[:, None] - y[None, :]) ** 2, axis=-1))

    mmd = kxx.mean() + kyy.mean() - 2 * kxy.mean()
    return float(max(mmd, 0.0))


def _severity_from_ratio(ratio: float) -> str:
    if ratio > 0.5:
        return "critical"
    elif ratio > 0.1:
        return "warning"
    return "none"
