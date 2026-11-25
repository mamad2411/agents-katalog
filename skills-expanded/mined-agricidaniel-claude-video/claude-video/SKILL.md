---
name: claude-video
description: >
  AI-powered video production suite: editing, transcoding, captioning, analysis, creation,
  shortform pipeline, image/video generation, web screenshots, AI audio/video enhancement.
  Uses FFmpeg, Whisper, PySceneDetect, FLUX.2, Veo, Playwright, Real-ESRGAN, Demucs, and
  Remotion. GPU-accelerated with NVIDIA NVENC. Use when user says "video", "ffmpeg", "trim",
  "cut", "transcode", "caption", "export", "analyze", "download", "create video", "shorts",
  "tiktok clips", "generate image", "generate video", "screenshot", "upscale", "enhance",
  "denoise", "separate vocals", "face restore", "slow motion", "remove background", or "/video".
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
---

# claude-video — CLI-Native Video Editing for Claude Code

## Quick Reference

| Command | What it does |
|---------|-------------|
| `/video` | Interactive mode — describe what you want in plain English |
| `/video setup` | Install all dependencies (faster-whisper, auto-editor, scenedetect, yt-dlp, mediainfo) |
| `/video edit` | Trim, cut, split, merge, speed, crop, overlay, stabilize, transitions |
| `/video transcode` | Convert codecs, compress, GPU-accelerated encoding, two-pass |
| `/video audio` | Normalize loudness, reduce noise, mix, extract, remove silence |
| `/video caption` | Transcribe speech → animated word-by-word subtitles (Whisper + ASS) |
| `/video analyze` | Inspect with ffprobe, measure quality (VMAF/SSIM/PSNR), detect scenes |
| `/video export <platform>` | One-command export: youtube, tiktok, instagram, linkedin, web, gif, podcast |
| `/video download <url>` | Download video via yt-dlp with format selection |
| `/video create` | Programmatic video creation via Remotion (React-based motion graphics) |
| `/video shorts` | Longform → shortform pipeline: transcribe, score, crop 9:16, caption, export |
| `/video image` | AI image generation (Gemini 3 Pro Image, FLUX.2 local, SD 3.5, OpenAI, rembg) |
| `/video generate` | AI video generation (Veo 3.1, Runway Gen-4, local SVD) |
| `/video screenshot` | Web capture via Playwright (screenshots, recordings, Ken Burns) |
| `/video enhance-audio` | AI audio (Demucs separation, DeepFilter denoise, TTS, diarize, AudioSR) |
| `/video enhance` | AI video (Real-ESRGAN upscale, RIFE interpolation, CodeFormer, rembg) |
| `/video promo` | Stock footage + Remotion promo videos with contrast-aware text overlays |
| `/video setup --ai` | Install AI dependencies (PyTorch, WhisperX, FLUX.2, Real-ESRGAN, etc.) |

## Orchestration Logic

### Command Routing

When the user provides a specific command, load the matching sub-skill:

- `/video edit` or intent is trim/cut/split/merge/speed/crop/overlay/stabilize/transition → Read `skills/claude-video-edit/SKILL.md`
- `/video transcode` or intent is convert/compress/encode/codec/format change → Read `skills/claude-video-transcode/SKILL.md`
- `/video audio` or intent is audio normalize/noise/mix/extract/silence/volume/LUFS → Read `skills/claude-video-audio/SKILL.md`
- `/video caption` or intent is transcribe/subtitle/caption/whisper/SRT/ASS → Read `skills/claude-video-caption/SKILL.md`
- `/video analyze` or intent is inspect/info/quality/VMAF/metadata/scene detect/ffprobe → Read `skills/claude-video-analyze/SKILL.md`
- `/video export` or intent is export for youtube/tiktok/instagram/linkedin/web/gif/podcast → Read `skills/claude-video-export/SKILL.md`
- `/video download` or intent is download video from URL → Read `skills/claude-video-download/SKILL.md`
- `/video create` or intent is create/generate programmatic video/motion graphics/title card → Read `skills/claude-video-create/SKILL.md`
- `/video shorts` or intent is shortform/clips/TikTok shorts/reels from longform → Read `skills/claude-video-shorts/SKILL.md`
- `/video image` or intent is generate image/AI image/FLUX/stable diffusion/remove background → Read `skills/claude-video-image/SKILL.md`
- `/video generate` or intent is generate video/AI video/Veo/Runway/text-to-video → Read `skills/claude-video-generate/SKILL.md`
- `/video screenshot` or intent is screenshot/web capture/screen recording/Ken Burns → Read `skills/claude-video-screenshot/SKILL.md`
- `/video enhance-audio` or intent is separate vocals/denoise AI/diarize/TTS/voice clone/upsample audio → Read `skills/claude-video-enhance-audio/SKILL.md`
- `/video enhance` or intent is upscale/super resolution/interpolate/face restore/remove background video → Read `skills/claude-video-enhance/SKILL.md`
- `/video promo` or intent is promo video/stock footage/marketing video/stock clips with text → Read `skills/claude-video-promo/SKILL.md`
- `/video setup` → Run `bash scripts/setup.sh`
- `/video setup --ai` → Run `bash scripts/setup.sh --ai`

### Interactive Mode

When user says `/video` without arguments or describes a task in natural language:
1. Run `bash scripts/check_deps.sh` to verify tools are available
2. Run `bash scripts/detect_gpu.sh` to know encoding capabilities
3. Identify intent from the user's description
4. Route to the appropriate sub-skill
5. If intent is ambiguous, ask the user to clarify

### Multi-Step Pipelines

For complex requests that span multiple sub-skills (e.g., "download this YouTube video, remove silence, add captions, export for TikTok"), execute sub-skills sequentially:
1. Download → edit → caption → export
2. Pass output of each step as input to the next
3. Use temp files in `/tmp/claude-video/` for intermediate outputs
4. Clean up temp files after final output is produced

## Safety Rules — MANDATORY

1. **Always use `-n` flag** (no-overwrite) unless user explicitly requests overwrite
2. **Never let output path equal input path** — run `bash scripts/preflight.sh "$INPUT" "$OUTPUT"` before any write
3. **Never delete source files** — all operations produce new files
4. **Run preflight before every write operation**: `bash scripts/preflight.sh <input> <output>`
5. **Confirm before**: batch operations (>3 files), downloads, operations estimated >5 minutes
6. **Auto-execute without confirmation**: ffprobe analysis, thumbnail extraction, GPU detection, metadata reading
7. **Temp file cleanup**: use `trap 'rm -f "$TEMP"' EXIT INT TERM` pattern in all scripts
8. **Disk space check**: run `bash scripts/estimate_size.sh` before large encodes

### AI Sub-Skill Routing Guide

- **"separate vocals" / "isolate dialogue"** → `claude-video-enhance-audio` (Demucs, AI model)
- **"reduce noise" / "denoise"** → `claude-video-audio` (FFmpeg afftdn) for quick fix, `claude-video-enhance-audio` (DeepFilterNet3) for AI quality
- **"remove background"** from image → `claude-video-image` (rembg), from video → `claude-video-enhance` (rembg batch + alpha assembly)
- **"upscale" / "super resolution"** → `claude-video-enhance` (Real-ESRGAN)
- **"slow motion"** (basic) → `claude-video-edit` (setpts), (AI frame interpolation) → `claude-video-enhance` (RIFE)
- **"generate image/video"** → `claude-video-image` / `claude-video-generate`
- **"shorts" / "clips from long video"** → `claude-video-shorts`

## Python Virtual Environment

AI scripts require an isolated venv with PyTorch nightly cu128 (for RTX 5070 Ti Blackwell sm_120):

```bash
# Install the AI venv (one-time)
bash scripts/setup.sh --ai

# Venv location
~/.video-skill/bin/python3
~/.video-skill/bin/activate
```

All Python scripts in `scripts/` that use AI models (`segment_scorer.py`, `face_tracker.py`,
`image_generate.py`, `video_generate.py`, `audio_enhance.py`, `video_enhance.py`, `web_capture.py`)
require activation: `source ~/.video-skill/bin/activate`

## VRAM Management (16GB Budget — RTX 5070 Ti)

Before loading any GPU model, check free VRAM:
```bash
nvidia-smi --query-gpu=memory.free --format=csv,noheader,nounits
```

| Tier | VRAM | Models | Rule |
|------|------|--------|------|
| Exclusive (>10GB) | 12-13GB | FLUX.2 klein, Bark TTS | Must be ONLY GPU model loaded |
| Heavy (5-10GB) | 5-8GB | Demucs, WhisperX, AudioSR | One heavy at a time |
| Light (<5GB) | 1-4GB | rembg, CodeFormer, RIFE, pyannote | Can coexist if total <12GB |
| NVENC | ~500MB | Hardware encoder | Always available |
| CPU only | 0 | MediaPipe, PySceneDetect, Playwright, librosa | No VRAM needed |

**NEVER** run two heavy/exclusive models simultaneously. Load → process → unload → next model.

## Encoding Defaults

### GPU-First Strategy
1. Run `bash scripts/detect_gpu.sh` at start of any encoding task
2. If NVENC available: use `h264_nvenc`/`hevc_nvenc`/`av1_nvenc` with `-preset p5 -tune hq`
3. If no GPU: fallback to `libx264`/`libx265`/`libsvtav1` with `-preset medium`
4. Always add `-movflags +faststart` for MP4 output

### Codec Selection Priority
- **Stream copy** (`-c copy`): when no re-encoding needed (trim, remux, extract)
- **AV1** (`av1_nvenc` or `libsvtav1`): best compression, royalty-free — default for new encodes
- **H.264** (`h264_nvenc` or `libx264`): maximum compatibility (social media, older devices)
- **H.265** (`hevc_nvenc` or `libx265`): good compression + wide support — use when user requests

### Quality Defaults
- H.264: CRF 20 (CPU) / CQ 21 (NVENC)
- H.265: CRF 24 (CPU) / CQ 26 (NVENC)
- AV1: CRF 28 (CPU) / CQ 30 (NVENC)
- Audio: AAC 192k for video, 128k for web, Opus 128k for WebM

## Reference Files

Load on-demand as needed — do NOT load all at startup:

- `references/transcode.md` — Codec comparison, CRF guide, two-pass encoding, containers
- `references/filters.md` — Complete video filter catalog with exact FFmpeg commands
- `references/audio.md` — Loudness targets, noise reduction, audio processing
- `references/captions.md` — Whisper setup, ASS karaoke format, word-level styling
- `references/analyze.md` — FFprobe patterns, VMAF/SSIM/PSNR quality assessment
- `references/export-presets.md` — Platform-specific export commands (YouTube, TikTok, etc.)
- `references/gpu-accel.md` — NVENC commands, CUDA filters, RTX-specific settings
- `references/remotion.md` — Remotion setup, React video patterns, headless rendering
- `references/shorts-pipeline.md` — WhisperX models, scoring algorithm, face tracking, platform limits
- `references/image-generation.md` — FLUX.2, SD 3.5, OpenAI/Google APIs, rembg, video-native dimensions
- `references/video-generation.md` — Veo 3.1, Runway Gen-4, SVD local, polling, cost formulas
- `references/web-capture.md` — Playwright setup, device emulation, Ken Burns FFmpeg commands
- `references/audio-enhance.md` — Demucs, DeepFilterNet3, pyannote, TTS comparison, AudioSR
- `references/video-enhance.md` — Real-ESRGAN, RIFE, CodeFormer, rembg, frame pipelines
- `references/batch-processing.md` — GNU parallel + NVENC concurrency, batch AI, error handling

## Sub-Skills

- `claude-video-edit` — Video editing: trim, cut, split, merge, speed, crop, overlay, stabilize, transitions
- `claude-video-transcode` — Codec conversion, compression, GPU encoding, two-pass, container remux
- `claude-video-audio` — Audio normalization, noise reduction, mixing, extraction, silence removal
- `claude-video-caption` — Speech-to-text transcription, animated subtitles, burn-in styling
- `claude-video-analyze` — Video inspection, quality metrics, scene detection, metadata analysis
- `claude-video-export` — Platform-optimized exports (YouTube, TikTok, Instagram, LinkedIn, Web, GIF, Podcast)
- `claude-video-download` — Video downloading via yt-dlp with format and quality selection
- `claude-video-create` — Programmatic video creation via Remotion (React-based motion graphics)
- `claude-video-shorts` — Longform → shortform pipeline: transcribe, score, crop 9:16, caption, export
- `claude-video-image` — AI image generation: Gemini 3 Pro Image, FLUX.2 local, SD 3.5, OpenAI API, rembg
- `claude-video-generate` — AI video generation: Veo 3.1, Runway Gen-4 Turbo, local SVD
- `claude-video-screenshot` — Web capture: Playwright screenshots, recordings, Ken Burns animation
- `claude-video-enhance-audio` — AI audio: Demucs separation, DeepFilter denoise, TTS, diarize, AudioSR
- `claude-video-enhance` — AI video: Real-ESRGAN upscale, RIFE interpolation, CodeFormer face restore, rembg

## Scripts

- `scripts/setup.sh` — Install all dependencies with user confirmation
- `scripts/detect_gpu.sh` — Detect NVIDIA NVENC, list encoders (JSON output)
- `scripts/check_deps.sh` — Verify all tools installed with versions (JSON output)
- `scripts/preflight.sh` — Safety check: input exists, output != input, disk space ok
- `scripts/estimate_size.sh` — Estimate output file size from duration + target codec
- `scripts/caption_pipeline.sh` — End-to-end: audio extract → whisper → ASS → burn-in
- `scripts/shorts_pipeline.sh` — Full shortform pipeline: transcribe → score → crop → caption → export
- `scripts/segment_scorer.py` — WhisperX transcription + engagement scoring (requires venv)
- `scripts/face_tracker.py` — MediaPipe face detection + smart crop to 9:16 (requires venv)
- `scripts/image_generate.py` — FLUX.2 / SD 3.5 / OpenAI image generation (requires venv)
- `scripts/video_generate.py` — Veo / Runway / SVD video generation (requires venv)
- `scripts/web_capture.py` — Playwright screenshots, recording, Ken Burns (requires venv)
- `scripts/audio_enhance.py` — Demucs / DeepFilter / pyannote / TTS / AudioSR (requires venv)
- `scripts/video_enhance.py` — Real-ESRGAN / RIFE / CodeFormer / rembg (requires venv)
- `scripts/screen_shorts_pipeline.sh` — V3 screen-aware shorts pipeline (VLM + framed layout)
- `scripts/frame_analyzer.py` — VLM frame analysis via Gemini 2.5 Flash (requires venv + GOOGLE_API_KEY)
- `scripts/topic_segmenter.py` — Topic boundary detection + multi-modal scoring (requires venv)
- `scripts/smart_reframe.py` — Content-aware vertical reframe with framed layout (requires venv)

## Agents

For complex multi-step tasks, delegate to specialized agents via Task tool:
- `claude-video-encoder` — Complex encoding pipelines (multi-pass, multi-output, batch)
- `claude-video-analyst` — Deep quality assessment and comprehensive video analysis
- `claude-video-producer` — Production pipeline specialist (multi-step, VRAM management, cost tracking)
