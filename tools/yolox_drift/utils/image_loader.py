"""
Image loading and preprocessing utilities for YOLOX Nano drift detection.
"""

import os
import json
import time
from pathlib import Path
from typing import List, Tuple, Optional

import numpy as np
from PIL import Image
from tqdm import tqdm

# #region agent log
_DBG_LOG = "/home/ggoswami/Project/Gaurav/DataDrift/.cursor/debug-61b8e1.log"
_DBG_SID = "61b8e1"
def _dbg(hid, loc, msg, data=None):
    try:
        with open(_DBG_LOG, "a") as f:
            f.write(json.dumps({"sessionId":_DBG_SID,"id":f"il_{int(time.time()*1000)}_{hid}","timestamp":int(time.time()*1000),"location":loc,"message":msg,"data":data or {},"runId":"run1","hypothesisId":hid})+"\n")
    except: pass
# #endregion


SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".webp"}


def list_images(directory: str) -> List[Path]:
    dir_path = Path(directory)
    images = sorted(
        p for p in dir_path.rglob("*")
        if p.suffix.lower() in SUPPORTED_EXTENSIONS
    )
    return images


def load_image(path: str, target_size: Optional[Tuple[int, int]] = None) -> np.ndarray:
    img = Image.open(path).convert("RGB")
    # #region agent log
    orig_size = img.size  # PIL size is (width, height)
    # #endregion
    if target_size:
        img = img.resize(target_size, Image.Resampling.BILINEAR)
    result = np.array(img)
    # #region agent log
    _dbg("H1", "image_loader.py:load_image", "load_image called", {"path": str(path)[-30:], "target_size": list(target_size) if target_size else None, "pil_orig_size_WH": list(orig_size), "pil_after_resize_WH": list(img.size), "numpy_shape_HWC": list(result.shape), "note": "PIL resize takes (W,H) but target_size may be (H,W)"})
    # #endregion
    return result


def load_image_batch(
    paths: List[str],
    target_size: Optional[Tuple[int, int]] = None,
    show_progress: bool = True,
) -> np.ndarray:
    iterator = tqdm(paths, desc="Loading images", disable=not show_progress)
    images = []
    for p in iterator:
        try:
            img = load_image(p, target_size)
            images.append(img)
        except Exception as e:
            print(f"Warning: Could not load {p}: {e}")
    if not images:
        raise ValueError("No images could be loaded from the provided paths.")
    if target_size is None:
        # Resize all to the most common shape to avoid ragged arrays
        shapes = [img.shape for img in images]
        target_shape = max(set(shapes), key=shapes.count)
        resized = []
        for img in images:
            if img.shape != target_shape:
                pil_img = Image.fromarray(img)
                pil_img = pil_img.resize(
                    (target_shape[1], target_shape[0]), Image.Resampling.BILINEAR
                )
                resized.append(np.array(pil_img))
            else:
                resized.append(img)
        images = resized
    return np.array(images)


def preprocess_for_yolox(
    image: np.ndarray,
    input_size: Tuple[int, int] = (416, 416),
) -> np.ndarray:
    """Preprocess image for YOLOX Nano inference (resize + pad + normalize)."""
    h, w = image.shape[:2]
    target_h, target_w = input_size
    ratio = min(target_h / h, target_w / w)
    new_h, new_w = int(h * ratio), int(w * ratio)

    img_pil = Image.fromarray(image)
    img_resized = img_pil.resize((new_w, new_h), Image.Resampling.BILINEAR)

    padded = np.full((target_h, target_w, 3), 114, dtype=np.uint8)
    pad_h = (target_h - new_h) // 2
    pad_w = (target_w - new_w) // 2
    padded[pad_h:pad_h + new_h, pad_w:pad_w + new_w] = np.array(img_resized)

    # YOLOX expects BGR channel order (trained with OpenCV)
    padded = padded[:, :, ::-1]

    img_float = padded.astype(np.float32)
    img_transposed = np.transpose(img_float, (2, 0, 1))  # HWC -> CHW

    # #region agent log
    _dbg("H2", "image_loader.py:preprocess_for_yolox", "preprocess result", {"input_shape": list(image.shape), "input_size": list(input_size), "output_shape": list(img_transposed.shape), "is_contiguous": bool(img_transposed.flags['C_CONTIGUOUS']), "dtype": str(img_transposed.dtype), "min": float(img_transposed.min()), "max": float(img_transposed.max())})
    # #endregion

    return img_transposed


def compute_image_statistics(images: np.ndarray) -> dict:
    """Compute per-channel statistics from a batch of images."""
    stats = {}
    for c, name in enumerate(["red", "green", "blue"]):
        channel = images[..., c].astype(np.float32)
        stats[f"{name}_mean"] = float(np.mean(channel))
        stats[f"{name}_std"] = float(np.std(channel))
        stats[f"{name}_median"] = float(np.median(channel))
        stats[f"{name}_skewness"] = float(_skewness(channel.flatten()))
        stats[f"{name}_kurtosis"] = float(_kurtosis(channel.flatten()))

    gray = np.mean(images.astype(np.float32), axis=-1)
    stats["brightness_mean"] = float(np.mean(gray))
    stats["brightness_std"] = float(np.std(gray))
    stats["contrast"] = float(np.std(gray) / (np.mean(gray) + 1e-8))

    return stats


def _skewness(arr: np.ndarray) -> float:
    mean = np.mean(arr)
    std = np.std(arr)
    if std < 1e-8:
        return 0.0
    return float(np.mean(((arr - mean) / std) ** 3))


def _kurtosis(arr: np.ndarray) -> float:
    mean = np.mean(arr)
    std = np.std(arr)
    if std < 1e-8:
        return 0.0
    return float(np.mean(((arr - mean) / std) ** 4) - 3.0)
