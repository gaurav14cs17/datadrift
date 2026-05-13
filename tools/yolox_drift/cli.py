"""
CLI entry point for YOLOX Nano Data Drift Detection Tool.

Usage:
    python -m yolox_drift.cli --ref-dir data/reference --prod-dir data/production
    python -m yolox_drift.cli --ref-dir data/ref --prod-dir data/prod --model yolox_nano.onnx
"""

import argparse
import sys
import time
from pathlib import Path

from .config import MonitorConfig, COCO_CLASSES
from .detectors.image_drift import ImageDriftDetector
from .detectors.prediction_drift import PredictionDriftDetector
from .reports.drift_report import DriftReportGenerator
from .utils.image_loader import list_images, load_image_batch


def parse_args():
    parser = argparse.ArgumentParser(
        description="YOLOX Nano Data Drift Detection Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic image-level drift detection
  python -m yolox_drift.cli --ref-dir data/reference --prod-dir data/production

  # With YOLOX Nano model for embedding + prediction drift
  python -m yolox_drift.cli --ref-dir data/ref --prod-dir data/prod --model yolox_nano.onnx

  # Custom thresholds and output
  python -m yolox_drift.cli --ref-dir data/ref --prod-dir data/prod \\
      --alpha 0.01 --psi-threshold 0.2 --output reports/
        """,
    )

    parser.add_argument("--ref-dir", required=True, help="Reference (training) images directory")
    parser.add_argument("--prod-dir", required=True, help="Production images directory")
    parser.add_argument("--model", default=None, help="YOLOX Nano model path (.onnx or .pth)")
    parser.add_argument("--output", default="drift_reports", help="Output directory for reports")
    parser.add_argument("--alpha", type=float, default=0.05, help="Significance level (default: 0.05)")
    parser.add_argument("--psi-threshold", type=float, default=0.1, help="PSI warning threshold")
    parser.add_argument("--max-images", type=int, default=500, help="Max images to sample per set")
    parser.add_argument("--input-size", type=int, default=416, help="YOLOX input size (default: 416)")
    parser.add_argument("--device", default="cpu", choices=["cpu", "cuda"], help="Compute device")
    parser.add_argument("--no-plots", action="store_true", help="Skip generating plot images")

    return parser.parse_args()


def main():
    args = parse_args()

    print_banner()

    ref_dir = Path(args.ref_dir)
    prod_dir = Path(args.prod_dir)
    if not ref_dir.exists():
        print(f"Error: Reference directory not found: {ref_dir}")
        sys.exit(1)
    if not prod_dir.exists():
        print(f"Error: Production directory not found: {prod_dir}")
        sys.exit(1)

    ref_images_list = list_images(str(ref_dir))
    prod_images_list = list_images(str(prod_dir))
    print(f"  Reference images: {len(ref_images_list)}")
    print(f"  Production images: {len(prod_images_list)}")
    print()

    if len(ref_images_list) < 10 or len(prod_images_list) < 10:
        print("Error: Need at least 10 images in each directory.")
        sys.exit(1)

    # Image-level drift
    start = time.time()
    input_size = (args.input_size, args.input_size)

    image_detector = ImageDriftDetector(
        model_path=args.model,
        input_size=input_size,
        device=args.device,
    )

    image_results = image_detector.detect(
        reference_dir=str(ref_dir),
        production_dir=str(prod_dir),
        alpha=args.alpha,
        max_images=args.max_images,
    )

    elapsed = time.time() - start
    print(f"  Image drift analysis completed in {elapsed:.1f}s")

    # Load images for plots
    ref_images = load_image_batch(
        [str(p) for p in ref_images_list[:args.max_images]],
        target_size=input_size,
        show_progress=False,
    )
    prod_images = load_image_batch(
        [str(p) for p in prod_images_list[:args.max_images]],
        target_size=input_size,
        show_progress=False,
    )

    # Report
    reporter = DriftReportGenerator(output_dir=args.output)
    reporter.generate(
        image_results=image_results,
        prediction_results=None,
        ref_images=ref_images if not args.no_plots else None,
        prod_images=prod_images if not args.no_plots else None,
    )


def print_banner():
    banner = """
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│     YOLOX Nano — Data Drift Detection Tool                  │
│                                                             │
│     Detects distribution shifts in:                         │
│       • Image pixel distributions                           │
│       • Feature embeddings (backbone)                       │
│       • Model predictions (class, bbox, confidence)         │
│                                                             │
│     Statistical tests: KS, PSI, MMD, Chi², Wasserstein     │
│                                                             │
└─────────────────────────────────────────────────────────────┘
    """
    print(banner)


if __name__ == "__main__":
    main()
