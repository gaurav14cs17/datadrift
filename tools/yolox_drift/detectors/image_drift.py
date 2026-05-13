"""
Image-level drift detection for YOLOX Nano.
Detects changes in pixel distributions, color statistics, brightness,
contrast, and embedding space.
"""

from typing import Dict, List

import numpy as np

from ..utils.image_loader import compute_image_statistics, load_image_batch, list_images
from ..utils.feature_extractor import YOLOXFeatureExtractor
from .statistical_tests import (
    DriftTestResult,
    ks_test,
    psi_test,
    wasserstein_test,
    js_divergence_test,
    mmd_test,
)


class ImageDriftDetector:
    """
    Detects data drift at the image level for a YOLOX Nano pipeline.

    Three detection strategies:
      1. Pixel-level: per-channel histograms and statistics
      2. Feature-level: handcrafted or backbone embeddings
      3. Embedding-level: MMD on deep feature representations
    """

    def __init__(
        self,
        model_path: str = None,
        input_size: tuple = (416, 416),
        device: str = "cpu",
    ):
        self.extractor = YOLOXFeatureExtractor(
            model_path=model_path,
            input_size=input_size,
            device=device,
        )
        self.input_size = input_size

    def detect(
        self,
        reference_dir: str,
        production_dir: str,
        alpha: float = 0.05,
        max_images: int = 500,
    ) -> Dict[str, object]:
        """Run full image-level drift detection suite."""
        ref_paths = list_images(reference_dir)[:max_images]
        prod_paths = list_images(production_dir)[:max_images]

        if len(ref_paths) < 10 or len(prod_paths) < 10:
            raise ValueError(
                f"Need at least 10 images per set. "
                f"Found {len(ref_paths)} ref, {len(prod_paths)} prod."
            )

        ref_images = load_image_batch(ref_paths, target_size=self.input_size)
        prod_images = load_image_batch(prod_paths, target_size=self.input_size)

        results = {}
        results["pixel_drift"] = self._detect_pixel_drift(ref_images, prod_images, alpha)
        results["statistics_drift"] = self._detect_statistics_drift(ref_images, prod_images)
        results["embedding_drift"] = self._detect_embedding_drift(ref_images, prod_images, alpha)
        results["summary"] = self._summarize(results)

        return results

    def _detect_pixel_drift(
        self,
        ref_images: np.ndarray,
        prod_images: np.ndarray,
        alpha: float,
    ) -> Dict[str, DriftTestResult]:
        """Per-channel pixel value drift."""
        results = {}
        channel_names = ["red", "green", "blue"]
        for c, name in enumerate(channel_names):
            ref_flat = ref_images[..., c].reshape(len(ref_images), -1).mean(axis=1)
            prod_flat = prod_images[..., c].reshape(len(prod_images), -1).mean(axis=1)
            results[f"{name}_ks"] = ks_test(ref_flat, prod_flat, alpha)
            results[f"{name}_psi"] = psi_test(ref_flat, prod_flat)

        ref_bright = np.mean(ref_images.astype(np.float32), axis=-1).reshape(len(ref_images), -1).mean(axis=1)
        prod_bright = np.mean(prod_images.astype(np.float32), axis=-1).reshape(len(prod_images), -1).mean(axis=1)
        results["brightness_ks"] = ks_test(ref_bright, prod_bright, alpha)
        results["brightness_wasserstein"] = wasserstein_test(ref_bright, prod_bright, threshold=5.0)

        return results

    def _detect_statistics_drift(
        self,
        ref_images: np.ndarray,
        prod_images: np.ndarray,
    ) -> Dict[str, object]:
        """Compare aggregate image statistics."""
        ref_stats = compute_image_statistics(ref_images)
        prod_stats = compute_image_statistics(prod_images)

        comparison = {}
        for key in ref_stats:
            ref_val = ref_stats[key]
            prod_val = prod_stats[key]
            diff = prod_val - ref_val
            pct_change = abs(diff) / (abs(ref_val) + 1e-8) * 100
            comparison[key] = {
                "reference": round(ref_val, 4),
                "production": round(prod_val, 4),
                "difference": round(diff, 4),
                "pct_change": round(pct_change, 2),
                "alert": pct_change > 10,
            }
        return comparison

    def _detect_embedding_drift(
        self,
        ref_images: np.ndarray,
        prod_images: np.ndarray,
        alpha: float,
    ) -> Dict[str, DriftTestResult]:
        """Embedding-space drift via feature extractor."""
        ref_feats = self.extractor.extract(ref_images)
        prod_feats = self.extractor.extract(prod_images)

        results = {}
        results["embedding_mmd"] = mmd_test(ref_feats, prod_feats, n_permutations=500, alpha=alpha)
        results["embedding_ks"] = ks_test(ref_feats, prod_feats, alpha)
        results["embedding_js"] = js_divergence_test(ref_feats, prod_feats)
        return results

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
        n_warning = sum(1 for t in all_tests if t.severity == "warning")

        if n_critical > 0:
            overall = "CRITICAL"
        elif n_warning > 0:
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
            "warning_count": n_warning,
            "drift_ratio": round(n_drift / max(n_total, 1), 3),
        }
