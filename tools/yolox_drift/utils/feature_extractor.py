"""
Feature extraction from YOLOX Nano backbone for embedding-based drift detection.
Supports both PyTorch and ONNX Runtime backends.
"""

from typing import List, Optional, Tuple

import numpy as np

try:
    import torch
    import torch.nn as nn
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False

try:
    import onnxruntime as ort
    ORT_AVAILABLE = True
except ImportError:
    ORT_AVAILABLE = False

from .image_loader import preprocess_for_yolox


class YOLOXFeatureExtractor:
    """
    Extract feature embeddings from YOLOX Nano's backbone.
    Uses the intermediate feature maps as a representation for drift detection.
    When no model is available, falls back to lightweight handcrafted features.
    """

    def __init__(
        self,
        model_path: Optional[str] = None,
        input_size: Tuple[int, int] = (416, 416),
        device: str = "cpu",
    ):
        self.input_size = input_size
        self.device = device
        self.model = None
        self.backend = "handcrafted"

        if model_path and model_path.endswith(".onnx") and ORT_AVAILABLE:
            self.model = ort.InferenceSession(
                model_path,
                providers=["CPUExecutionProvider"],
            )
            self.backend = "onnx"
        elif model_path and TORCH_AVAILABLE:
            self.model = torch.load(model_path, map_location=device)
            if hasattr(self.model, "eval"):
                self.model.eval()
            self.backend = "pytorch"

    def extract(self, images: np.ndarray) -> np.ndarray:
        if self.backend == "onnx":
            return self._extract_onnx(images)
        elif self.backend == "pytorch":
            return self._extract_pytorch(images)
        else:
            return self._extract_handcrafted(images)

    def _extract_onnx(self, images: np.ndarray) -> np.ndarray:
        embeddings = []
        for img in images:
            preprocessed = preprocess_for_yolox(img, self.input_size)
            input_tensor = np.expand_dims(preprocessed, axis=0).astype(np.float32)
            input_name = self.model.get_inputs()[0].name
            outputs = self.model.run(None, {input_name: input_tensor})
            feat = outputs[0].flatten()
            embeddings.append(feat)
        return np.array(embeddings)

    def _extract_pytorch(self, images: np.ndarray) -> np.ndarray:
        embeddings = []
        features_hook = []

        def hook_fn(module, input, output):
            features_hook.append(output.detach().cpu().numpy())

        backbone = _get_backbone(self.model)
        handle = backbone.register_forward_hook(hook_fn) if backbone else None

        for img in images:
            preprocessed = preprocess_for_yolox(img, self.input_size)
            input_tensor = torch.from_numpy(preprocessed).unsqueeze(0).to(self.device)
            features_hook.clear()
            with torch.no_grad():
                self.model(input_tensor)
            if features_hook:
                feat = features_hook[0]
                feat = np.mean(feat, axis=(2, 3)).flatten()  # global avg pool
            else:
                feat = self._extract_handcrafted(img[np.newaxis])[0]
            embeddings.append(feat)

        if handle:
            handle.remove()
        return np.array(embeddings)

    def _extract_handcrafted(self, images: np.ndarray) -> np.ndarray:
        """
        Lightweight feature extraction without a model.
        Computes color histograms, edge features, texture features.
        Produces a fixed-size 192-dimensional feature vector per image.
        """
        features = []
        for img in images:
            feat = []
            img_float = img.astype(np.float32) / 255.0

            for c in range(3):
                channel = img_float[..., c]
                hist, _ = np.histogram(channel, bins=32, range=(0, 1))
                hist = hist.astype(np.float32) / (hist.sum() + 1e-8)
                feat.extend(hist.tolist())

            gray = np.mean(img_float, axis=-1)
            feat.append(float(np.mean(gray)))
            feat.append(float(np.std(gray)))
            feat.append(float(np.percentile(gray, 25)))
            feat.append(float(np.median(gray)))
            feat.append(float(np.percentile(gray, 75)))

            # Gradient-based edge features
            gy = np.diff(gray, axis=0)
            gx = np.diff(gray, axis=1)
            grad_mag = np.sqrt(
                gy[:, :min(gx.shape[1], gy.shape[1])] ** 2
                + gx[:min(gy.shape[0], gx.shape[0]), :] ** 2
            )
            feat.append(float(np.mean(grad_mag)))
            feat.append(float(np.std(grad_mag)))

            # Spatial layout (divide into 4x4 grid, compute mean per cell)
            h, w = gray.shape
            gh, gw = h // 4, w // 4
            for i in range(4):
                for j in range(4):
                    cell = gray[i * gh:(i + 1) * gh, j * gw:(j + 1) * gw]
                    feat.append(float(np.mean(cell)))
                    feat.append(float(np.std(cell)))

            # Frequency domain features
            fft = np.fft.fft2(gray)
            fft_mag = np.abs(fft)
            feat.append(float(np.mean(fft_mag)))
            feat.append(float(np.std(fft_mag)))

            # Aspect ratio and size features
            feat.append(float(img.shape[1] / (img.shape[0] + 1e-8)))
            feat.append(float(img.shape[0] * img.shape[1]))

            features.append(feat)

        max_len = max(len(f) for f in features)
        for i, f in enumerate(features):
            if len(f) < max_len:
                features[i] = f + [0.0] * (max_len - len(f))

        return np.array(features, dtype=np.float32)


def _get_backbone(model):
    """Try to get the backbone module from a YOLOX model."""
    for name in ["backbone", "dark", "stem"]:
        if hasattr(model, name):
            return getattr(model, name)
    children = list(model.children()) if hasattr(model, "children") else []
    if children:
        return children[0]
    return None
