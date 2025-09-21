# src/models/monai_models.py
import torch
import monai
from monai.data import Dataset, DataLoader, decollate_batch
from monai.transforms import *
from monai.networks.nets import UNet, DenseNet121
from monai.metrics import DiceMetric
import onnxruntime as ort
import numpy as np
from pathlib import Path

class MedicalImageProcessor:
    def __init__(self, device='cpu'):
        self.device = device
        self.setup_transforms()
        self.load_optimized_models()
        
    def setup_transforms(self):
        """Medical-specific preprocessing pipeline"""
        self.preprocess = Compose([
            LoadImage(image_only=True),
            EnsureChannelFirst(),
            Spacing(pixdim=(1.0, 1.0, 1.0), mode="bilinear"),
            ScaleIntensity(minv=0.0, maxv=1.0),
            CropForeground(),
            Resize(spatial_size=(256, 256, 128)),  # CPU-friendly size
            ToTensor()
        ])
        
    def load_optimized_models(self):
        """Load CPU-optimized ONNX models"""
        model_dir = Path("models/onnx/")
        model_dir.mkdir(exist_ok=True)
        
        # Lung segmentation model (ONNX for CPU efficiency)
        self.lung_seg_session = self._load_onnx_model("lung_segmentation.onnx")
        
        # Chest X-ray classification
        self.chest_cls_session = self._load_onnx_model("chest_classification.onnx")
        
    def _load_onnx_model(self, model_name):
        """Load ONNX model with CPU optimization"""
        model_path = Path("models/onnx") / model_name
        if model_path.exists():
            return ort.InferenceSession(
                str(model_path),
                providers=['CPUExecutionProvider'],
                sess_options=self._get_cpu_session_options()
            )
        return None
    
    def _get_cpu_session_options(self):
        """Optimize ONNX for CPU"""
        sess_options = ort.SessionOptions()
        sess_options.intra_op_num_threads = 4
        sess_options.inter_op_num_threads = 1
        sess_options.execution_mode = ort.ExecutionMode.ORT_SEQUENTIAL
        sess_options.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL
        return sess_options
    
    def segment_lungs(self, image_path):
        """Perform lung segmentation"""
        if self.lung_seg_session is None:
            return self._fallback_segmentation(image_path)
            
        # Preprocess image
        image = self.preprocess(image_path)
        image_np = image.cpu().numpy()
        
        # ONNX inference
        input_name = self.lung_seg_session.get_inputs()[0].name
        result = self.lung_seg_session.run(None, {input_name: image_np})
        
        return self._postprocess_segmentation(result[0])
    
    def classify_chest_xray(self, image_path):
        """Classify chest X-ray pathologies"""
        if self.chest_cls_session is None:
            return self._fallback_classification()
            
        image = self.preprocess(image_path)
        image_np = image.cpu().numpy()
        
        input_name = self.chest_cls_session.get_inputs()[0].name
        result = self.chest_cls_session.run(None, {input_name: image_np})
        
        return self._postprocess_classification(result[0])
