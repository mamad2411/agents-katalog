---
name: claude-video-enhance
description: >
  AI video enhancement using Real-ESRGAN (4x upscaling, 720p to 4K, 2-6GB VRAM),
  Practical-RIFE (frame interpolation for smooth slow motion, 60+ FPS at 720p),
  CodeFormer (face restoration for old/low-quality footage, adjustable fidelity),
  and rembg (transparent video via background removal, VP9+alpha or ProRes 4444).
  Use when user says "upscale", "enhance video", "4K", "super resolution",
  "frame interpolation", "slow motion AI", "smooth slow motion", "restore faces",
  "fix faces", "remove video background", "transparent video", "increase resolution",
  or "improve quality".
allowed-tools:
  - Bash
  - Read
  - Write
---

# claude-video-enhance — AI Video Enhancement

## Pre-Flight

1. Activate venv: `source ~/.video-skill/bin/activate`
2. Check free VRAM: `nvidia-smi --query-gpu=memory.free --format=csv,noheader,nounits`
3. Get input video info: `ffprobe -v quiet -print_format json -show_streams "$INPUT"`
4. Estimate processing time and disk space (frame-based pipelines are slow and large)
5. **Always warn the user** about expected processing time before starting

## AI Upscaling (Real-ESRGAN)

Upscale video resolution by 2x or 4x using AI super-resolution.

```bash
source ~/.video-skill/bin/activate
python3 scripts/video_enhance.py upscale "$INPUT" \
  --scale 4 \
  --output upscaled_4k.mp4
```

**Options:**
- `--scale 2|4` — Upscale factor (default: 4)
- `--model realesrgan-x4plus` — General purpose model (default)
- `--model realesrgan-x4plus-anime` — Optimized for anime/cartoon content
- `--half` — Use FP16 precision (faster, less VRAM, recommended)
- `--output FILE` — Output path
- `--codec h264|hevc|av1` — Output codec (default: h264_nvenc if available)

**VRAM:** 2-6GB with `--half` flag

**Performance expectations:**
- 720p → 4K (4x): 2-5 FPS → 10 min video (18,000 frames) takes ~1-2.5 hours
- 1080p → 4K (2x): 1-3 FPS → expect even longer

**Pipeline:**
1. Extract all frames to temp directory (large disk usage: ~5x input size)
2. Upscale each frame with Real-ESRGAN (GPU)
3. Extract audio from original video
4. Reassemble upscaled frames + audio into output video
5. Clean up temp frames

**Disk space warning:** A 10-minute 30fps video creates 18,000 PNG frames. At 4K, each frame is ~10-20MB. Total temp space: 180-360GB. Ensure sufficient disk space.

## Frame Interpolation (Practical-RIFE)

Create smooth slow motion by generating intermediate frames.

```bash
source ~/.video-skill/bin/activate
python3 scripts/video_enhance.py interpolate "$INPUT" \
  --multi 2 \
  --output smooth_slowmo.mp4
```

**Options:**
- `--multi 2|4|8` — Frame multiplication factor (default: 2)
  - 2x: 30fps → 60fps, or half-speed smooth slow motion
  - 4x: 30fps → 120fps, or quarter-speed smooth slow motion
  - 8x: 30fps → 240fps, extreme slow motion
- `--output FILE` — Output path
- `--fps-target N` — Instead of multiplier, set target FPS

**VRAM:** 2-4GB

**Performance:** 60+ FPS for 2x interpolation at 720p. Slower at higher resolutions.

**Use cases:**
- Convert 30fps to 60fps for smoother playback
- Create cinematic slow motion from normal-speed footage
- Smooth out choppy screen recordings

## Face Restoration (CodeFormer)

Restore degraded faces in old or low-quality video footage.

```bash
source ~/.video-skill/bin/activate
python3 scripts/video_enhance.py restore-faces "$INPUT" \
  --fidelity 0.7 \
  --output restored.mp4
```

**Options:**
- `--fidelity 0.0-1.0` — Quality-fidelity balance (default: 0.7)
  - 0.0 = Most beautiful (more hallucinated/enhanced)
  - 0.5 = Balanced
  - 0.7 = Recommended (good quality while staying faithful)
  - 1.0 = Most faithful to original (minimal enhancement)
- `--bg-upscale` — Also upscale background with Real-ESRGAN
- `--output FILE` — Output path

**VRAM:** 2-4GB (CodeFormer) + 2-4GB if `--bg-upscale` enabled

**Pipeline:**
1. Extract frames
2. Detect faces in each frame
3. Restore each detected face with CodeFormer
4. Optionally upscale background
5. Reassemble with audio

**Best for:** Old family videos, low-resolution webcam footage, compressed video with face artifacts.

## Background Removal (rembg)

Remove background from video to create transparent video.

```bash
source ~/.video-skill/bin/activate
python3 scripts/video_enhance.py remove-bg "$INPUT" \
  --format webm \
  --output transparent.webm
```

**Options:**
- `--format webm` — VP9 with alpha channel (for web, default)
- `--format prores` — ProRes 4444 with alpha (for editing workflows)
- `--model u2net_human_seg` — Optimized for humans (default)
- `--model u2net` — General purpose (any subject)
- `--model isnet-general-use` — Alternative general model
- `--output FILE` — Output path

**VRAM:** 1-2GB (GPU) or CPU fallback

**Performance:** 5-10 FPS for 1080p

**Output formats:**
- WebM (VP9+alpha): `ffmpeg -c:v libvpx-vp9 -pix_fmt yuva420p output.webm`
- ProRes 4444: `ffmpeg -c:v prores_ks -profile:v 4 -pix_fmt yuva444p10le output.mov`

## Combined Enhancement Pipeline

Chain multiple enhancements on a single video:

```bash
python3 scripts/video_enhance.py upscale "$INPUT" --scale 2 --output /tmp/step1.mp4
python3 scripts/video_enhance.py restore-faces /tmp/step1.mp4 --fidelity 0.7 --output /tmp/step2.mp4
python3 scripts/video_enhance.py interpolate /tmp/step2.mp4 --multi 2 --output final_enhanced.mp4
```

The script extracts frames once and applies multiple enhancements to minimize I/O when using `--pipeline` mode:

```bash
python3 scripts/video_enhance.py pipeline "$INPUT" \
  --upscale 2 --restore-faces 0.7 --interpolate 2 \
  --output final_enhanced.mp4
```

## Time and Space Estimates

| Operation | Input | Time | Temp Space |
|-----------|-------|------|-----------|
| Upscale 4x | 10min 720p 30fps | 1-2.5 hours | 180-360GB |
| Upscale 2x | 10min 1080p 30fps | 2-4 hours | 300-600GB |
| Interpolate 2x | 10min 720p 30fps | ~5 minutes | Minimal |
| Face restore | 10min 720p 30fps | 30-60 minutes | 5-10GB |
| Remove BG | 10min 1080p 30fps | 30-60 minutes | 10-20GB |

**Always run `bash scripts/estimate_size.sh "$INPUT"` before starting.**

## VRAM Management

| Operation | VRAM | Priority |
|-----------|------|----------|
| Real-ESRGAN (--half) | 2-6GB | Medium |
| RIFE | 2-4GB | Light |
| CodeFormer | 2-4GB | Light |
| rembg (GPU) | 1-2GB | Light |

All operations load models on-demand and unload after processing. Multiple light models can coexist if combined VRAM < 12GB.

## Safety Rules

1. **Always estimate time and disk space** before starting — confirm with user
2. Run `bash scripts/preflight.sh "$INPUT" "$OUTPUT"` before writes
3. Never overwrite source video
4. For upscaling: verify sufficient disk space for temp frames (can be 100x+ input size)
5. Use trap to clean up temp directories on failure
6. Confirm before operations estimated to take >30 minutes

## Reference

Load `references/video-enhance.md` for model details, quality comparisons, and pipeline optimization.
