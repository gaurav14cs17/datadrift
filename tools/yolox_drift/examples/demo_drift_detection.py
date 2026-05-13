"""
Demo: YOLOX Nano Data Drift Detection

This script demonstrates how to use the drift detection tools
programmatically (without the CLI).

Usage:
    python demo_drift_detection.py --ref-dir /path/to/reference --prod-dir /path/to/production
"""

import argparse
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from yolox_drift.detectors.image_drift import ImageDriftDetector
from yolox_drift.detectors.prediction_drift import PredictionDriftDetector
from yolox_drift.detectors.statistical_tests import ks_test, psi_test, mmd_test
from yolox_drift.reports.drift_report import DriftReportGenerator
from yolox_drift.config import COCO_CLASSES


def demo_image_drift(ref_dir: str, prod_dir: str):
    """Demonstrate image-level drift detection."""
    print("\n" + "=" * 60)
    print("  DEMO 1: Image-Level Drift Detection")
    print("=" * 60)

    detector = ImageDriftDetector(input_size=(416, 416))
    results = detector.detect(ref_dir, prod_dir, max_images=100)

    print(f"\n  Overall Status: {results['summary']['overall_status']}")
    print(f"  Drifted Tests: {results['summary']['drifted_tests']}/{results['summary']['total_tests']}")

    print("\n  Pixel Drift Results:")
    for name, result in results["pixel_drift"].items():
        icon = "X" if result.is_drift else "✓"
        print(f"    [{icon}] {result.test_name}: stat={result.statistic:.4f}, p={result.p_value:.4f}")

    print("\n  Embedding Drift Results:")
    for name, result in results["embedding_drift"].items():
        icon = "X" if result.is_drift else "✓"
        print(f"    [{icon}] {result.test_name}: stat={result.statistic:.4f}, p={result.p_value:.4f}")

    return results


def demo_prediction_drift():
    """Demonstrate prediction-level drift with synthetic data."""
    print("\n" + "=" * 60)
    print("  DEMO 2: Prediction-Level Drift (Synthetic)")
    print("=" * 60)

    rng = np.random.default_rng(42)

    # Simulate reference predictions (normal operation)
    ref_predictions = []
    for _ in range(200):
        n_det = rng.poisson(5)
        boxes = rng.uniform(0, 416, size=(n_det, 4))
        boxes[:, 2:] = boxes[:, :2] + rng.uniform(20, 100, size=(n_det, 2))
        scores = rng.beta(5, 2, size=n_det)
        # Normal class distribution: mostly person, car, dog
        classes = rng.choice([0, 2, 16], size=n_det, p=[0.5, 0.3, 0.2])
        ref_predictions.append({
            "boxes": boxes,
            "scores": scores,
            "classes": classes,
            "image_size": (416, 416),
        })

    # Simulate production predictions (drifted)
    prod_predictions = []
    for _ in range(200):
        n_det = rng.poisson(8)  # More detections
        boxes = rng.uniform(0, 416, size=(n_det, 4))
        boxes[:, 2:] = boxes[:, :2] + rng.uniform(10, 60, size=(n_det, 2))  # Smaller boxes
        scores = rng.beta(3, 3, size=n_det)  # Lower confidence
        # Shifted class distribution: more trucks and buses
        classes = rng.choice([0, 2, 5, 7, 16], size=n_det, p=[0.3, 0.2, 0.2, 0.2, 0.1])
        prod_predictions.append({
            "boxes": boxes,
            "scores": scores,
            "classes": classes,
            "image_size": (416, 416),
        })

    detector = PredictionDriftDetector(num_classes=80, class_names=COCO_CLASSES)
    results = detector.detect(ref_predictions, prod_predictions)

    print(f"\n  Overall Status: {results['summary']['overall_status']}")
    print(f"  Drifted Tests: {results['summary']['drifted_tests']}/{results['summary']['total_tests']}")

    # Class distribution
    class_data = results["class_distribution"]
    print(f"\n  Class Drift: {'DRIFT' if class_data['chi_square'].is_drift else 'OK'}")
    print(f"  Unique classes: ref={class_data['ref_unique_classes']} → prod={class_data['prod_unique_classes']}")

    # Confidence
    conf = results["confidence_drift"]
    print(f"\n  Confidence: ref={conf['ref_mean_confidence']:.3f} → prod={conf['prod_mean_confidence']:.3f}")
    print(f"  Change: {conf['confidence_change']:+.3f}")

    # Detection count
    count = results["detection_count_drift"]
    print(f"\n  Detections/image: ref={count['ref_mean_count']:.1f} → prod={count['prod_mean_count']:.1f}")
    print(f"  Change: {count['count_change_pct']:+.1f}%")

    return results


def demo_statistical_tests():
    """Demonstrate individual statistical tests."""
    print("\n" + "=" * 60)
    print("  DEMO 3: Individual Statistical Tests")
    print("=" * 60)

    rng = np.random.default_rng(123)

    # No drift (same distribution)
    ref = rng.normal(0, 1, size=(200, 10))
    prod_same = rng.normal(0, 1, size=(200, 10))

    print("\n  Test: Same distribution (expect NO drift)")
    result = ks_test(ref, prod_same)
    print(f"    KS Test: {result}")
    result = psi_test(ref, prod_same)
    print(f"    PSI Test: {result}")

    # With drift (shifted distribution)
    prod_shifted = rng.normal(0.5, 1.5, size=(200, 10))

    print("\n  Test: Shifted distribution (expect DRIFT)")
    result = ks_test(ref, prod_shifted)
    print(f"    KS Test: {result}")
    result = psi_test(ref, prod_shifted)
    print(f"    PSI Test: {result}")
    result = mmd_test(ref, prod_shifted, n_permutations=200)
    print(f"    MMD Test: {result}")


def demo_full_report(ref_dir: str, prod_dir: str):
    """Generate a full HTML-style report."""
    print("\n" + "=" * 60)
    print("  DEMO 4: Full Report Generation")
    print("=" * 60)

    image_detector = ImageDriftDetector(input_size=(416, 416))
    image_results = image_detector.detect(ref_dir, prod_dir, max_images=50)

    reporter = DriftReportGenerator(output_dir="demo_reports")
    reporter.generate(image_results=image_results)

    print("\n  Report generated in: demo_reports/")


def main():
    parser = argparse.ArgumentParser(description="YOLOX Nano Drift Detection Demo")
    parser.add_argument("--ref-dir", default=None, help="Reference images directory")
    parser.add_argument("--prod-dir", default=None, help="Production images directory")
    args = parser.parse_args()

    print("""
╔════════════════════════════════════════════════════════════════╗
║       YOLOX Nano Data Drift Detection — Demo Suite            ║
╚════════════════════════════════════════════════════════════════╝
    """)

    # Always run synthetic demos
    demo_statistical_tests()
    demo_prediction_drift()

    # Run image demos only if directories provided
    if args.ref_dir and args.prod_dir:
        demo_image_drift(args.ref_dir, args.prod_dir)
        demo_full_report(args.ref_dir, args.prod_dir)
    else:
        print("\n  [Note] Skipping image demos: provide --ref-dir and --prod-dir")
        print("  Example: python demo_drift_detection.py --ref-dir data/ref --prod-dir data/prod")

    print("\n" + "=" * 60)
    print("  All demos completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
