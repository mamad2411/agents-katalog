---
name: claude-video-promo
description: >
  Create promo videos using free stock footage (Pixabay/Pexels) as backgrounds with
  Remotion text overlays, transitions, effects, and audio. Contrast-aware text placement
  adapts to background brightness. Use when user says "promo video", "stock footage video",
  "marketing video", "video with stock", "/video promo", or describes creating a video
  from stock clips with text overlays.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
---

# claude-video-promo: Stock Footage + Remotion Promo Videos

Create polished promo/marketing videos by combining **free stock footage** with
Remotion text overlays, transitions, and audio: with **contrast-aware text placement**.

## V2 Intelligence Layer

The pipeline includes a **scene planner** that automatically makes aesthetic decisions:

### Scene Intent Classification
The planner reads headlines/subtexts and classifies each scene:
- **hook**: First scene, dramatic, dark (Ken Burns: zoom out reveal)
- **problem**: Tension, urgency (Ken Burns: slow pan)
- **feature**: Clean, professional (Ken Burns: zoom in focus)
- **proof**: Warm, collaborative (static or medium)
- **cta**: Last scene, urgent (Ken Burns: subtle zoom, 15% larger text)

### Transition Decision Tree
Transitions are auto-selected based on scene context:
- Dark to bright: fade (0.7s, smooth brightness ramp)
- Hook to problem: cut (punchy, immediate)
- Feature to feature: wipe-left (progression feel)
- Any to CTA: zoom (builds urgency)

### Audio Intelligence
Per-scene ducking levels and ramp speeds:
- Hook: duck to 0.10, 10-frame ramp
- Feature: duck to 0.10, 10-frame ramp
- CTA: duck to 0.08, 5-frame ramp (fastest, voice most prominent)
- Proof: duck to 0.15, 15-frame ramp (music more present)

### Contrast Analysis V2
Uses worst-case zone brightness (not average) plus variance detection:
- High variance (busy background): always strong backing
- Bright zone in text area (>0.5): force backing regardless of average
- Clean dark background: no backing, just shadow

## Prerequisites

- **Pixabay API key**: Free at https://pixabay.com/api/docs/ (set `PIXABAY_API_KEY` env var)
- **Pexels API key** (optional): Free at https://www.pexels.com/api/ (set `PEXELS_API_KEY` env var)
- **FFmpeg**: Required for video preprocessing and contrast analysis
- **Node.js + npm**: For Remotion rendering
- **Remotion project**: The `promo-pipeline/` directory bundled with this plugin

## Pipeline: 3 Stages

```
1. ACQUIRE          2. ANALYZE           3. RENDER
Stock search     →  Frame contrast   →   Remotion composition
Stock download       analysis             AdaptiveText overlay
FFmpeg preprocess    Luminance grid        Transitions + Audio
TTS voiceover        contrast-map.json    Final MP4 output
```

## Workflow

### Step 1: Understand the Request

Determine from the user (conversationally or via YAML config):
- What scenes are needed (topic, text, duration)
- What stock footage to search for (keywords, mood)
- Text positioning (center, lower-third, upper-left, upper-right)
- Transitions between scenes (fade, wipe-left, wipe-right, zoom, cut)
- Audio: background music query + voiceover text
- Output: resolution, codec, destination path

### Step 2: Search Stock Footage

```bash
python3 promo-pipeline/scripts/stock_search.py \
  --query "aerial city night" \
  --source pixabay \
  --orientation landscape \
  --min-duration 8 \
  --count 5
```

For music:
```bash
python3 promo-pipeline/scripts/stock_search.py \
  --query "upbeat corporate" \
  --source pixabay \
  --media-type music \
  --count 3
```

Present results to user with preview URLs. Let them pick.

### Step 3: Download + Preprocess

```bash
python3 promo-pipeline/scripts/stock_download.py \
  --url "DOWNLOAD_URL" \
  --output promo-pipeline/public/stock/scene-id.mp4 \
  --trim-duration 10 \
  --gpu
```

This scales to 1080p 30fps, pads if needed, and encodes H.264.

### Step 4: Analyze Contrast

```bash
python3 promo-pipeline/scripts/analyze_contrast.py \
  --input promo-pipeline/public/stock/scene-id.mp4 \
  --output promo-pipeline/public/stock/scene-id-contrast.json
```

Produces a per-second 4x3 luminance grid. The Remotion `AdaptiveText` component
reads this to adjust text backing plates:
- Dark background → white text, no backing, subtle shadow
- Mid background → white text, semi-transparent dark plate
- Bright background → white text, strong dark plate

### Step 5: Generate TTS (if voiceover needed)

Use the existing Gemini TTS script:
```bash
python3 promo-pipeline/scripts/tts_generate.py \
  --text "Your voiceover text here" \
  --output promo-pipeline/public/voiceover/scene-id.wav
```

### Step 6: Build Scene Config JSON

Create `scene-config.json` with all paths and contrast data resolved:

```json
{
  "scenes": [
    {
      "id": "hook",
      "durationFrames": 150,
      "stockPath": "stock/hook.mp4",
      "contrastMap": { ... },
      "headline": "The Future is Here",
      "subtext": "Launching Spring 2026",
      "textPosition": "center",
      "transition": "fade",
      "voiceoverPath": "voiceover/hook.wav"
    }
  ],
  "musicPath": "music/background.mp3",
  "musicVolume": 0.3,
  "musicFadeInFrames": 30,
  "musicFadeOutFrames": 60,
  "voiceoverDucking": 0.15
}
```

### Step 7: Render

```bash
cd promo-pipeline
npx remotion render PromoVideo --props scene-config.json --codec h264 --crf 18
```

## YAML Config Format (Alternative to Conversational)

Users can write a YAML config and the pipeline resolves everything:

```yaml
scenes:
  - id: hook
    duration: 5s
    stock:
      query: "aerial city night lights"
      source: pixabay
    text:
      headline: "The Future is Here"
      subtext: "Launching Spring 2026"
      position: center
    transition: fade
    voiceover: "The future of marketing is about to change."

  - id: features
    duration: 8s
    stock:
      query: "technology dashboard data"
      source: pexels
    text:
      headline: "AI-Powered Analytics"
      position: lower-third
    transition: wipe-left

audio:
  music:
    query: "upbeat corporate"
    volume: 0.3
    ducking: 0.15
```

## Safety Rules

1. **Never overwrite source files**: all operations produce new files
2. **Check API key before searching**: fail clearly if PIXABAY_API_KEY is missing
3. **Validate stock video duration >= scene duration** before rendering
4. **Pre-trim music** to match total video duration (Remotion Audio doesn't loop)
5. **Confirm before batch downloads**: stock video files can be large

## Text Position Reference

| Position | Where | Best For |
|----------|-------|----------|
| `center` | Vertically + horizontally centered | Hero statements, titles |
| `lower-third` | Bottom 25%, full width | News-style, documentary |
| `upper-left` | Top-left corner | Subtitles, labels |
| `upper-right` | Top-right corner | Branding, logos |

## Transition Reference

| Type | Effect | Use When |
|------|--------|----------|
| `fade` | Opacity crossfade (0.5s) | Default, smooth |
| `wipe-left` | Horizontal clip reveal from left | Sequential progression |
| `wipe-right` | Horizontal clip reveal from right | Reverse/callback |
| `zoom` | Scale + fade dissolve | Dramatic emphasis |
| `cut` | Instant switch | Fast pacing, urgency |

## Scripts

- `scripts/stock_search.py`: Search Pixabay + Pexels video/music APIs (stdlib only)
- `scripts/stock_download.py`: Download + FFmpeg preprocess to 1080p 30fps
- `scripts/analyze_contrast.py`: Frame luminance analysis → JSON contrast map

## Remotion Components

- `src/components/PromoVideo.tsx`: Main composition: sequences scenes + audio
- `src/components/StockScene.tsx`: Single scene: OffthreadVideo bg + adaptive text + Ken Burns
- `src/components/AdaptiveText.tsx`: Contrast-aware text with spring/fade/typewriter/slide-up animations
- `src/components/Transitions.tsx`: Fade, wipe, zoom transitions between scenes
- `src/components/AudioLayer.tsx`: Background music with voiceover ducking
- `src/hooks/useContrast.ts`: Reads contrast map, returns per-frame adaptive text styles
