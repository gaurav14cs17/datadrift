"""
Image loading and preprocessing utilities for YOLOX Nano drift detection.
"""

import os
from pathlib import Path
from typing import List, Tuple, Optional

import numpy as np
from PIL import Image
from tqdm import tqdm


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
    if target_size:
        img = img.resize(target_size, Image.BILINEAR)
    return np.array(img)


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
    img_resized = img_pil.resize((new_w, new_h), Image.BILINEAR)

    padded = np.full((target_h, target_w, 3), 114, dtype=np.uint8)
    pad_h = (target_h - new_h) // 2
    pad_w = (target_w - new_w) // 2
    padded[pad_h:pad_h + new_h, pad_w:pad_w + new_w] = np.array(img_resized)

    img_float = padded.astype(np.float32)
    img_transposed = np.transpose(img_float, (2, 0, 1))  # HWC -> CHW

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
