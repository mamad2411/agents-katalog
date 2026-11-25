---
name: onnx-runtime
description: "ONNX Runtime — cross-platform ML inference optimizer. Convert PyTorch, TensorFlow, scikit-learn models to ONNX. GPU, CPU, and mobile acceleration. Quantization, graph optimization, and custom ops."
tags: [onnx, model-optimization, inference, cross-platform, quantization, edge, zorai]
---
## Overview

ONNX Runtime is a cross-platform ML inference engine that runs models in the ONNX format. Supports CPU, GPU (CUDA, DirectML), and mobile inference with graph optimizations, quantization, and custom operators.

## Installation

```bash
uv pip install onnxruntime  # CPU
uv pip install onnxruntime-gpu  # CUDA

# Convert first: from transformers, PyTorch, etc.
```

## Basic Inference

```python
import onnxruntime as ort
import numpy as np

session = ort.InferenceSession("model.onnx")
input_name = session.get_inputs()[0].name
output_name = session.get_outputs()[0].name

result = session.run([output_name], {input_name: np.random.randn(1, 3, 224, 224).astype(np.float32)})
print(result[0].shape)
```

## GPU and Optimization

```python
# GPU inference
session = ort.InferenceSession("model.onnx", providers=["CUDAExecutionProvider"])

# Enable optimizations
options = ort.SessionOptions()
options.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL
session = ort.InferenceSession("model.onnx", sess_options=options)
```

## Quantization

```python
from onnxruntime.quantization import quantize_dynamic, QuantType

quantize_dynamic("model.onnx", "model_quantized.onnx", weight_type=QuantType.QInt8)
# ~4x smaller, minimal accuracy loss
```

## References
- [ONNX Runtime docs](https://onnxruntime.ai/docs/)
- [ONNX model zoo](https://github.com/onnx/models)