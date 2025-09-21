# src/models/cpu_optimizers.py
import torch
import torch.quantization as quantization
import onnx
from onnxruntime.quantization import quantize_dynamic, QuantType
import psutil
import gc

class CPUOptimizer:
    def __init__(self):
        self.memory_threshold = 0.8  # 80% memory usage limit
        
    def optimize_pytorch_model(self, model, sample_input):
        """Convert PyTorch model to optimized ONNX"""
        model.eval()
        
        # Dynamic quantization for CPU
        quantized_model = quantization.quantize_dynamic(
            model, {torch.nn.Linear, torch.nn.Conv2d, torch.nn.Conv3d},
            dtype=torch.qint8
        )
        
        # Export to ONNX
        torch.onnx.export(
            quantized_model,
            sample_input,
            "temp_model.onnx",
            export_params=True,
            opset_version=11,
            do_constant_folding=True,
            input_names=['input'],
            output_names=['output'],
            dynamic_axes={'input': {0: 'batch_size'},
                         'output': {0: 'batch_size'}}
        )
        
        # Further ONNX optimization
        self.optimize_onnx_model("temp_model.onnx")
        
    def optimize_onnx_model(self, model_path):
        """Apply ONNX quantization and optimization"""
        output_path = model_path.replace('.onnx', '_optimized.onnx')
        
        quantize_dynamic(
            model_path,
            output_path,
            weight_type=QuantType.QInt8,
            optimize_model=True
        )
        
        return output_path
    
    def monitor_resources(self):
        """Real-time resource monitoring"""
        memory = psutil.virtual_memory()
        cpu = psutil.cpu_percent(interval=1)
        
        if memory.percent > self.memory_threshold * 100:
            gc.collect()  # Force garbage collection
            
        return {
            'memory_percent': memory.percent,
            'memory_gb': memory.used / (1024**3),
            'cpu_percent': cpu,
            'available_memory': memory.available / (1024**3)
        }
