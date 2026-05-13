# YOLOX Nano — Data Drift Detection Tool

```
┌──────────────────────────────────────────────────────────────────────┐
│                                                                      │
│     ╔═══╗  YOLOX Nano                                                │
│     ║ Y ║  Data Drift Detection & Monitoring                         │
│     ╚═══╝                                                            │
│                                                                      │
│     Detect distribution shifts in images and model predictions        │
│     before they silently degrade your object detection pipeline.      │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

## Overview

A comprehensive toolkit for detecting **data drift** in YOLOX Nano object detection pipelines. Monitors changes in image distributions, feature embeddings, and model outputs to alert when retraining or investigation is needed.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                     HOW IT WORKS                                         │
│                                                                         │
│   Reference Data         Production Data                                │
│   (Training Set)         (Live Inference)                               │
│        │                       │                                        │
│        ▼                       ▼                                        │
│   ┌─────────┐            ┌─────────┐                                   │
│   │  Load   │            │  Load   │                                   │
│   │ Images  │            │ Images  │                                   │
│   └────┬────┘            └────┬────┘                                   │
│        │                      │                                         │
│        ▼                      ▼                                         │
│   ┌─────────────────────────────────────┐                              │
│   │         Feature Extraction          │                              │
│   │  • Pixel histograms (RGB channels)  │                              │
│   │  • Backbone embeddings (YOLOX)      │                              │
│   │  • Handcrafted features (fallback)  │                              │
│   └─────────────────┬───────────────────┘                              │
│                     │                                                   │
│                     ▼                                                   │
│   ┌─────────────────────────────────────┐                              │
│   │       Statistical Drift Tests       │                              │
│   │                                     │                              │
│   │  • KS Test (distribution equality)  │                              │
│   │  • PSI (population stability)       │                              │
│   │  • MMD (kernel embedding distance)  │                              │
│   │  • Chi² (categorical drift)         │                              │
│   │  • Wasserstein (earth mover's)      │                              │
│   │  • JS Divergence (information)      │                              │
│   └─────────────────┬───────────────────┘                              │
│                     │                                                   │
│                     ▼                                                   │
│   ┌─────────────────────────────────────┐                              │
│   │           Drift Report              │                              │
│   │                                     │                              │
│   │  • Terminal dashboard (Rich)        │                              │
│   │  • Matplotlib visualizations        │                              │
│   │  • Per-feature breakdown            │                              │
│   │  • Severity classification          │                              │
│   └─────────────────────────────────────┘                              │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

## Directory Structure

```
tools/
├── requirements.txt                  ← Dependencies
├── README.md                         ← This file
└── yolox_drift/
    ├── __init__.py
    ├── __main__.py                   ← python -m yolox_drift
    ├── cli.py                        ← Command-line interface
    ├── config.py                     ← Configuration dataclasses
    ├── detectors/
    │   ├── __init__.py
    │   ├── statistical_tests.py      ← KS, PSI, MMD, Chi², Wasserstein, JS
    │   ├── image_drift.py            ← Image-level drift detection
    │   └── prediction_drift.py       ← Prediction-level drift detection
    ├── utils/
    │   ├── __init__.py
    │   ├── image_loader.py           ← Image loading & preprocessing
    │   └── feature_extractor.py      ← Feature extraction (ONNX/PyTorch/handcrafted)
    ├── reports/
    │   ├── __init__.py
    │   └── drift_report.py           ← Report generation (Rich + Matplotlib)
    └── examples/
        ├── __init__.py
        └── demo_drift_detection.py   ← Usage demo with synthetic data
```

## Installation

```bash
cd tools/
pip install -r requirements.txt
```

## Quick Start

### CLI Usage

```bash
# Basic image drift detection (no model required)
python -m yolox_drift --ref-dir data/reference/ --prod-dir data/production/

# With YOLOX Nano model for deeper embedding analysis
python -m yolox_drift --ref-dir data/ref/ --prod-dir data/prod/ --model yolox_nano.onnx

# Custom significance level and output
python -m yolox_drift --ref-dir data/ref/ --prod-dir data/prod/ \
    --alpha 0.01 --output my_reports/ --max-images 1000
```

### Python API Usage

```python
from yolox_drift.detectors.image_drift import ImageDriftDetector
from yolox_drift.detectors.prediction_drift import PredictionDriftDetector
from yolox_drift.reports.drift_report import DriftReportGenerator

# Image-level drift
detector = ImageDriftDetector(model_path="yolox_nano.onnx", input_size=(416, 416))
results = detector.detect(
    reference_dir="data/reference/",
    production_dir="data/production/",
    alpha=0.05,
    max_images=500,
)

print(results["summary"])
# {'overall_status': 'WARNING', 'total_tests': 12, 'drifted_tests': 4, ...}

# Generate visual report
reporter = DriftReportGenerator(output_dir="reports/")
reporter.generate(image_results=results)
```

### Prediction-Level Drift

```python
from yolox_drift.detectors.prediction_drift import PredictionDriftDetector

detector = PredictionDriftDetector(num_classes=80)
results = detector.detect(ref_predictions, prod_predictions)

# Check class distribution drift
if results["class_distribution"]["chi_square"].is_drift:
    print("Class distribution has shifted!")

# Check confidence degradation
conf = results["confidence_drift"]
print(f"Confidence: {conf['ref_mean_confidence']:.3f} → {conf['prod_mean_confidence']:.3f}")
```

## Drift Detection Levels

```
┌────────────────────────────────────────────────────────────────────┐
│                   THREE LEVELS OF DETECTION                         │
├────────────────────────────────────────────────────────────────────┤
│                                                                    │
│  Level 1: PIXEL-LEVEL                                              │
│  ─────────────────────                                             │
│  • Per-channel (R/G/B) histogram shifts                            │
│  • Brightness & contrast changes                                   │
│  • Color distribution statistics                                   │
│  • Detect: camera changes, lighting shifts, weather effects        │
│                                                                    │
│  Level 2: FEATURE-LEVEL (Embeddings)                               │
│  ───────────────────────────────────                               │
│  • YOLOX backbone feature space (if model provided)                │
│  • Handcrafted features: gradients, texture, spatial layout        │
│  • MMD test in embedding space                                     │
│  • Detect: scene composition changes, new object types             │
│                                                                    │
│  Level 3: PREDICTION-LEVEL                                         │
│  ─────────────────────────                                         │
│  • Class distribution drift (what objects are found)               │
│  • Bounding box size/position changes                              │
│  • Confidence score degradation                                    │
│  • Detection count per image                                       │
│  • Detect: model degradation, deployment errors, label drift       │
│                                                                    │
└────────────────────────────────────────────────────────────────────┘
```

## Statistical Tests

| Test | Type | Best For | Speed |
|------|------|----------|-------|
| **KS Test** | Non-parametric | Continuous features, general-purpose | Fast |
| **PSI** | Binned comparison | Production monitoring, thresholds | Fast |
| **Chi-Square** | Categorical | Class distributions | Fast |
| **MMD** | Kernel-based | High-dimensional embeddings | Slow |
| **Wasserstein** | Optimal transport | Measuring magnitude of shift | Fast |
| **JS Divergence** | Information-theoretic | Comparing probability distributions | Fast |

## Severity Levels

```
┌──────────────────────────────────────────────────────────────┐
│                                                              │
│   ● HEALTHY        No significant drift detected             │
│                    Action: None required                      │
│                                                              │
│   ● MINOR DRIFT   Some tests flag drift, likely noise        │
│                    Action: Monitor closely                    │
│                                                              │
│   ● WARNING        Multiple features drifting                 │
│                    Action: Investigate, prepare retraining    │
│                                                              │
│   ● CRITICAL       Severe distribution shift                  │
│                    Action: Immediate retraining or rollback   │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

## YOLOX Nano Model

This tool is designed specifically for **YOLOX Nano** — the smallest variant in the YOLOX family:

```
┌─────────────────────────────────────────────────────────┐
│  YOLOX Nano Specifications                              │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Architecture:  CSPDarknet (Nano) + PAFPN + YOLOX Head  │
│  Input Size:    416 × 416                               │
│  Parameters:    0.91M                                   │
│  FLOPs:         1.08G                                   │
│  COCO mAP:     25.8% (AP@0.5:0.95)                     │
│  Speed:         ~3ms (TensorRT FP16, T4 GPU)            │
│                                                         │
│  Use Case:      Edge/Mobile deployment where drift      │
│                 detection is critical due to             │
│                 environment variability                  │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### Supported Model Formats

- **ONNX** (`.onnx`) — Recommended, uses ONNX Runtime
- **PyTorch** (`.pth`, `.pt`) — Uses PyTorch, supports GPU
- **No model** — Falls back to handcrafted features (still effective!)

## Example Output

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│     YOLOX Nano — Data Drift Detection Report                │
│     2024-11-15 14:32:00                                     │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Image-Level Drift: ⚠ WARNING                               │
│  Tests: 4/12 drifted | Critical: 1 | Warning: 3            │
│                                                             │
│  ┌──────────────────────────────────────────────────┐      │
│  │ Pixel-Level Tests                                 │      │
│  ├──────────┬───────────┬─────────┬────────┬────────┤      │
│  │ Test     │ Statistic │ P-Value │ Status │ Sev.   │      │
│  ├──────────┼───────────┼─────────┼────────┼────────┤      │
│  │ Red KS   │ 0.1234    │ 0.0321  │ DRIFT  │ WARN   │      │
│  │ Green KS │ 0.0456    │ 0.4521  │ OK     │ NONE   │      │
│  │ Blue KS  │ 0.2345    │ 0.0012  │ DRIFT  │ CRIT   │      │
│  │ Bright.  │ 0.0789    │ 0.1234  │ OK     │ NONE   │      │
│  └──────────┴───────────┴─────────┴────────┴────────┘      │
│                                                             │
│  Prediction-Level Drift: ✓ HEALTHY                          │
│                                                             │
│  Overall Status: ⚠ WARNING                                  │
│  Report saved to: drift_reports/                            │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Run Demo

```bash
# Run synthetic demos (no data needed)
cd tools/
python -m yolox_drift.examples.demo_drift_detection

# Run with real data
python -m yolox_drift.examples.demo_drift_detection \
    --ref-dir /path/to/reference/images \
    --prod-dir /path/to/production/images
```

## Integration with YOLOX Pipeline

```python
# In your inference pipeline:
from yolox_drift.detectors.image_drift import ImageDriftDetector

# Initialize once
drift_monitor = ImageDriftDetector(model_path="yolox_nano.onnx")

# Periodically check drift (e.g., every 1000 images)
def check_drift_periodically(new_batch_dir, reference_dir):
    results = drift_monitor.detect(reference_dir, new_batch_dir)
    if results["summary"]["overall_status"] in ["WARNING", "CRITICAL"]:
        send_alert(results)
        trigger_retraining()
```

## License

MIT — See root [LICENSE](../LICENSE) for details.
