"""Test script to exercise the full preprocessing pipeline with synthetic images."""

import sys
import json
import time
import tempfile
import traceback
from pathlib import Path

import numpy as np
from PIL import Image

LOG_PATH = "/home/ggoswami/Project/Gaurav/DataDrift/.cursor/debug-61b8e1.log"
SESSION_ID = "61b8e1"
RUN_ID = "run1"

def _log(hypothesis_id, location, message, data=None):
    entry = {
        "sessionId": SESSION_ID,
        "id": f"log_{int(time.time()*1000)}_{hypothesis_id}",
        "timestamp": int(time.time() * 1000),
        "location": location,
        "message": message,
        "data": data or {},
        "runId": RUN_ID,
        "hypothesisId": hypothesis_id,
    }
    with open(LOG_PATH, "a") as f:
        f.write(json.dumps(entry) + "\n")


def generate_synthetic_images(directory, num_images=20, size=(480, 640, 3), seed=42):
    """Generate synthetic images with known properties."""
    rng = np.random.default_rng(seed)
    Path(directory).mkdir(parents=True, exist_ok=True)
    for i in range(num_images):
        img_arr = rng.integers(0, 256, size=size, dtype=np.uint8)
        img = Image.fromarray(img_arr)
        img.save(Path(directory) / f"img_{i:04d}.png")
    _log("setup", "test_preprocessing.py:generate", f"Generated {num_images} images",
         {"dir": directory, "size": list(size)})


def test_h1_dimension_swap():
    """H1: Test if load_image swaps height/width for non-square target_size."""
    from yolox_drift.utils.image_loader import load_image
    with tempfile.TemporaryDirectory() as tmpdir:
        arr = np.zeros((480, 640, 3), dtype=np.uint8)
        arr[:240, :, 0] = 255  # top half red
        path = Path(tmpdir) / "test.png"
        Image.fromarray(arr).save(path)

        target_size = (300, 200)  # intended as (H, W) per preprocess_for_yolox convention
        loaded = load_image(str(path), target_size=target_size)
        _log("H1", "test_preprocessing.py:test_h1", "load_image dimension test", {
            "target_size_passed": list(target_size),
            "loaded_shape": list(loaded.shape),
            "expected_HW": [300, 200],
            "actual_HW": [loaded.shape[0], loaded.shape[1]],
            "dimensions_swapped": loaded.shape[0] != 300 or loaded.shape[1] != 200,
        })


def test_h2_bgr_contiguity():
    """H2: Test if preprocess_for_yolox produces contiguous arrays."""
    from yolox_drift.utils.image_loader import preprocess_for_yolox
    img = np.random.randint(0, 256, (480, 640, 3), dtype=np.uint8)
    result = preprocess_for_yolox(img, input_size=(416, 416))
    _log("H2", "test_preprocessing.py:test_h2", "preprocess_for_yolox contiguity", {
        "output_shape": list(result.shape),
        "dtype": str(result.dtype),
        "is_contiguous": bool(result.flags['C_CONTIGUOUS']),
        "is_f_contiguous": bool(result.flags['F_CONTIGUOUS']),
        "min_val": float(result.min()),
        "max_val": float(result.max()),
        "expected_shape": [3, 416, 416],
    })
    # Also check if channel order was actually swapped
    rgb_img = np.zeros((100, 100, 3), dtype=np.uint8)
    rgb_img[:, :, 0] = 200  # R=200, G=0, B=0
    result2 = preprocess_for_yolox(rgb_img, input_size=(100, 100))
    ch0_mean = float(result2[0].mean())
    ch1_mean = float(result2[1].mean())
    ch2_mean = float(result2[2].mean())
    _log("H2", "test_preprocessing.py:test_h2_bgr", "BGR channel order verification", {
        "input": "R=200, G=0, B=0",
        "output_ch0_mean": ch0_mean,
        "output_ch1_mean": ch1_mean,
        "output_ch2_mean": ch2_mean,
        "bgr_correct": ch0_mean < 10 and ch2_mean > 150,
        "note": "If BGR correct: ch0(B)~0, ch1(G)~0, ch2(R)~200",
    })


def test_h3_statistics_drift():
    """H3: Test compute_image_statistics returns single scalars (no distribution)."""
    from yolox_drift.utils.image_loader import compute_image_statistics
    rng = np.random.default_rng(42)
    batch = rng.integers(0, 256, (20, 100, 100, 3), dtype=np.uint8)
    stats = compute_image_statistics(batch)
    _log("H3", "test_preprocessing.py:test_h3", "compute_image_statistics output", {
        "keys": list(stats.keys()),
        "values_are_scalars": all(isinstance(v, float) for v in stats.values()),
        "red_mean": stats.get("red_mean"),
        "red_std": stats.get("red_std"),
        "num_keys": len(stats),
        "note": "These are global scalars, not per-image distributions",
    })


def test_h4_mmd_performance():
    """H4: Test _compute_mmd memory and time with realistic sizes."""
    from yolox_drift.detectors.statistical_tests import _compute_mmd, mmd_test
    rng = np.random.default_rng(42)

    # Small test first
    x_small = rng.normal(0, 1, (50, 139))
    y_small = rng.normal(0, 1, (50, 139))
    t0 = time.time()
    mmd_val = _compute_mmd(x_small, y_small)
    t_small = time.time() - t0
    _log("H4", "test_preprocessing.py:test_h4_small", "_compute_mmd small test", {
        "shape_x": list(x_small.shape), "shape_y": list(y_small.shape),
        "time_sec": round(t_small, 4), "mmd_value": mmd_val,
    })

    # Realistic size
    x_real = rng.normal(0, 1, (200, 139))
    y_real = rng.normal(0, 1, (200, 139))
    t0 = time.time()
    try:
        result = mmd_test(x_real, y_real, n_permutations=100)
        t_real = time.time() - t0
        _log("H4", "test_preprocessing.py:test_h4_real", "mmd_test realistic size", {
            "shape_x": list(x_real.shape), "time_sec": round(t_real, 2),
            "n_permutations": 100, "statistic": result.statistic,
            "p_value": result.p_value, "is_drift": result.is_drift,
            "estimated_500perm_time": round(t_real * 5, 2),
        })
    except Exception as e:
        t_real = time.time() - t0
        _log("H4", "test_preprocessing.py:test_h4_real_error", "mmd_test FAILED", {
            "error": str(e), "time_sec": round(t_real, 2),
            "traceback": traceback.format_exc(),
        })


def test_h5_feature_length():
    """H5: Test actual handcrafted feature vector length."""
    from yolox_drift.utils.feature_extractor import YOLOXFeatureExtractor
    extractor = YOLOXFeatureExtractor(model_path=None, input_size=(416, 416))
    rng = np.random.default_rng(42)
    images = rng.integers(0, 256, (5, 416, 416, 3), dtype=np.uint8)
    feats = extractor.extract(images)
    _log("H5", "test_preprocessing.py:test_h5", "handcrafted feature extraction", {
        "backend": extractor.backend,
        "input_shape": list(images.shape),
        "output_shape": list(feats.shape),
        "feature_dim": int(feats.shape[1]),
        "docstring_says": 192,
        "mismatch": feats.shape[1] != 192,
        "all_finite": bool(np.all(np.isfinite(feats))),
        "has_nan": bool(np.any(np.isnan(feats))),
    })


def test_full_pipeline():
    """Run the full pipeline with synthetic images to find crashes."""
    with tempfile.TemporaryDirectory() as tmpdir:
        ref_dir = Path(tmpdir) / "ref"
        prod_dir = Path(tmpdir) / "prod"
        generate_synthetic_images(str(ref_dir), num_images=15, size=(480, 640, 3), seed=42)
        generate_synthetic_images(str(prod_dir), num_images=15, size=(480, 640, 3), seed=99)

        from yolox_drift.detectors.image_drift import ImageDriftDetector
        detector = ImageDriftDetector(input_size=(416, 416))

        _log("pipeline", "test_preprocessing.py:pipeline", "Starting full pipeline test", {})
        t0 = time.time()
        try:
            results = detector.detect(str(ref_dir), str(prod_dir), max_images=15)
            elapsed = time.time() - t0
            _log("pipeline", "test_preprocessing.py:pipeline_ok", "Pipeline completed", {
                "elapsed_sec": round(elapsed, 2),
                "summary": results.get("summary"),
                "pixel_drift_keys": list(results.get("pixel_drift", {}).keys()),
                "embedding_drift_keys": list(results.get("embedding_drift", {}).keys()),
            })
        except Exception as e:
            elapsed = time.time() - t0
            _log("pipeline", "test_preprocessing.py:pipeline_error", "Pipeline FAILED", {
                "error": str(e), "elapsed_sec": round(elapsed, 2),
                "traceback": traceback.format_exc(),
            })


def main():
    _log("start", "test_preprocessing.py:main", "=== Test run started ===", {})

    tests = [
        ("H1: Dimension swap", test_h1_dimension_swap),
        ("H2: BGR contiguity", test_h2_bgr_contiguity),
        ("H3: Statistics drift", test_h3_statistics_drift),
        ("H4: MMD performance", test_h4_mmd_performance),
        ("H5: Feature length", test_h5_feature_length),
        ("Full pipeline", test_full_pipeline),
    ]

    for name, fn in tests:
        _log("test", "test_preprocessing.py:main", f"Running: {name}", {})
        try:
            fn()
        except Exception as e:
            _log("test_error", "test_preprocessing.py:main", f"CRASHED: {name}", {
                "error": str(e), "traceback": traceback.format_exc(),
            })

    _log("end", "test_preprocessing.py:main", "=== Test run finished ===", {})
    print("Test run complete. Check logs.")


if __name__ == "__main__":
    main()
