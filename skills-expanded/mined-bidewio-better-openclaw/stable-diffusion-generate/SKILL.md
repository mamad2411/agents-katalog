---
name: stable-diffusion-generate
description: "Generate images from text prompts using Stable Diffusion at {{SD_HOST}}:{{SD_PORT}}."
metadata:
  openclaw:
    emoji: "🖼️"
---

# Stable Diffusion Image Generation

Stable Diffusion is available at `http://{{SD_HOST}}:{{SD_PORT}}` within the Docker network.

## Generate an Image

```bash
curl -X POST "http://{{SD_HOST}}:{{SD_PORT}}/sdapi/v1/txt2img" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "a futuristic city at sunset, detailed, 8k",
    "negative_prompt": "blurry, low quality",
    "steps": 30,
    "width": 1024,
    "height": 1024,
    "cfg_scale": 7
  }'
```

## Image-to-Image

```bash
curl -X POST "http://{{SD_HOST}}:{{SD_PORT}}/sdapi/v1/img2img" \
  -H "Content-Type: application/json" \
  -d '{"init_images": ["base64_encoded_image"], "prompt": "oil painting style", "denoising_strength": 0.7}'
```

## Tips for AI Agents

- The response contains base64-encoded images — decode and save to files.
- Use negative prompts to exclude unwanted elements.
- Higher step counts produce better quality but take longer.
- GPU acceleration is highly recommended for reasonable generation times.
