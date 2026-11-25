---
name: stable-diffusion
description: Text-to-image generation, inpainting, and img2img.
version: 1.0.0
author: Orchestra Research
license: MIT
dependencies: [diffusers>=0.30.0, transformers>=4.41.0, accelerate>=0.31.0, torch>=2.0.0]
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Image Generation, Stable Diffusion, Diffusers, Text-to-Image, Multimodal, Computer Vision]

---

# Stable Diffusion 图像生成

本指南介绍如何使用 HuggingFace Diffusers 库通过 Stable Diffusion 生成图像。

## 何时使用 Stable Diffusion

**以下情况适合使用 Stable Diffusion：**
- 根据文本描述生成图像
- 执行图像到图像的转换（风格迁移、图像增强）
- 修复画布（填充被遮盖的区域）
- 扩展画布范围（将图像延伸至边界之外）
- 创建现有图像的变体
- 构建自定义的图像生成工作流

**核心功能：**
- **文本转图像**：根据自然语言提示词生成图像
- **图像转图像**：在文本引导下对现有图像进行变换
- **修复画布**：用符合上下文的内容填充被遮盖区域
- **ControlNet**：添加空间条件控制（边缘、姿态、深度等）
- **LoRA 支持**：高效的微调与风格适配功能
- **多种模型支持**：兼容 SD 1.5、SDXL、SD 3.0 以及 Flux 模型

**如需其他替代方案，可考虑：**
- **DALL-E 3**：适用于无需 GPU 的基于 API 的图像生成
- **Midjourney**：适合生成具有艺术风格的效果
- **Imagen**：支持与 Google Cloud 集成
- **Leonardo.ai**：适用于基于网页的创意工作流

## 快速入门

### 安装

```bash
pip install diffusers transformers accelerate torch
pip install xformers  # Optional: memory-efficient attention
```

### 基础文本转图像功能

```python
from diffusers import DiffusionPipeline
import torch

# Load pipeline (auto-detects model type)
pipe = DiffusionPipeline.from_pretrained(
    "stable-diffusion-v1-5/stable-diffusion-v1-5",
    torch_dtype=torch.float16
)
pipe.to("cuda")

# Generate image
image = pipe(
    "A serene mountain landscape at sunset, highly detailed",
    num_inference_steps=50,
    guidance_scale=7.5
).images[0]

image.save("output.png")
```

### 使用 SDXL（更高画质）

```python
from diffusers import AutoPipelineForText2Image
import torch

pipe = AutoPipelineForText2Image.from_pretrained(
    "stabilityai/stable-diffusion-xl-base-1.0",
    torch_dtype=torch.float16,
    variant="fp16"
)
pipe.to("cuda")

# Enable memory optimization
pipe.enable_model_cpu_offload()

image = pipe(
    prompt="A futuristic city with flying cars, cinematic lighting",
    height=1024,
    width=1024,
    num_inference_steps=30
).images[0]
```

## 架构概览

### 三大核心组件设计

Diffusers 由三个核心组件构成：

```
Pipeline (orchestration)
├── Model (neural networks)
│   ├── UNet / Transformer (noise prediction)
│   ├── VAE (latent encoding/decoding)
│   └── Text Encoder (CLIP/T5)
└── Scheduler (denoising algorithm)
```

### 流水线推理流程

```
Text Prompt → Text Encoder → Text Embeddings
                                    ↓
Random Noise → [Denoising Loop] ← Scheduler
                      ↓
               Predicted Noise
                      ↓
              VAE Decoder → Final Image
```

## 核心概念

### 流水线

流水线用于统筹整个工作流程：

| 流水线名称 | 功能 |
|----------|------|
| `StableDiffusionPipeline` | 文本生成图像（SD 1.x/2.x） |
| `StableDiffusionXLPipeline` | 文本生成图像（SDXL） |
| `StableDiffusion3Pipeline` | 文本生成图像（SD 3.0） |
| `FluxPipeline` | 文本生成图像（Flux 模型） |
| `StableDiffusionImg2ImgPipeline` | 图像转图像 |
| `StableDiffusionInpaintPipeline` | 修复绘图 |

### 调度器

调度器用于控制去噪过程：

| 调度器名称 | 步数 | 图像质量 | 典型应用场景 |
|-----------|------|----------|--------------|
| `EulerDiscreteScheduler` | 20-50 | 较好 | 默认选择 |
| `EulerAncestralDiscreteScheduler` | 20-50 | 较好 | 更多的变化效果 |
| `DPMSolverMultistepScheduler` | 15-25 | 极佳 | 速度快且质量高 |
| `DDIMScheduler` | 50-100 | 较好 | 具有确定性 |
| `LCMScheduler` | 4-8 | 较好 | 速度极快 |
| `UniPCMultistepScheduler` | 15-25 | 极佳 | 收敛速度快 |

### 更换调度器

```python
from diffusers import DPMSolverMultistepScheduler

# Swap for faster generation
pipe.scheduler = DPMSolverMultistepScheduler.from_config(
    pipe.scheduler.config
)

# Now generate with fewer steps
image = pipe(prompt, num_inference_steps=20).images[0]
```

## 生成参数

### 核心参数

| 参数 | 默认值 | 描述 |
|------|--------|------|
| `prompt` | 必填 | 所需图像的文本描述 |
| `negative_prompt` | 无 | 需要避免出现在图像中的内容 |
| `num_inference_steps` | 50 | 去噪步数（步数越多，图像质量越高） |
| `guidance_scale` | 7.5 | 提示词遵循程度（通常范围为7-12） |
| `height`, `width` | 512/1024 | 输出尺寸（需为8的倍数） |
| `generator` | 无 | 用于确保结果可复现的Torch生成器 |
| `num_images_per_prompt` | 1 | 批量生成数量 |

### 可复现的图像生成

```python
import torch

generator = torch.Generator(device="cuda").manual_seed(42)

image = pipe(
    prompt="A cat wearing a top hat",
    generator=generator,
    num_inference_steps=50
).images[0]
```

### 负面提示词

```python
image = pipe(
    prompt="Professional photo of a dog in a garden",
    negative_prompt="blurry, low quality, distorted, ugly, bad anatomy",
    guidance_scale=7.5
).images[0]
```

## 图像到图像转换

在文本引导下对现有图像进行变换：

```python
from diffusers import AutoPipelineForImage2Image
from PIL import Image

pipe = AutoPipelineForImage2Image.from_pretrained(
    "stable-diffusion-v1-5/stable-diffusion-v1-5",
    torch_dtype=torch.float16
).to("cuda")

init_image = Image.open("input.jpg").resize((512, 512))

image = pipe(
    prompt="A watercolor painting of the scene",
    image=init_image,
    strength=0.75,  # How much to transform (0-1)
    num_inference_steps=50
).images[0]
```

## 修复填充功能

填充被遮盖的区域：

```python
from diffusers import AutoPipelineForInpainting
from PIL import Image

pipe = AutoPipelineForInpainting.from_pretrained(
    "runwayml/stable-diffusion-inpainting",
    torch_dtype=torch.float16
).to("cuda")

image = Image.open("photo.jpg")
mask = Image.open("mask.png")  # White = inpaint region

result = pipe(
    prompt="A red car parked on the street",
    image=image,
    mask_image=mask,
    num_inference_steps=50
).images[0]
```

## ControlNet

通过空间约束实现精准控制：

```python
from diffusers import StableDiffusionControlNetPipeline, ControlNetModel
import torch

# Load ControlNet for edge conditioning
controlnet = ControlNetModel.from_pretrained(
    "lllyasviel/control_v11p_sd15_canny",
    torch_dtype=torch.float16
)

pipe = StableDiffusionControlNetPipeline.from_pretrained(
    "stable-diffusion-v1-5/stable-diffusion-v1-5",
    controlnet=controlnet,
    torch_dtype=torch.float16
).to("cuda")

# Use Canny edge image as control
control_image = get_canny_image(input_image)

image = pipe(
    prompt="A beautiful house in the style of Van Gogh",
    image=control_image,
    num_inference_steps=30
).images[0]
```

### 可用的 ControlNets

| ControlNet | 输入类型 | 应用场景 |
|------------|----------|----------|
| `canny` | 边缘图 | 保留结构特征 |
| `openpose` | 姿态骨架 | 人物姿态生成 |
| `depth` | 深度图 | 具有3D感知的生成 |
| `normal` | 法线图 | 表面细节表现 |
| `mlsd` | 线段 | 建筑线条绘制 |
| `scribble` | 草图 | 草图转图像 |

## LoRA 适配器

加载经过微调的风格适配器：

```python
from diffusers import DiffusionPipeline

pipe = DiffusionPipeline.from_pretrained(
    "stable-diffusion-v1-5/stable-diffusion-v1-5",
    torch_dtype=torch.float16
).to("cuda")

# Load LoRA weights
pipe.load_lora_weights("path/to/lora", weight_name="style.safetensors")

# Generate with LoRA style
image = pipe("A portrait in the trained style").images[0]

# Adjust LoRA strength
pipe.fuse_lora(lora_scale=0.8)

# Unload LoRA
pipe.unload_lora_weights()
```

### 多个LoRA模型

```python
# Load multiple LoRAs
pipe.load_lora_weights("lora1", adapter_name="style")
pipe.load_lora_weights("lora2", adapter_name="character")

# Set weights for each
pipe.set_adapters(["style", "character"], adapter_weights=[0.7, 0.5])

image = pipe("A portrait").images[0]
```

## 内存优化

### 启用 CPU 卸载功能

```python
# Model CPU offload - moves models to CPU when not in use
pipe.enable_model_cpu_offload()

# Sequential CPU offload - more aggressive, slower
pipe.enable_sequential_cpu_offload()
```

### 注意力切片

```python
# Reduce memory by computing attention in chunks
pipe.enable_attention_slicing()

# Or specific chunk size
pipe.enable_attention_slicing("max")
```

### xFormers高效内存注意力机制

```python
# Requires xformers package
pipe.enable_xformers_memory_efficient_attention()
```

### 大尺寸图像的VAE切片功能

```python
# Decode latents in tiles for large images
pipe.enable_vae_slicing()
pipe.enable_vae_tiling()
```

## 模型版本

### 加载不同精度版本

```python
# FP16 (recommended for GPU)
pipe = DiffusionPipeline.from_pretrained(
    "model-id",
    torch_dtype=torch.float16,
    variant="fp16"
)

# BF16 (better precision, requires Ampere+ GPU)
pipe = DiffusionPipeline.from_pretrained(
    "model-id",
    torch_dtype=torch.bfloat16
)
```

### 加载特定组件

```python
from diffusers import UNet2DConditionModel, AutoencoderKL

# Load custom VAE
vae = AutoencoderKL.from_pretrained("stabilityai/sd-vae-ft-mse")

# Use with pipeline
pipe = DiffusionPipeline.from_pretrained(
    "stable-diffusion-v1-5/stable-diffusion-v1-5",
    vae=vae,
    torch_dtype=torch.float16
)
```

## 批量生成

高效地创建多张图像：

```python
# Multiple prompts
prompts = [
    "A cat playing piano",
    "A dog reading a book",
    "A bird painting a picture"
]

images = pipe(prompts, num_inference_steps=30).images

# Multiple images per prompt
images = pipe(
    "A beautiful sunset",
    num_images_per_prompt=4,
    num_inference_steps=30
).images
```

## 常见工作流程

### 工作流程 1：高质量生成

```python
from diffusers import StableDiffusionXLPipeline, DPMSolverMultistepScheduler
import torch

# 1. Load SDXL with optimizations
pipe = StableDiffusionXLPipeline.from_pretrained(
    "stabilityai/stable-diffusion-xl-base-1.0",
    torch_dtype=torch.float16,
    variant="fp16"
)
pipe.to("cuda")
pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)
pipe.enable_model_cpu_offload()

# 2. Generate with quality settings
image = pipe(
    prompt="A majestic lion in the savanna, golden hour lighting, 8k, detailed fur",
    negative_prompt="blurry, low quality, cartoon, anime, sketch",
    num_inference_steps=30,
    guidance_scale=7.5,
    height=1024,
    width=1024
).images[0]
```

### 工作流 2：快速原型设计

```python
from diffusers import AutoPipelineForText2Image, LCMScheduler
import torch

# Use LCM for 4-8 step generation
pipe = AutoPipelineForText2Image.from_pretrained(
    "stabilityai/stable-diffusion-xl-base-1.0",
    torch_dtype=torch.float16
).to("cuda")

# Load LCM LoRA for fast generation
pipe.load_lora_weights("latent-consistency/lcm-lora-sdxl")
pipe.scheduler = LCMScheduler.from_config(pipe.scheduler.config)
pipe.fuse_lora()

# Generate in ~1 second
image = pipe(
    "A beautiful landscape",
    num_inference_steps=4,
    guidance_scale=1.0
).images[0]
```

## 常见问题

**CUDA 内存不足：**
```python
# Enable memory optimizations
pipe.enable_model_cpu_offload()
pipe.enable_attention_slicing()
pipe.enable_vae_slicing()

# Or use lower precision
pipe = DiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16)
```

**黑色/噪点图像：**
```python
# Check VAE configuration
# Use safety checker bypass if needed
pipe.safety_checker = None

# Ensure proper dtype consistency
pipe = pipe.to(dtype=torch.float16)
```

**生成速度过慢：**
```python
# Use faster scheduler
from diffusers import DPMSolverMultistepScheduler
pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)

# Reduce steps
image = pipe(prompt, num_inference_steps=20).images[0]
```

## 参考资料

- **[高级用法](references/advanced-usage.md)** - 自定义流程、微调及部署
- **[故障排除](references/troubleshooting.md)** - 常见问题与解决方案

## 资源链接

- **文档**：https://huggingface.co/docs/diffusers
- **代码仓库**：https://github.com/huggingface/diffusers
- **模型中心**：https://huggingface.co/models?library=diffusers
- **Discord社区**：https://discord.gg/diffusers
