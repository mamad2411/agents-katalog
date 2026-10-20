---
name: diffusers
description: "HuggingFace Diffusers library for diffusion models: text-to-image, image-to-image, inpainting, super-resolution. Supports Stable Diffusion, Flux, SDXL, and custom pipelines."
tags: [diffusers, stable-diffusion, text-to-image, image-generation, huggingface, pytorch, zorai]
---

## Overview

HuggingFace Diffusers provides diffusion models for text-to-image, image-to-image, inpainting, and super-resolution. Supports Stable Diffusion, Flux, and SDXL with full pipeline customization.

## Installation

```bash
uv pip install diffusers transformers accelerate
```

## Text-to-Image

```python
from diffusers import StableDiffusionPipeline
import torch

pipe = StableDiffusionPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5",
    torch_dtype=torch.float16,
).to("cuda")

image = pipe("a photo of a cat wearing a space suit").images[0]
image.save("cat_astronaut.png")
```

## SDXL

```python
from diffusers import DiffusionPipeline

pipe = DiffusionPipeline.from_pretrained(
    "stabilityai/stable-diffusion-xl-base-1.0",
    torch_dtype=torch.float16,
).to("cuda")

image = pipe(prompt="a cinematic shot of a mountain", num_inference_steps=30).images[0]
```

## Inpainting

```python
from diffusers import StableDiffusionInpaintPipeline

pipe = StableDiffusionInpaintPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5", torch_dtype=torch.float16,
).to("cuda")

image = pipe(prompt="cat", image=init_image, mask_image=mask_image).images[0]
```

## Workflow

1. Install with uv pip install diffusers
2. Choose pipeline: StableDiffusionPipeline, StableDiffusionXLPipeline, FluxPipeline
3. Load model with .from_pretrained(model_id)
4. Generate with pipe(prompt).images[0]
5. Customize: num_inference_steps, guidance_scale, negative_prompt
6. Save with .save() or convert to PIL for further processing
