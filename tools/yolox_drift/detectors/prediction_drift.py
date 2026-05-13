"""
Prediction-level drift detection for YOLOX Nano.
Detects changes in:
  - Class distribution (which objects are detected)
  - Bounding box statistics (size, position, aspect ratio)
  - Confidence score distribution
  - Number of detections per image
"""

from typing import Dict, List, Optional

import numpy as np
from scipy import stats

from .statistical_tests import (
    DriftTestResult,
    ks_test,
    psi_test,
    chi_square_test,
    wasserstein_test,
    js_divergence_test,
)


class PredictionDriftDetector:
    """
    Detects drift in YOLOX Nano model outputs.
    Takes pre-computed predictions (bounding boxes, classes, confidences)
    for reference and production datasets.
    """

    def __init__(self, num_classes: int = 80, class_names: Optional[List[str]] = None):
        self.num_classes = num_classes
        self.class_names = class_names

    def detect(
        self,
        ref_predictions: List[dict],
        prod_predictions: List[dict],
        alpha: float = 0.05,
    ) -> Dict[str, object]:
        """
        Run full prediction-level drift detection.

        Each prediction dict should have:
          - "boxes": np.ndarray of shape (N, 4) in [x1, y1, x2, y2] format
          - "scores": np.ndarray of shape (N,)
          - "classes": np.ndarray of shape (N,) with integer class IDs
          - "image_size": (height, width)
        """
        results = {}
        results["class_distribution"] = self._detect_class_drift(
            ref_predictions, prod_predictions, alpha
        )
        results["confidence_drift"] = self._detect_confidence_drift(
            ref_predictions, prod_predictions, alpha
        )
        results["bbox_drift"] = self._detect_bbox_drift(
            ref_predictions, prod_predictions, alpha
        )
        results["detection_count_drift"] = self._detect_count_drift(
            ref_predictions, prod_predictions, alpha
        )
        results["summary"] = self._summarize(results)
        return results

    def _detect_class_drift(
        self,
        ref_preds: List[dict],
        prod_preds: List[dict],
        alpha: float,
    ) -> Dict[str, object]:
        """Detect drift in class distribution."""
        ref_classes = np.concatenate([p["classes"] for p in ref_preds if len(p["classes"]) > 0])
        prod_classes = np.concatenate([p["classes"] for p in prod_preds if len(p["classes"]) > 0])

        ref_hist = np.bincount(ref_classes.astype(int), minlength=self.num_classes).astype(float)
        prod_hist = np.bincount(prod_classes.astype(int), minlength=self.num_classes).astype(float)

        ref_dist = ref_hist / (ref_hist.sum() + 1e-10)
        prod_dist = prod_hist / (prod_hist.sum() + 1e-10)

        # Chi-square on class distributions
        ref_norm = ref_hist + 1e-8
        prod_norm = prod_hist + 1e-8
        ref_norm = ref_norm / ref_norm.sum()
        prod_norm = prod_norm / prod_norm.sum()
        chi2_stat, chi2_p = stats.chisquare(prod_norm, f_exp=ref_norm)

        # Per-class changes
        per_class = {}
        for i in range(self.num_classes):
            if ref_dist[i] > 0.001 or prod_dist[i] > 0.001:
                name = self.class_names[i] if self.class_names and i < len(self.class_names) else f"class_{i}"
                per_class[name] = {
                    "ref_pct": round(float(ref_dist[i]) * 100, 2),
                    "prod_pct": round(float(prod_dist[i]) * 100, 2),
                    "change": round(float(prod_dist[i] - ref_dist[i]) * 100, 2),
                }

        # Top disappearing and emerging classes
        diff = prod_dist - ref_dist
        top_emerging = np.argsort(diff)[-5:][::-1]
        top_disappearing = np.argsort(diff)[:5]

        return {
            "chi_square": DriftTestResult(
                test_name="Class Distribution Chi-Square",
                statistic=float(chi2_stat),
                p_value=float(chi2_p),
                is_drift=chi2_p < alpha,
                severity="critical" if chi2_p < 0.01 else ("warning" if chi2_p < alpha else "none"),
            ),
            "per_class": per_class,
            "top_emerging": [int(i) for i in top_emerging],
            "top_disappearing": [int(i) for i in top_disappearing],
            "ref_unique_classes": int(np.sum(ref_hist > 0)),
            "prod_unique_classes": int(np.sum(prod_hist > 0)),
        }

    def _detect_confidence_drift(
        self,
        ref_preds: List[dict],
        prod_preds: List[dict],
        alpha: float,
    ) -> Dict[str, DriftTestResult]:
        """Detect drift in confidence score distributions."""
        ref_scores = np.concatenate([p["scores"] for p in ref_preds if len(p["scores"]) > 0])
        prod_scores = np.concatenate([p["scores"] for p in prod_preds if len(p["scores"]) > 0])

        return {
            "ks_test": ks_test(ref_scores, prod_scores, alpha),
            "psi_test": psi_test(ref_scores, prod_scores),
            "wasserstein": wasserstein_test(ref_scores, prod_scores, threshold=0.05),
            "ref_mean_confidence": float(np.mean(ref_scores)),
            "prod_mean_confidence": float(np.mean(prod_scores)),
            "confidence_change": float(np.mean(prod_scores) - np.mean(ref_scores)),
        }

    def _detect_bbox_drift(
        self,
        ref_preds: List[dict],
        prod_preds: List[dict],
        alpha: float,
    ) -> Dict[str, DriftTestResult]:
        """Detect drift in bounding box characteristics."""
        ref_features = self._extract_bbox_features(ref_preds)
        prod_features = self._extract_bbox_features(prod_preds)

        results = {}
        feature_names = ["width", "height", "area", "aspect_ratio", "center_x", "center_y"]

        for i, name in enumerate(feature_names):
            if i < ref_features.shape[1] and i < prod_features.shape[1]:
                results[f"{name}_ks"] = ks_test(
                    ref_features[:, i], prod_features[:, i], alpha
                )
                results[f"{name}_psi"] = psi_test(
                    ref_features[:, i], prod_features[:, i]
                )

        return results

    def _detect_count_drift(
        self,
        ref_preds: List[dict],
        prod_preds: List[dict],
        alpha: float,
    ) -> Dict[str, object]:
        """Detect drift in number of detections per image."""
        ref_counts = np.array([len(p["classes"]) for p in ref_preds], dtype=float)
        prod_counts = np.array([len(p["classes"]) for p in prod_preds], dtype=float)

        return {
            "ks_test": ks_test(ref_counts, prod_counts, alpha),
            "ref_mean_count": float(np.mean(ref_counts)),
            "prod_mean_count": float(np.mean(prod_counts)),
            "ref_std_count": float(np.std(ref_counts)),
            "prod_std_count": float(np.std(prod_counts)),
            "count_change_pct": float(
                (np.mean(prod_counts) - np.mean(ref_counts))
                / (np.mean(ref_counts) + 1e-8) * 100
            ),
        }

    def _extract_bbox_features(self, predictions: List[dict]) -> np.ndarray:
        """Extract normalized bounding box features from predictions."""
        features = []
        for pred in predictions:
            boxes = pred["boxes"]
            img_h, img_w = pred.get("image_size", (416, 416))
            for box in boxes:
                x1, y1, x2, y2 = box
                w = (x2 - x1) / img_w
                h = (y2 - y1) / img_h
                area = w * h
                aspect = w / (h + 1e-8)
                cx = ((x1 + x2) / 2) / img_w
                cy = ((y1 + y2) / 2) / img_h
                features.append([w, h, area, aspect, cx, cy])

        if not features:
            return np.zeros((1, 6))
        return np.array(features, dtype=np.float32)

    def _summarize(self, results: dict) -> dict:
        all_tests = []
        for section in results.values():
            if isinstance(section, dict):
                for v in section.values():
                    if isinstance(v, DriftTestResult):
                        all_tests.append(v)

        n_total = len(all_tests)
        n_drift = sum(1 for t in all_tests if t.is_drift)
        n_critical = sum(1 for t in all_tests if t.severity == "critical")

        if n_critical > 0:
            overall = "CRITICAL"
        elif n_drift > n_total * 0.3:
            overall = "WARNING"
        elif n_drift > 0:
            overall = "MINOR_DRIFT"
        else:
            overall = "HEALTHY"

        return {
            "overall_status": overall,
            "total_tests": n_total,
            "drifted_tests": n_drift,
            "critical_count": n_critical,
        }
