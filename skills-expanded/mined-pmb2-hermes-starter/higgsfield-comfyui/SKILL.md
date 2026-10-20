---
name: higgsfield-comfyui
description: Transform local ComfyUI into a Higgsfield-class video generation platform with automatic cloud overflow (fal.ai) for heavy workloads
version: 1.2.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [higgsfield, comfyui, video-generation, face-swap, cloud-gpu, fal-ai, wan]
    triggers: [higgsfield, comfyui, video-generation, face-swap, cloud-gpu, fal-ai, wan-video, animatediff, video-pipeline, comfyui-cloud-overflow]
    related_skills: [comfyui, fal-ai-integration, genmedia, ai-video-pipeline]
---

# Higgsfield — ComfyUI Generation Platform

Turns your local ComfyUI into a full-featured video generation platform comparable to Higgsfield.ai, but cheaper and with full flexibility.

## Architecture

```
┌─────────────┐     Local GPU (RTX 3090 24GB)
│  higgsfield │     ┌─────────────────────────┐
│  .py script │────▶│  ComfyUI (Docker)        │
│             │     │  - AnimateDiff (video)   │
│  CLI args:  │     │  - Wan2.1 (T2V + I2V)   │
│  --mode     │     │  - Hunyuan (video)       │
│  --prompt   │     │  - IP-Adapter (char)     │
│  --workflow │     │  - InstantID (face ID)   │
│  --cloud    │     │  - fal-Connector (cloud) │
└──────┬──────┘     └──────────┬──────────────┘
       │                       │
       │         Cloud GPU     ▼
       │         ┌─────────────────────────┐
       └────────▶│  fal.ai (RTX 6000 Pro)  │
                  │  - When VRAM > 18GB     │
                  │  - Force with --cloud   │
                  └─────────────────────────┘
```

## User Preferences (Critical)

- **NO Ken Burns / zoom-pan effects** — explicitly rejected as "cheap and looks bad like a slideshow." All video output must use real video generation (Wan2.1 I2V, AnimateDiff, etc.). Never use ffmpeg zoompan or setpts-based Ken Burns as the primary animation method.

## Scene-Based Video Pipeline

For narrative videos with voiceover, use this proven architecture:

```
Script (30+ scenes)
  → Per-scene FLUX image generation (4-5 images, text-to-image, local GPU)
  → Wan2.1 Image-to-Video (best FLUX image → 81-frame video clip, 832x480, local GPU)
  → Speed-ramp each clip to align with scene narration timing
  → Concat all scene clips → overlay TTS audio → final MP4
```

Key design decisions:
- **FLUX** for stills (SOTA for MS Paint style, local RTX 3090)
- **Wan2.1 I2V** for video clips (real motion, NOT Ken Burns)
- **Speed ramping** (ffmpeg setpts) to match scene duration — slow down or speed up video
- **Never freeze-frame or zoom-pan** as a timing fill — pad with slowed video or cut scene shorter
- Assembly via ffmpeg concat demuxer (not xfade which crashes on gyan.dev Windows builds)

Pipeline scripts:
- `run_scene_pipeline.py` — orchestrator (generate + assemble)
- `scripts/pipeline_utils.py` — ComfyUI submission, I2V generation, ffmpeg helpers
- `scripts/scene_generator.py` — per-scene FLUX + I2V generation with checkpointing
- `scripts/scene_assembler.py` — speed-ramped I2V clip assembly with TTS overlay

## higgsfield.py CLI

**`scripts/higgsfield.py`** — Main CLI tool:
- Auto-detects VRAM → routes to local or cloud
- Supports video gen, character consistency, face swap, upscale

```bash
# Check VRAM status
python3 scripts/higgsfield.py vram

# Generate video (auto-routes based on VRAM)
python3 scripts/higgsfield.py video --prompt "cinematic drone shot of a city" --workflow wan_t2v

# Force cloud GPU for heavy workloads
python3 scripts/higgsfield.py video --prompt "..." --cloud

# Character-consistent generation
python3 scripts/higgsfield.py character --prompt "a person smiling" --reference ref.jpg
```

## Setup

1. Get a fal.ai API key: https://fal.ai/dashboard → API Keys
2. Add to Hermes `.env`: `FAL_KEY=fal-xxxxxxxxxxxx`
3. Restart the ComfyUI Docker container to pick up env vars

## Workflows

Export from ComfyUI web UI (Workflow → Export API) to:
`~/higgsfield_workflows/`

Required workflow files:
- `wan_text_to_video.json` — Wan2.1 text-to-video
- `wan_image_to_video.json` — Wan2.1 image-to-video  
- `animatediff_video.json` — AnimateDiff
- `hunyuan_video.json` — Hunyuan
- `character_consistency.json` — IP-Adapter + InstantID
- `face_swap.json` — Face swap
- `upscale.json` — Upscale + detail

## Recommended Video Models (download)

**Important**: The Kijai/WanVideo_comfy repo does NOT have a 1.3B I2V model. The smallest I2V variant is 14B at fp8 quantization (~17GB). For local I2V on RTX 3090 24GB, use the 14B fp8 model with `WanVideoBlockSwap` to offload transformer blocks to CPU as needed.

```bash
# --- Wan2.1 I2V 14B fp8 (fits RTX 3090 with block swap) ---
# Models go in the comfyui-models Docker volume:
#   text_encoders/ → /workspace/ComfyUI/models/text_encoders/
#   diffusion_models/ → /workspace/ComfyUI/models/diffusion_models/
#   vae/ → /workspace/ComfyUI/models/vae/

# Inside the comfyui container:
docker exec yt-anim-comfyui bash -c '
  HF_BASE="https://huggingface.co/Kijai/WanVideo_comfy/resolve/main"
  MODELS=/workspace/ComfyUI/models
  
  # VAE (~243MB)
  curl -L -o "$MODELS/vae/Wan2_1_VAE_bf16.safetensors" \
    "$HF_BASE/Wan2_1_VAE_bf16.safetensors"
  
  # T5 text encoder (~11GB)
  curl -L -o "$MODELS/text_encoders/umt5-xxl-enc-bf16.safetensors" \
    "$HF_BASE/umt5-xxl-enc-bf16.safetensors"
  
  # I2V 14B fp8 model (~17GB) — the primary I2V model
  curl -L -o "$MODELS/diffusion_models/Wan2_1-I2V-14B-480P_fp8_e4m3fn.safetensors" \
    "$HF_BASE/Wan2_1-I2V-14B-480P_fp8_e4m3fn.safetensors"
'

# Alternative: use hf CLI (huggingface-cli is deprecated)
docker exec yt-anim-comfyui bash -c '
  MODELS=/workspace/ComfyUI/models
  hf download Kijai/WanVideo_comfy Wan2_1_VAE_bf16.safetensors \
    --local-dir "$MODELS/vae"
  hf download Kijai/WanVideo_comfy umt5-xxl-enc-bf16.safetensors \
    --local-dir "$MODELS/text_encoders"
  hf download Kijai/WanVideo_comfy Wan2_1-I2V-14B-480P_fp8_e4m3fn.safetensors \
    --local-dir "$MODELS/diffusion_models"
'
```

## Wan2.1 I2V Workflow (API format)

The I2V pipeline uses these ComfyUI nodes in `workflows/wan_i2v_1_3B.json`:

1. **LoadImage** — FLUX-generated input image
2. **LoadWanVideoT5TextEncoder** — umt5-xxl-enc-bf16.safetensors
3. **WanVideoModelLoader** — Wan2_1-I2V-14B-480P_fp8_e4m3fn.safetensors (14B fp8, the smallest available I2V model in Kijai/WanVideo_comfy)
3. **WanVideoModelLoader** — Wan2_1-I2V-14B-480P_fp8_e4m3fn.safetensors (14B fp8, the smallest available I2V model in Kijai/WanVideo_comfy)
5. **CLIPVisionLoader** — clip_vision_h.safetensors (models/clip-vit-large-patch14/ has this)
6. **WanVideoClipVisionEncode** — encodes image for I2V conditioning
7. **WanVideoTextEncode** — positive + negative prompt encoding
8. **WanVideoImageToVideoEncode** — width/height/num_frames parameters
9. **WanVideoSampler** — dpm++_sde scheduler, euler sampler
10. **WanVideoDecode** — decode latents
11. **VHS_VideoCombine** — outputs video to ComfyUI output directory

Important: VHS_VideoCombine is an OUTPUT_NODE with RETURN_TYPES=("VHS_FILENAMES",). The video file is saved to the Docker volume's output directory, NOT returned as a standard image. Use `docker cp` or find recent files in `/workspace/ComfyUI/output/` after completion.

Wan2.1 I2V models auto-detect type from state dict keys — no need to set model_type manually. 1.3B models have 30 transformer blocks, 14B models have 40.

## Cost Comparison

| Service | 1 min video | Flex | Our Setup |
|---------|------------|------|-----------|
| Higgsfield | $5-10/mo sub + per-gen | Limited | **$0 flat** (own GPU) |
| RunPod | $0.50-2/hr rental | Full | Free for local fits |
| fal.ai overflow | $0.10-0.50/gen | Full | Only when VRAM full |
| **Our setup** | **$0 local / ~$0.30 cloud** | **Full optionality** | **Best of both** |

## Reference Files

| File | What it covers |
|------|---------------|
| `references/docker-node-install.md` | Installing custom nodes inside Docker when git clone fails (auth/credential issues) |
| `references/docker-persistence.md` | Docker persistence: custom nodes + pip deps wiped on recreate, bootstrap.sh pattern, env var pass-through |
| `references/wan-i2v-local-pipeline.md` | Full Wan2.1 I2V pipeline: model files, workflow architecture, resolution limits, ComfyUI submission flow |

## Pitfalls

- **Docker git clone fails** — git clone inside the container errors "could not read Username for https://github.com" because the container has no credential helper. Use Python urllib + zipfile as workaround (see `references/docker-node-install.md`).
- **Custom nodes + pip deps don't survive `docker compose down`** — container recreates start from the base image. Use a bootstrap script mounted via volume (see `references/docker-persistence.md`). The bootstrap runs on every `docker compose up` and re-installs nodes + deps.
- **Docker env vars** — FAL_KEY must be in a `.env` file in the docker-compose project directory, or wired via `environment:` in docker-compose.yml. Hermes `.env` does NOT pass through to Docker containers.
- **fal-Connector auth chain** — reads from: (1) fal_client credentials file, (2) FAL_KEY env var, (3) fal-config.ini. Setting FAL_KEY env var is most reliable.
- **VRAM detection** — routes to cloud when >18GB in use. On Windows WDDM, Docker Desktop + browser tabs consume 4-6GB before ComfyUI starts. Check with `python3 scripts/higgsfield.py vram`.
- **Workflow param injection** — matches parameter names across node inputs. Open workflow JSON and check actual inputs field names if params aren't sticking.
- **VHS_VideoCombine output is NOT an image type** — it returns `VHS_FILENAMES`, not images. After the workflow completes, find the video file at `/workspace/ComfyUI/output/` with `find -name "*<prefix>*" -mmin -5`. Use `docker cp yt-anim-comfyui:/workspace/ComfyUI/output/<filename> <dest>` to retrieve it.
- **`huggingface-cli` is deprecated** — the container ships `hf` CLI instead. Use `hf download <repo> <file> --local-dir <dir>` or fall back to direct curl from `https://huggingface.co/Kijai/WanVideo_comfy/resolve/main/<filename>`.
- **Freeze-frame padding is not acceptable** — when a video clip is shorter than the scene narration, slow it down (ffmpeg setpts) rather than adding a static freeze frame. The user considers freeze-frames and Ken Burns effects "cheap slideshow."
- **I2V model download timeout** — large models (10GB+ T5 encoder) may timeout via `hf download`. Use `curl -L -o` with background=true + notify_on_complete for reliable multi-GB downloads. Speed typical: 10-12 MB/s on gigabit.