---
name: gpt-image
description: "Generate and edit images with OpenAI GPT-Image-2.5 and GPT-Image-2 via inference.sh CLI. Models: GPT-Image-2.5 Flare, GPT-Image-2.5 Sunburst, GPT-Image-2. Capabilities: text-to-image, image editing, inpainting, mask-based editing, multi-image reference, batch generation, transparent backgrounds. Use for: product mockups, marketing visuals, image editing, concept art, inpainting, photo manipulation. Triggers: gpt image, gpt-image-2.5, gpt image 2.5, flare, sunburst, gpt-image-2, openai image, chatgpt image, dall-e, dalle, openai image generation, gpt image edit, gpt inpainting, openai dall-e, gpt 4o image, transparent background, transparent png, remove background"
allowed-tools: Bash(belt *)
---

> **Install the belt CLI skill:** `npx skills add belt-sh/cli`

# GPT-Image

Generate and edit images with OpenAI's GPT-Image-2.5 and GPT-Image-2 via [inference.sh](https://inference.sh) CLI.

## Models

| Model | App ID | Pick it for |
|-------|--------|-------------|
| **GPT-Image-2.5 Flare** | `openai/gpt-image-2-5-flare` | Default. Higher quality than GPT-Image-2 at 50% lower latency |
| **GPT-Image-2.5 Sunburst** | `openai/gpt-image-2-5-sunburst` | Premium edits: keeps subject and composition, tighter control across multi-turn edits |
| GPT-Image-2 | `openai/gpt-image-2` | Previous generation |

All three share the same input schema. The 2.5 models add `xhigh` and `max` quality tiers.

## Quick Start

> Requires inference.sh CLI (`belt`). [Install instructions](https://raw.githubusercontent.com/inference-sh/skills/refs/heads/main/cli-install.md)

```bash
belt login

belt app run openai/gpt-image-2-5-flare --input '{"prompt": "a cat astronaut floating in space"}'
```


## Capabilities

Every GPT-Image app supports text-to-image generation, image editing with reference images, and mask-based inpainting through a single app.

| Feature | Description |
|---------|-------------|
| Text-to-Image | Generate images from text prompts |
| Image Editing | Edit images using reference images |
| Inpainting | Mask-based editing of specific regions |
| Batch Generation | Generate up to 10 images at once |
| Multiple Formats | PNG, JPEG, WebP output |
| Transparent Background | Alpha-channel PNG/WebP output for stickers, icons, product cutouts |
| Flexible Resolution | Any size in 16px increments (256–3840), aspect ratio up to 3:1 |

## Examples

### Text-to-Image

```bash
belt app run openai/gpt-image-2-5-flare --input '{
  "prompt": "professional product photo of sneakers on a white background, studio lighting",
  "quality": "high"
}'
```

### Multiple Images

```bash
belt app run openai/gpt-image-2-5-flare --input '{
  "prompt": "minimalist logo design for a coffee shop",
  "n": 4,
  "quality": "medium"
}'
```

### Image Editing with Reference

```bash
belt app run openai/gpt-image-2-5-flare --input '{
  "prompt": "change the background to a beach at sunset",
  "images": ["https://your-image.jpg"]
}'
```

### Precise Edit with Sunburst

Sunburst is built to change only what you ask for and preserve the rest.

```bash
belt app run openai/gpt-image-2-5-sunburst --input '{
  "prompt": "change the jacket to red leather, keep the person, pose and background unchanged",
  "images": ["https://your-photo.jpg"],
  "quality": "high"
}'
```

### Maximum Detail

```bash
belt app run openai/gpt-image-2-5-flare --input '{
  "prompt": "macro photo of a dragonfly wing, intricate veins, morning dew",
  "quality": "max"
}'
```

### Multi-Image Reference

```bash
belt app run openai/gpt-image-2-5-flare --input '{
  "prompt": "combine these two characters into one scene",
  "images": ["https://character1.jpg", "https://character2.jpg"]
}'
```

### Inpainting with Mask

```bash
belt app run openai/gpt-image-2-5-flare --input '{
  "prompt": "replace with a red sports car",
  "images": ["https://street-scene.jpg"],
  "mask": "https://car-mask.png"
}'
```

### Transparent Background

Prompt for an isolated subject — describing a scene or backdrop makes the model draw one. Requires `png` (default) or `webp` output.

```bash
belt app run openai/gpt-image-2-5-flare --input '{
  "prompt": "a single red apple with a green leaf, isolated subject",
  "background": "transparent"
}'
```

### Custom Resolution

```bash
belt app run openai/gpt-image-2-5-flare --input '{
  "prompt": "wide cinematic landscape, mountains at golden hour",
  "width": 1920,
  "height": 1080,
  "quality": "high"
}'
```

### Fast Drafts

```bash
belt app run openai/gpt-image-2-5-flare --input '{
  "prompt": "quick concept sketch of a robot",
  "quality": "low"
}'
```

## Pricing

Approximate price per 1024x1024 image. Flare and Sunburst cost the same.

| Quality | GPT-Image-2.5 | GPT-Image-2 |
|---------|---------------|-------------|
| low | $0.006 | $0.006 |
| medium | $0.013 | $0.053 |
| high | $0.053 | $0.21 |
| xhigh | $0.094 | – |
| max | $0.21 | – |

Larger resolutions cost more. Edits add about $0.008 per reference image. See `belt app get openai/gpt-image-2-5-flare` for full pricing details.

## Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `prompt` | string | required | Text prompt describing the image |
| `images` | array | - | Reference image(s) for editing |
| `mask` | string | - | Mask image for inpainting |
| `n` | integer | 1 | Number of images (1–10) |
| `quality` | string | auto | low, medium, high, xhigh, max (xhigh/max are 2.5 only) |
| `width` | integer | 1024 | Output width (256–3840, multiples of 16, ratio ≤ 3:1) |
| `height` | integer | 1024 | Output height (256–3840, multiples of 16, ratio ≤ 3:1) |
| `output_format` | string | png | png, jpeg, or webp |
| `output_compression` | integer | - | Compression level for jpeg/webp (0–100) |
| `background` | string | auto | auto, transparent, or opaque (transparent needs png/webp) |

## Related Skills

```bash
# Full platform skill (all apps)
npx skills add inference-sh/skills@infsh-cli

# All image generation models
npx skills add inference-sh/skills@ai-image-generation

# FLUX models
npx skills add inference-sh/skills@flux-image

# Pruna P-Image (fast & economical)
npx skills add inference-sh/skills@p-image
```

Browse all image apps: `belt app list --category image`

## Documentation

- [Running Apps](https://inference.sh/docs/apps/running) - How to run apps via CLI
- [Streaming Results](https://inference.sh/docs/api/sdk/streaming) - Real-time progress updates
