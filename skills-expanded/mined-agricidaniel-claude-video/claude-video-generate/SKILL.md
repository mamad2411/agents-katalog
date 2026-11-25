---
name: claude-video-generate
description: >
  AI video generation from text or image prompts using Google Veo 3.1 Fast ($0.15/sec,
  native audio, 8s clips, up to 4K), Runway Gen-4 Turbo ($0.05/sec, silent B-roll, 10s),
  or local Stable Video Diffusion (free, 2-4s). Generates transition clips, B-roll footage,
  animated intros/outros, establishing shots, and image-to-video animations. Use when user
  says "generate video", "AI video", "video from text", "video from image", "B-roll",
  "veo", "runway", "text to video", "image to video", or "create footage".
allowed-tools:
  - Bash
  - Read
  - Write
---

# claude-video-generate — AI Video Generation

> **Tip:** For advanced prompt engineering, Creative Director workflow, image-to-video with
> prompt crafting, domain mode selection, and cost tracking, use the standalone `/veo` skill.
> This sub-skill is a lightweight wrapper for quick generation within video pipelines.

## Pre-Flight

1. Check API keys:
   - `GEMINI_API_KEY` — Required for Google Veo 3.1
   - `RUNWAY_API_KEY` — Required for Runway Gen-4
2. If no API keys available, only local SVD (very limited) is available
3. Always show estimated cost and confirm before API generation

## Google Veo 3.1 — Primary (Best Quality + Audio)

Generates up to 8-second clips with synchronized audio at up to 4K resolution.

```bash
source ~/.video-skill/bin/activate
python3 scripts/video_generate.py \
  --provider veo \
  --prompt "A drone view of the Grand Canyon at sunset with ambient wind sounds" \
  --aspect 16:9 --resolution 1080p \
  --output broll_canyon.mp4
```

**Options:**
- `--provider veo` — Use Google Veo 3.1 Fast
- `--prompt "..."` — Text description of desired video
- `--image ref.png` — Image-to-video (animate a still frame)
- `--aspect 16:9|9:16|1:1` — Aspect ratio
- `--resolution 720p|1080p` — Output resolution
- `--tier fast|standard` — Fast ($0.15/sec, 2-5 min gen) or Standard ($0.40/sec, 5-12 min gen)
- `--output clip.mp4` — Output path

**Pricing:**
- Veo 3.1 Fast: $0.15/sec x 8s = **$1.20 per clip**
- Veo 3.1 Standard: $0.40/sec x 8s = **$3.20 per clip**

**Features:**
- Native synchronized audio (dialogue, SFX, ambient sounds)
- Text-to-video and image-to-video
- Video extension (chain up to 20 extensions for ~148s total)
- Up to 4K resolution

**Generation time:** 2-5 minutes (Fast), 5-12 minutes (Standard). Script polls with progress.

## Runway Gen-4 Turbo — Budget B-Roll

Fastest and cheapest for silent B-roll footage.

```bash
source ~/.video-skill/bin/activate
python3 scripts/video_generate.py \
  --provider runway \
  --prompt "Smooth camera pan across a modern office workspace" \
  --duration 10 \
  --output broll_office.mp4
```

**Options:**
- `--provider runway` — Use Runway Gen-4 Turbo
- `--prompt "..."` — Text description
- `--image ref.png` — Image-to-video
- `--duration 5|10` — Clip duration in seconds (max 10)
- `--output clip.mp4` — Output path

**Pricing:** $0.05/sec x 10s = **$0.50 per clip**

**Limitations:**
- No audio output (silent video only)
- Max 1080p resolution
- Max 10 seconds per generation

**Best for:** Placeholder B-roll, transitions, background footage where audio isn't needed.

## Local SVD-XT — Free but Limited

Generates 2-4 second clips from a source image. No text-to-video.

```bash
source ~/.video-skill/bin/activate
python3 scripts/video_generate.py \
  --provider local \
  --image source_frame.png \
  --output motion.mp4
```

**Limitations:**
- Image-to-video only (no text-to-video)
- 2-4 second clips maximum
- 1024x576 resolution
- Requires 16GB VRAM (exclusive use)
- 2-25 minutes generation time
- No audio

**Best for:** Subtle motion effects from still images when no API keys available.

## Video Extension (Veo Only)

Extend an existing generated clip:

```bash
python3 scripts/video_generate.py \
  --provider veo \
  --extend existing_clip.mp4 \
  --prompt "Continue the camera movement, revealing the cityscape below" \
  --output extended_clip.mp4
```

Can chain up to 20 extensions (8s each = ~148s total). Each extension costs $1.20 (Fast).

## Fallback Chain

```
1. Veo 3.1 Fast  → Best quality, native audio ($1.20/clip)
2. Runway Gen-4  → Budget silent B-roll ($0.50/clip)
3. Local SVD-XT  → Free, image-to-video only, 2-4s, degraded quality
4. Remotion      → Programmatic motion graphics (existing create sub-skill)
```

## Cost Confirmation Protocol

Before ANY API generation, display and confirm:

```
Provider: Google Veo 3.1 Fast
Duration: 8 seconds
Resolution: 1080p
Estimated cost: $1.20
Proceed? (y/n)
```

Never generate without explicit user confirmation for paid API calls.

## Output Format

All generated videos are MP4 with H.264 codec. The script runs ffprobe on the output and returns JSON metadata including resolution, duration, codec, and file size.

## Safety Rules

1. Always confirm API costs before generation
2. Run `bash scripts/preflight.sh` for output path validation
3. Track cumulative API costs across multiple generations in a session
4. Warn if total session cost exceeds $10
5. For batch generation, show total estimated cost upfront

## Reference

Load `references/video-generation.md` for API setup, polling patterns, cost formulas, and emerging models.
