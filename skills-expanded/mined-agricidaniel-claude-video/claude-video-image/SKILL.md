---
name: claude-video-image
description: >
  AI image generation for video production using Gemini 3 Pro Image / Nano Banana Pro
  (API, up to 4K, $0.13-0.24/image), FLUX.2 klein 4B (local, sub-second, 13GB VRAM),
  SD 3.5 Medium (local fallback, 6GB), or OpenAI GPT Image 1 Mini API ($0.005/image,
  transparent PNGs). Generates thumbnails, backgrounds, overlays, lower thirds, title
  cards, and B-roll stills at video-native resolutions. Background removal via rembg.
  Use when user says "generate image", "create image", "AI image", "thumbnail",
  "background image", "overlay image", "transparent png", "gemini image", "nano banana",
  "flux", "stable diffusion", "remove background", or "image for video".
allowed-tools:
  - Bash
  - Read
  - Write
---

# claude-video-image — AI Image Generation for Video

## Pre-Flight

1. Activate venv: `source ~/.video-skill/bin/activate`
2. Check free VRAM: `nvidia-smi --query-gpu=memory.free --format=csv,noheader,nounits`
3. Route to local or API based on VRAM availability and user preference

## API Generation (Gemini 3 Pro Image) — Primary

Gemini 3 Pro Image (Nano Banana Pro) — best quality API generation, up to 4K resolution.
Uses Google Search for factual accuracy. Best for photorealistic content and complex prompts.

```bash
source ~/.video-skill/bin/activate
python3 scripts/image_generate.py \
  --api gemini \
  --prompt "Professional marketing dashboard showing SEO metrics, clean modern UI" \
  --resolution 2K \
  --output thumbnail.png
```

**Options:**
- `--api gemini` — Use Gemini 3 Pro Image API (default API)
- `--resolution 1K` — Standard resolution ($0.13/image)
- `--resolution 2K` — High resolution ($0.13/image, default)
- `--resolution 4K` — Ultra resolution ($0.24/image)
- `--aspect RATIO` — Aspect ratio: 1:1, 16:9, 9:16, 4:3, 3:4, 4:5, 5:4, 21:9

Requires `GOOGLE_API_KEY` environment variable.

## Local Generation (FLUX.2 klein 4B) — Free, Fastest

Best local option, free, sub-second generation. Requires 13GB VRAM (or 6GB with quantization).

```bash
source ~/.video-skill/bin/activate
python3 scripts/image_generate.py \
  --prompt "Cinematic wide shot of a futuristic city at sunset, 16:9 aspect ratio" \
  --width 1024 --height 576 \
  --output thumbnail.png
```

**Options:**
- `--model flux` — FLUX.2 klein 4B (default local, 13GB VRAM, <1 second)
- `--model sd35medium` — Stable Diffusion 3.5 Medium (6GB VRAM, ~5-20 seconds)
- `--quantize int8` — Quantize FLUX to ~8GB VRAM (slight quality loss)
- `--steps N` — Inference steps (default: 4 for FLUX, 28 for SD)
- `--seed N` — Reproducible generation
- `--batch N` — Generate N variants (default: 1)

**When to use each:**
- Gemini 3 Pro Image: Best quality, complex prompts, factual content, up to 4K ($0.13-0.24)
- FLUX.2 klein: 13GB+ VRAM free, need speed, no API cost
- SD 3.5 Medium: <13GB VRAM free, or need different aesthetic
- OpenAI GPT Image 1: Need transparent PNG backgrounds

## API Generation (OpenAI GPT Image 1) — For Transparent PNGs

Only option that natively generates transparent PNG backgrounds.

```bash
source ~/.video-skill/bin/activate
python3 scripts/image_generate.py \
  --api openai \
  --prompt "Professional podcast microphone icon on transparent background" \
  --transparent \
  --size 1024x1024 \
  --output overlay.png
```

**Options:**
- `--api openai` — Use OpenAI GPT Image 1 API
- `--quality mini` — GPT Image 1 Mini ($0.005/image, default)
- `--quality medium` — GPT Image 1.5 ($0.034/image)
- `--quality high` — GPT Image 1.5 high ($0.20/image)
- `--transparent` — Transparent background (PNG only)
- `--size WxH` — Output size: 1024x1024, 1536x1024, 1024x1536

Requires `OPENAI_API_KEY` environment variable.

**Cost confirmation:** Always show estimated cost and confirm before API generation.

## Background Removal (rembg)

Strip background from any image to create transparent overlays:

```bash
source ~/.video-skill/bin/activate
python3 scripts/image_generate.py \
  --remove-bg input.png \
  --output transparent.png
```

Uses rembg with u2net_human_seg model (~2GB VRAM with GPU, or CPU fallback). Works with photos, AI-generated images, or any PNG/JPEG.

**Batch mode:**
```bash
python3 scripts/image_generate.py --remove-bg-dir ./images/ --output-dir ./transparent/
```

## Video-Native Dimensions

Always generate at dimensions matching the target video format:

| Use Case | Width | Height | Aspect |
|----------|-------|--------|--------|
| YouTube thumbnail | 1280 | 720 | 16:9 |
| Landscape video frame | 1920 | 1080 | 16:9 |
| Portrait/Shorts | 1080 | 1920 | 9:16 |
| Instagram square | 1080 | 1080 | 1:1 |
| Instagram portrait | 1080 | 1350 | 4:5 |
| Lower third graphic | 1920 | 200 | ~10:1 |
| Title card | 1920 | 1080 | 16:9 |

For FLUX.2 klein, generate at 1024x576 (16:9) or 576x1024 (9:16) then upscale with FFmpeg:
```bash
ffmpeg -n -i generated_1024.png -vf "scale=1920:1080:flags=lanczos" output_1080p.png
```

## Integration with Video Workflow

Generated images can be used as:
- **Overlay input** for the edit sub-skill (`-filter_complex "overlay=X:Y"`)
- **Background** for green screen compositing
- **Thumbnail** alongside exported videos
- **Title card** for Remotion create sub-skill
- **Ken Burns source** for the screenshot sub-skill's animation pipeline

## VRAM Management

- FLUX.2 klein requires 13GB — unload all other GPU models first
- SD 3.5 Medium requires 6GB — can coexist with light models (<5GB)
- rembg requires ~2GB — safe to run alongside medium models
- Script handles loading/unloading automatically via `torch.cuda.empty_cache()`

## Safety Rules

1. Always confirm cost before API image generation
2. Run `bash scripts/preflight.sh` for output path validation
3. Never overwrite existing images without confirmation
4. Report generation time and VRAM usage in output

## Reference

Load `references/image-generation.md` for model details, API parameters, and advanced options.
