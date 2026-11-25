---
name: captum
description: "Captum (PyTorch) — model interpretability and feature attribution. Integrated Gradients, DeepLIFT, SmoothGrad, Occlusion, SHAP approximation, and Layer-wise Relevance Propagation. For vision and text models."
tags: [captum, explainability, feature-attribution, integrated-gradients, pytorch, interpretability, zorai]
---
## Overview

Captum (Comprehension in PyTorch) provides model interpretability for PyTorch models. Implements Integrated Gradients, Gradient SHAP, DeepLIFT, Occlusion, Feature Ablation, and Layer Conductance. Supports computer vision, NLP, and tabular models.

## Installation

```bash
uv pip install captum
```

## Integrated Gradients

```python
import torch
import torch.nn as nn
from captum.attr import IntegratedGradients

model = nn.Linear(10, 2)
input = torch.randn(1, 10)
baseline = torch.zeros(1, 10)

ig = IntegratedGradients(model)
attrs = ig.attribute(input, baseline, target=0)
print(f"Feature attributions: {attrs}")
```

## Occlusion

```python
from captum.attr import Occlusion

occ = Occlusion(model)
attrs = occ.attribute(input, target=0, sliding_window_shapes=(1,))  # 1D
print(attrs)
```

## Visualization

```python
from captum.attr import visualization as viz

_ = viz.visualize_image_attr(
    attrs.squeeze().numpy(),
    original_image=input.squeeze().numpy(),
    method="heat_map",
    sign="absolute_value",
    show_colorbar=True,
)
```

## References
- [Captum docs](https://captum.ai/docs/)
- [Captum GitHub](https://github.com/pytorch/captum)