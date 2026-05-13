"""
Configuration for YOLOX Nano Data Drift Detection Tool.
"""

from dataclasses import dataclass, field
from typing import Optional
from pathlib import Path


@dataclass
class YOLOXNanoConfig:
    input_size: tuple = (416, 416)
    num_classes: int = 80
    confidence_threshold: float = 0.25
    nms_threshold: float = 0.45
    model_path: Optional[str] = None
    device: str = "cpu"


@dataclass
class DriftConfig:
    significance_level: float = 0.05
    psi_warn_threshold: float = 0.1
    psi_critical_threshold: float = 0.25
    ks_warn_threshold: float = 0.1
    mmd_num_permutations: int = 1000
    embedding_layer: str = "backbone"
    num_histogram_bins: int = 50
    min_sample_size: int = 30


@dataclass
class MonitorConfig:
    reference_dir: str = ""
    production_dir: str = ""
    output_dir: str = "drift_reports"
    batch_size: int = 16
    num_workers: int = 4
    save_plots: bool = True
    report_format: str = "html"
    yolox: YOLOXNanoConfig = field(default_factory=YOLOXNanoConfig)
    drift: DriftConfig = field(default_factory=DriftConfig)

    def validate(self):
        assert Path(self.reference_dir).exists(), f"Reference dir not found: {self.reference_dir}"
        assert Path(self.production_dir).exists(), f"Production dir not found: {self.production_dir}"
        Path(self.output_dir).mkdir(parents=True, exist_ok=True)


COCO_CLASSES = [
    "person", "bicycle", "car", "motorcycle", "airplane", "bus", "train",
    "truck", "boat", "traffic light", "fire hydrant", "stop sign",
    "parking meter", "bench", "bird", "cat", "dog", "horse", "sheep",
    "cow", "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella",
    "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard",
    "sports ball", "kite", "baseball bat", "baseball glove", "skateboard",
    "surfboard", "tennis racket", "bottle", "wine glass", "cup", "fork",
    "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange",
    "broccoli", "carrot", "hot dog", "pizza", "donut", "cake", "chair",
    "couch", "potted plant", "bed", "dining table", "toilet", "tv",
    "laptop", "mouse", "remote", "keyboard", "cell phone", "microwave",
    "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase",
    "scissors", "teddy bear", "hair drier", "toothbrush",
]
