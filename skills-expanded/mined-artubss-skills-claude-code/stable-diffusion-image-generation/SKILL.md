---
name: stable-diffusion-image-generation
description: Geração de imagens com tecnologia de ponta usando Stable Diffusion via HuggingFace Diffusers. Use quando gerar imagens a partir de prompts em texto, realizar tradução de imagem para imagem, inpainting ou construir pipelines de difusão customizados.
version: 1.0.0
author: Orchestra Research
license: MIT
tags: [Image Generation, Stable Diffusion, Diffusers, Text-to-Image, Multimodal, Computer Vision]
dependencies: [diffusers>=0.30.0, transformers>=4.41.0, accelerate>=0.31.0, torch>=2.0.0]
---

# Geração de Imagens com Stable Diffusion

Guia completo para gerar imagens com Stable Diffusion usando a biblioteca HuggingFace Diffusers.

## Quando usar Stable Diffusion

**Use Stable Diffusion quando:**
- Gerar imagens a partir de descrições em texto
- Realizar tradução de imagem para imagem (transferência de estilo, aprimoramento)
- Inpainting (preenchimento de regiões mascaradas)
- Outpainting (extensão de imagens além de limites)
- Criar variações de imagens existentes
- Construir workflows customizados de geração de imagens

**Principais características:**
- **Text-to-Image**: Gere imagens a partir de prompts em linguagem natural
- **Image-to-Image**: Transforme imagens existentes com orientação em texto
- **Inpainting**: Preencha regiões mascaradas com conteúdo contextual
- **ControlNet**: Adicione conditioning espacial (bordas, poses, profundidade)
- **Suporte a LoRA**: Fine-tuning eficiente e adaptação de estilo
- **Múltiplos Modelos**: Suporte para SD 1.5, SDXL, SD 3.0, Flux

**Use alternativas em vez disso:**
- **DALL-E 3**: Para geração via API sem GPU
- **Midjourney**: Para outputs artísticos e estilizados
- **Imagen**: Para integração com Google Cloud
- **Leonardo.ai**: Para workflows criativos baseados na web

## Início rápido

### Instalação

```bash
pip install diffusers transformers accelerate torch
pip install xformers  # Opcional: atenção eficiente em memória
```

### Text-to-image básico

```python
from diffusers import DiffusionPipeline
import torch

# Carregue o pipeline (detecta tipo de modelo automaticamente)
pipe = DiffusionPipeline.from_pretrained(
    "stable-diffusion-v1-5/stable-diffusion-v1-5",
    torch_dtype=torch.float16
)
pipe.to("cuda")

# Gere imagem
image = pipe(
    "A serene mountain landscape at sunset, highly detailed",
    num_inference_steps=50,
    guidance_scale=7.5
).images[0]

image.save("output.png")
```

### Usando SDXL (qualidade superior)

```python
from diffusers import AutoPipelineForText2Image
import torch

pipe = AutoPipelineForText2Image.from_pretrained(
    "stabilityai/stable-diffusion-xl-base-1.0",
    torch_dtype=torch.float16,
    variant="fp16"
)
pipe.to("cuda")

# Ative otimização de memória
pipe.enable_model_cpu_offload()

image = pipe(
    prompt="A futuristic city with flying cars, cinematic lighting",
    height=1024,
    width=1024,
    num_inference_steps=30
).images[0]
```

## Visão geral da arquitetura

### Design de três pilares

Diffusers é construído em torno de três componentes principais:

```
Pipeline (orchestration)
├── Model (neural networks)
│   ├── UNet / Transformer (noise prediction)
│   ├── VAE (latent encoding/decoding)
│   └── Text Encoder (CLIP/T5)
└── Scheduler (denoising algorithm)
```

### Fluxo de inferência do pipeline

```
Text Prompt → Text Encoder → Text Embeddings
                                    ↓
Random Noise → [Denoising Loop] ← Scheduler
                      ↓
               Predicted Noise
                      ↓
              VAE Decoder → Final Image
```

## Conceitos principais

### Pipelines

Os pipelines orquestram workflows completos:

| Pipeline | Propósito |
|----------|-----------|
| `StableDiffusionPipeline` | Text-to-image (SD 1.x/2.x) |
| `StableDiffusionXLPipeline` | Text-to-image (SDXL) |
| `StableDiffusion3Pipeline` | Text-to-image (SD 3.0) |
| `FluxPipeline` | Text-to-image (modelos Flux) |
| `StableDiffusionImg2ImgPipeline` | Image-to-image |
| `StableDiffusionInpaintPipeline` | Inpainting |

### Schedulers

Os schedulers controlam o processo de denoising:

| Scheduler | Passos | Qualidade | Caso de Uso |
|-----------|--------|-----------|------------|
| `EulerDiscreteScheduler` | 20-50 | Bom | Escolha padrão |
| `EulerAncestralDiscreteScheduler` | 20-50 | Bom | Mais variação |
| `DPMSolverMultistepScheduler` | 15-25 | Excelente | Rápido, alta qualidade |
| `DDIMScheduler` | 50-100 | Bom | Determinístico |
| `LCMScheduler` | 4-8 | Bom | Muito rápido |
| `UniPCMultistepScheduler` | 15-25 | Excelente | Convergência rápida |

### Troca de schedulers

```python
from diffusers import DPMSolverMultistepScheduler

# Troque para geração mais rápida
pipe.scheduler = DPMSolverMultistepScheduler.from_config(
    pipe.scheduler.config
)

# Agora gere com menos passos
image = pipe(prompt, num_inference_steps=20).images[0]
```

## Parâmetros de geração

### Parâmetros principais

| Parâmetro | Padrão | Descrição |
|-----------|--------|-----------|
| `prompt` | Obrigatório | Descrição em texto da imagem desejada |
| `negative_prompt` | None | O que evitar na imagem |
| `num_inference_steps` | 50 | Passos de denoising (mais = melhor qualidade) |
| `guidance_scale` | 7.5 | Aderência ao prompt (7-12 típico) |
| `height`, `width` | 512/1024 | Dimensões de saída (múltiplos de 8) |
| `generator` | None | Gerador Torch para reprodutibilidade |
| `num_images_per_prompt` | 1 | Tamanho do lote |

### Geração reprodutível

```python
import torch

generator = torch.Generator(device="cuda").manual_seed(42)

image = pipe(
    prompt="A cat wearing a top hat",
    generator=generator,
    num_inference_steps=50
).images[0]
```

### Prompts negativos

```python
image = pipe(
    prompt="Professional photo of a dog in a garden",
    negative_prompt="blurry, low quality, distorted, ugly, bad anatomy",
    guidance_scale=7.5
).images[0]
```

## Image-to-image

Transforme imagens existentes com orientação em texto:

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
    strength=0.75,  # Quanto transformar (0-1)
    num_inference_steps=50
).images[0]
```

## Inpainting

Preencha regiões mascaradas:

```python
from diffusers import AutoPipelineForInpainting
from PIL import Image

pipe = AutoPipelineForInpainting.from_pretrained(
    "runwayml/stable-diffusion-inpainting",
    torch_dtype=torch.float16
).to("cuda")

image = Image.open("photo.jpg")
mask = Image.open("mask.png")  # Branco = região para inpainting

result = pipe(
    prompt="A red car parked on the street",
    image=image,
    mask_image=mask,
    num_inference_steps=50
).images[0]
```

## ControlNet

Adicione conditioning espacial para controle preciso:

```python
from diffusers import StableDiffusionControlNetPipeline, ControlNetModel
import torch

# Carregue ControlNet para conditioning de bordas
controlnet = ControlNetModel.from_pretrained(
    "lllyasviel/control_v11p_sd15_canny",
    torch_dtype=torch.float16
)

pipe = StableDiffusionControlNetPipeline.from_pretrained(
    "stable-diffusion-v1-5/stable-diffusion-v1-5",
    controlnet=controlnet,
    torch_dtype=torch.float16
).to("cuda")

# Use imagem de borda Canny como controle
control_image = get_canny_image(input_image)

image = pipe(
    prompt="A beautiful house in the style of Van Gogh",
    image=control_image,
    num_inference_steps=30
).images[0]
```

### ControlNets disponíveis

| ControlNet | Tipo de Entrada | Caso de Uso |
|------------|-----------------|------------|
| `canny` | Mapas de borda | Preservar estrutura |
| `openpose` | Esqueletos de pose | Poses humanas |
| `depth` | Mapas de profundidade | Geração 3D-aware |
| `normal` | Mapas normais | Detalhes de superfície |
| `mlsd` | Segmentos de linha | Linhas arquitetônicas |
| `scribble` | Esboços aproximados | Sketch-to-image |

## Adaptadores LoRA

Carregue adaptadores de estilo fine-tuned:

```python
from diffusers import DiffusionPipeline

pipe = DiffusionPipeline.from_pretrained(
    "stable-diffusion-v1-5/stable-diffusion-v1-5",
    torch_dtype=torch.float16
).to("cuda")

# Carregue pesos LoRA
pipe.load_lora_weights("path/to/lora", weight_name="style.safetensors")

# Gere com estilo LoRA
image = pipe("A portrait in the trained style").images[0]

# Ajuste força LoRA
pipe.fuse_lora(lora_scale=0.8)

# Descarregue LoRA
pipe.unload_lora_weights()
```

### Múltiplos LoRAs

```python
# Carregue múltiplos LoRAs
pipe.load_lora_weights("lora1", adapter_name="style")
pipe.load_lora_weights("lora2", adapter_name="character")

# Defina pesos para cada um
pipe.set_adapters(["style", "character"], adapter_weights=[0.7, 0.5])

image = pipe("A portrait").images[0]
```

## Otimização de memória

### Ative CPU offloading

```python
# Model CPU offload - move modelos para CPU quando não em uso
pipe.enable_model_cpu_offload()

# Sequential CPU offload - mais agressivo, mais lento
pipe.enable_sequential_cpu_offload()
```

### Attention slicing

```python
# Reduza memória computando atenção em chunks
pipe.enable_attention_slicing()

# Ou tamanho específico de chunk
pipe.enable_attention_slicing("max")
```

### xFormers atenção eficiente em memória

```python
# Requer pacote xformers
pipe.enable_xformers_memory_efficient_attention()
```

### VAE slicing para imagens grandes

```python
# Decodifique latents em tiles para imagens grandes
pipe.enable_vae_slicing()
pipe.enable_vae_tiling()
```

## Variantes de modelo

### Carregamento de diferentes precisões

```python
# FP16 (recomendado para GPU)
pipe = DiffusionPipeline.from_pretrained(
    "model-id",
    torch_dtype=torch.float16,
    variant="fp16"
)

# BF16 (melhor precisão, requer GPU Ampere+)
pipe = DiffusionPipeline.from_pretrained(
    "model-id",
    torch_dtype=torch.bfloat16
)
```

### Carregamento de componentes específicos

```python
from diffusers import UNet2DConditionModel, AutoencoderKL

# Carregue VAE customizado
vae = AutoencoderKL.from_pretrained("stabilityai/sd-vae-ft-mse")

# Use com pipeline
pipe = DiffusionPipeline.from_pretrained(
    "stable-diffusion-v1-5/stable-diffusion-v1-5",
    vae=vae,
    torch_dtype=torch.float16
)
```

## Geração em lote

Gere múltiplas imagens de forma eficiente:

```python
# Múltiplos prompts
prompts = [
    "A cat playing piano",
    "A dog reading a book",
    "A bird painting a picture"
]

images = pipe(prompts, num_inference_steps=30).images

# Múltiplas imagens por prompt
images = pipe(
    "A beautiful sunset",
    num_images_per_prompt=4,
    num_inference_steps=30
).images
```

## Workflows comuns

### Workflow 1: Geração de alta qualidade

```python
from diffusers import StableDiffusionXLPipeline, DPMSolverMultistepScheduler
import torch

# 1. Carregue SDXL com otimizações
pipe = StableDiffusionXLPipeline.from_pretrained(
    "stabilityai/stable-diffusion-xl-base-1.0",
    torch_dtype=torch.float16,
    variant="fp16"
)
pipe.to("cuda")
pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)
pipe.enable_model_cpu_offload()

# 2. Gere com configurações de qualidade
image = pipe(
    prompt="A majestic lion in the savanna, golden hour lighting, 8k, detailed fur",
    negative_prompt="blurry, low quality, cartoon, anime, sketch",
    num_inference_steps=30,
    guidance_scale=7.5,
    height=1024,
    width=1024
).images[0]
```

### Workflow 2: Prototipagem rápida

```python
from diffusers import AutoPipelineForText2Image, LCMScheduler
import torch

# Use LCM para geração em 4-8 passos
pipe = AutoPipelineForText2Image.from_pretrained(
    "stabilityai/stable-diffusion-xl-base-1.0",
    torch_dtype=torch.float16
).to("cuda")

# Carregue LCM LoRA para geração rápida
pipe.load_lora_weights("latent-consistency/lcm-lora-sdxl")
pipe.scheduler = LCMScheduler.from_config(pipe.scheduler.config)
pipe.fuse_lora()

# Gere em ~1 segundo
image = pipe(
    "A beautiful landscape",
    num_inference_steps=4,
    guidance_scale=1.0
).images[0]
```

## Problemas comuns

**CUDA sem memória:**
```python
# Ative otimizações de memória
pipe.enable_model_cpu_offload()
pipe.enable_attention_slicing()
pipe.enable_vae_slicing()

# Ou use precisão menor
pipe = DiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16)
```

**Imagens pretas/ruidosas:**
```python
# Verifique configuração VAE
# Use safety checker bypass se necessário
pipe.safety_checker = None

# Garanta consistência de dtype
pipe = pipe.to(dtype=torch.float16)
```

**Geração lenta:**
```python
# Use scheduler mais rápido
from diffusers import DPMSolverMultistepScheduler
pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)

# Reduza passos
image = pipe(prompt, num_inference_steps=20).images[0]
```

## Referências

- **[Uso Avançado](references/advanced-usage.md)** - Pipelines customizados, fine-tuning, deploy
- **[Solução de Problemas](references/troubleshooting.md)** - Problemas comuns e soluções

## Recursos

- **Documentação**: https://huggingface.co/docs/diffusers
- **Repositório**: https://github.com/huggingface/diffusers
- **Model Hub**: https://huggingface.co/models?library=diffusers
- **Discord**: https://discord.gg/diffusers