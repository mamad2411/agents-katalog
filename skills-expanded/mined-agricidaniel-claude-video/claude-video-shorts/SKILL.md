---
name: claude-video-shorts
description: >
  Longform-to-shortform video pipeline that automatically extracts viral-ready short clips
  from long videos. V3 pipeline with VLM-powered visual analysis (Gemini 2.5 Flash), auto-detects
  screen recordings vs talking-head, uses "Framed" layout for screen content (padded top/bottom
  with centered captions), face-tracked crop for talking-head. Transcribes with WhisperX, scores
  by visual interest + transcript quality, adds karaoke captions, hook text, normalizes audio.
  Use when user says "shorts", "clips", "highlight", "shortform", "reels", "tiktok clips",
  "extract clips", "viral clips", "repurpose", "longform to shortform", "auto clip",
  "find best moments", or "screen recording shorts".
allowed-tools:
  - Bash
  - Read
  - Write
---

# claude-video-shorts — Longform to Shortform Pipeline (V3)

## One-Command Pipeline

### V3 Screen-Aware Pipeline (recommended)

For screen recordings, tutorials, and mixed content — uses VLM for visual analysis:

```bash
source ~/.video-skill/bin/activate && bash scripts/screen_shorts_pipeline.sh "$INPUT" \
  [--count N] [--min-duration S] [--max-duration S] [--style STYLE] \
  [--platform PLATFORM] [--skip-captions] [--skip-vlm] [--hook-text "Your hook here"] \
  [--mode screen|talking-head|auto]
```

### V1 Audio-Only Pipeline (legacy)

For simple talking-head content where face tracking is sufficient:

```bash
source ~/.video-skill/bin/activate && bash scripts/shorts_pipeline.sh "$INPUT" \
  [--count N] [--duration S] [--style STYLE] [--platform PLATFORM]
```

## V3 Pipeline Architecture

```
INPUT (any video) → Auto-detect mode (screen vs talking-head)
        │
  [1] WhisperX transcription (word-level timestamps)
  [2] PySceneDetect scene boundaries
  [3] Extract keyframes at scene cuts + intervals
  [4] Auto-detect: face rate <60% → screen mode
  [5] VLM analysis (Gemini 2.5 Flash) → visual interest + zoom regions
  [6] Topic segmentation + multi-modal scoring
  [7] Per-topic: extract → reframe → caption → normalize
  [8] Export for platform → manifest JSON
```

## Framed Layout (Screen Mode)

The validated layout for screen recordings (1080x1920):

```
+--------1080px--------+
|                       |
|  HOOK TEXT (200px)    |  "SEO Health Score: 57/100"
|  Compelling data pt   |  "What Claude found in seconds"
|                       |
+=======================+
|                       |
|  SCREEN CONTENT       |  Cropped from source, scaled to 1080x1372
|  (1372px)             |  VLM-selected crop position
|                       |  ~63% of source resolution
|  Score tables,        |  Readable on phone
|  data, charts...      |
|                       |
+=======================+
|                       |
|  KARAOKE CAPTIONS     |  Impact 72pt, yellow sweep fill
|  (348px)              |  Dark box background (BorderStyle=4)
|  Centered in zone     |  MarginV=240, word-by-word \kf timing
|                       |
+-----------------------+
```

### FFmpeg Filter Chain

```
crop={W}:{H}:{X}:0 → scale=1080:1372 → pad=1080:1920:0:200:black
→ drawbox (chrome mask) → drawtext (hook) → ass (captions)
```

### Crop Position Logic

VLM analyzes each frame and suggests zoom regions. The crop position (X) varies:
- **Left-aligned content** (tables, lists): x_pct ~0.22
- **Center-aligned content** (title pages, score circles): x_pct ~0.35
- **Right-aligned content** (sidebars, panels): x_pct ~0.55

Multiple zoom regions within a clip create **jump cuts** (not smooth pan) — this matches natural scroll/section transitions in screen recordings.

## Multi-Modal Scoring (V3)

| Factor | Weight | Source | Description |
|--------|--------|--------|-------------|
| Visual interest | 0.30 | VLM | Charts, tables, data = high score |
| Content completeness | 0.25 | VLM + transcript | Complete data shown, full thoughts |
| Audio engagement | 0.20 | Transcript | Emphasis words, questions, emotion |
| Hook potential | 0.15 | Transcript | First sentence strength |
| Standalone coherence | 0.10 | Transcript | Works without context |

## Caption Style (V3)

The validated caption parameters for the framed layout:

```
Font: Impact, 72pt, Bold
Primary: White (&H00FFFFFF)
Secondary/Karaoke: Yellow (&H0000FFFF)
Outline: Black, 4px
Background: Semi-transparent black (&HC0000000)
BorderStyle: 4 (opaque box behind text)
Alignment: 2 (bottom-center)
MarginV: 240 (centered in 348px bottom zone)
Letter spacing: 2
Animation: \kf word-by-word karaoke sweep
Words per line: 3
```

## Flags Reference

| Flag | Default | Description |
|------|---------|-------------|
| `--count N` | 5 | Number of shorts to extract |
| `--min-duration S` | 20 | Minimum clip length in seconds |
| `--max-duration S` | 55 | Maximum clip length in seconds |
| `--style STYLE` | bold | Caption style: default, bold, minimal, neon, shadow |
| `--platform PLAT` | shorts | Export: tiktok, reels, shorts, all |
| `--skip-captions` | false | Skip caption burn-in |
| `--skip-vlm` | false | Skip VLM analysis (audio-only scoring) |
| `--hook-text TXT` | auto | Custom hook text for all shorts |
| `--language LANG` | en | Transcription language |
| `--output-dir DIR` | input dir | Output directory |
| `--vlm-model MOD` | gemini-2.5-flash | VLM model for frame analysis |
| `--max-frames N` | 40 | Max frames for VLM analysis |
| `--mode MODE` | auto | Force: screen, talking-head, auto |

## Requirements

### Core (always needed)
- FFmpeg with libass support
- WhisperX (`pip install whisperx` in venv, 6GB VRAM)
- PySceneDetect (`pip install scenedetect`)

### VLM Analysis (screen mode)
- `GOOGLE_API_KEY` environment variable
- `pip install google-genai` in venv
- Cost: ~$0.01-0.03 per video (~40 frames via Gemini 2.5 Flash)

### Face Tracking (talking-head mode)
- MediaPipe (`pip install mediapipe`)
- OpenCV (`pip install opencv-python`)
- CPU-only, no VRAM required

## Platform Duration Limits

| Platform | Max Duration | Recommended | Aspect |
|----------|-------------|-------------|--------|
| TikTok | 10 min | 30-60s | 9:16 |
| Instagram Reels | 90s | 30-60s | 9:16 |
| YouTube Shorts | 60s | 30-55s | 9:16 |

## Safety Rules

1. Always run `bash scripts/preflight.sh "$INPUT" "$OUTPUT"` before writes
2. Never overwrite source video — all shorts are new files
3. Confirm before processing videos longer than 60 minutes
4. Clean up temp files after pipeline completes
5. Report estimated processing time before starting

## Reference

Load `references/shorts-pipeline.md` for detailed algorithms, scoring formulas, and tuning parameters.
