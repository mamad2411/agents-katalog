---
name: open-clip
description: "OpenCLIP — open-source implementation of CLIP trained on LAION-5B/OpenCLIP datasets. Multi-head attention pooling, SigLIP loss variants, and wide model zoo (ViT, ConvNeXt, EVA). Community-driven."
tags: [open-clip, multimodal, image-text, laion, zero-shot, embeddings, zorai]
---
## Overview

OpenCLIP is an open-source reimplementation of CLIP trained on LAION-5B, LAION-400M, and DataComp. Provides larger and better architectures than the original: ViT-H/14, ConvNeXt, EVA-02, SigLIP. Full model transparency with flexible training customizations.

## Installation

```bash
uv pip install open-clip-torch
```

## Encoding Images and Text

```python
import open_clip
import torch
from PIL import Image

model, _, preprocess = open_clip.create_model_and_transforms(
    "ViT-H-14", pretrained="laion2b_s32b_b79k")
tokenizer = open_clip.get_tokenizer("ViT-H-14")

image = preprocess(Image.open("photo.jpg")).unsqueeze(0)
text = tokenizer(["a dog", "a cat", "a car"])

with torch.no_grad():
    image_features = model.encode_image(image)
    text_features = model.encode_text(text)
    logits = (image_features @ text_features.T).softmax(dim=-1)
    print(f"Predicted: class {logits.argmax().item()} with {logits.max():.2%}")
```

## References
- [OpenCLIP GitHub](https://github.com/mlfoundations/open_clip)
- [OpenCLIP paper](https://arxiv.org/abs/2211.04293)