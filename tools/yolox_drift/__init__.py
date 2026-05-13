"""
YOLOX Nano Data Drift Detection Tool.

Detects distribution shifts in images, feature embeddings,
and model predictions for YOLOX Nano object detection pipelines.
"""

__version__ = "1.0.0"
__author__ = "DataDrift Team"

from .config import MonitorConfig, DriftConfig, YOLOXNanoConfig
