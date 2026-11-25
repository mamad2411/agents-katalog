---
name: media-transform
description: Generic media transformation orchestrator — download videos from any source (X/Twitter, Zoom, YouTube, web embeds), upload to YouTube, transcribe with timestamps, generate chapters, create thumbnails with GPT-Image-2, and A/B test titles. Use when the user wants to move a video from one platform to another, or asks to "download and upload this video to YouTube", "publish this recording", "save and transcribe this", or any video pipeline task. Encodes learned best practices and preferences for each stage.
---

# Media Transform

Generic orchestrator for media transformation pipelines. Chains atomic skills based on source and destination, with stage-by-stage checkpoints.

## Architecture

Each pipeline stage is handled by a dedicated atomic skill. This orchestrator provides:

1. **Stage selection** — which steps to run based on source/destination
2. **Preferences** — battle-tested defaults and known gotchas
3. **Learnings** — what worked, what didn't, what to avoid
4. **Checkpoints** — present plan, get confirmation, then execute

## Atomic Skills

| Stage | Skill | Notes |
|-------|-------|-------|
| Download (X/Twitter) | `download-x-video` | yt-dlp, `--print after_move:filepath` |
| Download (Zoom) | `zoom-download` | Browser-based, gallery view preferred |
| Download (web embeds) | `download-video` | Handles Vimeo, YouTube embeds, referer headers |
| Download (generic URL) | `yt-dlp` directly | `brew install yt-dlp` |
| Upload to YouTube | `youtube-api` | OAuth, resumable upload, tags, metadata |
| Update metadata | `youtube-api` | `update_metadata.py` — title, description, tags |
| Set thumbnail | `youtube-api` | `set_thumbnail.py` — upload custom thumbnail |
| Transcribe | `transcribe-anything` | Multi-backend, auto-selects best |
| Chapters (LLM titles) | `podcast-publishing-assistant` | High-quality chapter summaries |

## Pipelines

### Pipeline A: X/Twitter → YouTube + Chapters

```
download-x-video → youtube-api (upload) → transcribe-anything → youtube-api (update description)
```

```bash
# 1. Download
python3 download-x-video/scripts/download_x_video.py "https://x.com/user/status/123/video/1" /tmp

# 2. Upload (unlisted)
python3 youtube-api/scripts/upload_video.py \
    --file /tmp/x_video_<id>.mp4 \
    --title "Video Title" \
    --privacy unlisted

# 3. Transcribe (prefer mlx_whisper on Apple Silicon)
mlx_whisper /tmp/x_video_<id>.mp4 \
    --model mlx-community/whisper-turbo \
    --output-dir /tmp --output-format json \
    --word-timestamps True

# 4. Generate chapters + update description
# See Chapter Generation section below
```

### Pipeline B: Zoom → YouTube + Thumbnails

```
zoom-download → youtube-api (upload + metadata + thumbnail)
```

Zoom recordings typically have built-in transcripts. Focus on proper titling, playlist assignment, and thumbnails.

### Pipeline C: Generic Video → YouTube + Transcription

```
yt-dlp download → youtube-api (upload) → transcribe-anything
```

For any video URL that yt-dlp supports (YouTube, Vimeo, etc.), download and re-publish.

## Title Generation

Generate 3-5 title candidates using the LLM. Evaluate against these heuristics:

**What makes a good YouTube title:**
- **Curiosity gap**: Implies something the viewer doesn't know yet
- **Specificity**: Names, numbers, concrete claims beat vague ones
- **Pattern interrupt**: Unexpected framing or contradiction
- **Under 70 chars**: Avoids truncation in search results
- **Front-load keywords**: Most important words first
- **No clickbait**: Title must match content (retention matters more than CTR)

**Title generation prompt template:**
```
Generate 5 YouTube title candidates for a video about [topic].
The video is [duration] and [brief content description].

Requirements:
- Under 70 characters each
- Different angles: (1) curiosity-driven, (2) how-to/value, (3) controversial/contrarian,
  (4) specific/numbers-driven, (5) question-based
- No ALL CAPS, no emoji overuse
- Titles must accurately reflect the content
```

### A/B Testing Titles

YouTube Studio has native "Test & Compare" (tests up to 3 titles/thumbnails, runs up to 2 weeks, winner based on watch time share). This is NOT available via the YouTube Data API directly.

**Programmatic DIY A/B testing:**

Use `youtube-api/scripts/update_metadata.py` to rotate titles on a schedule, then analyze performance via YouTube Analytics:

```bash
# Start test: set title A
python3 youtube-api/scripts/update_metadata.py --video-id <ID> --title "Title A"

# After 24-48h: rotate to title B
python3 youtube-api/scripts/update_metadata.py --video-id <ID> --title "Title B"

# After 24-48h more: check analytics to determine winner
# Winner = higher CTR * average view duration (or just CTR for early tests)
```

**A/B testing schedule:**
- Rotate every 24-48 hours (YouTube needs time to collect impressions)
- Test 2-3 titles per video
- Run for 1-2 weeks total
- Winner based on: CTR (click-through rate) × retention, not just view count

## Thumbnail Generation

### GPT-Image-2 (Recommended)

GPT-Image-2 (`openai/gpt-image-2`) via the `image_generate` tool is the preferred thumbnail generator:

**Key capabilities relevant to thumbnails:**
- **Near-perfect text rendering**: Can include readable text on thumbnails (previously impossible with AI)
- **Thinking mode**: Plans composition before rendering — ensures faces, text, and layout are coherent
- **Up to 2K resolution**: 2048px, perfect for 1280×720 thumbs with room to crop
- **Aspect ratio 16:9**: Native YouTube thumbnail ratio
- **Multilingual text**: Works across scripts (Latin, CJK, etc.)
- **Multi-variant generation**: Up to 4-8 coherent variations from one prompt

**Thumbnail prompt template:**
```
YouTube thumbnail for a video titled "[TITLE]". Style: [clean/bold/minimalist/tech].
[Specific visual elements: faces, diagrams, text overlays].
Aspect ratio: 16:9. High contrast, eye-catching. No clutter. 
Text on image (if any): "[KEY PHRASE]" in [position].
```

**Post-generation:**
- Use `youtube-api/scripts/set_thumbnail.py` to upload
- Compress if >2MB: `convert -resize 1280x720 -quality 85 input.png output.jpg`

### Thumbnail A/B Testing

YouTube's native "Test & Compare" supports up to 3 thumbnails. Generate 3 distinct concepts:
1. **Text-heavy**: Key phrase or number in large font
2. **Face/emotion**: Expressive reaction, eye contact
3. **Concept/abstract**: Visual metaphor for the topic

## Stage-by-Stage Preferences & Learnings

### Download

**yt-dlp path detection:**
- Use `--print after_move:filepath` for reliable final path (don't parse stdout for `[download] Destination`)
- HLS streams from X/Twitter use fragmented filenames during download; only the `after_move` path is the final merged file

**X/Twitter auth:**
- Some videos require authentication: `yt-dlp --cookies-from-browser chrome`

### Upload

**OAuth token caching:**
- `youtube-api` skill handles this: `~/.config/youtube-api/token.pickle` (or Cowork path)
- First run opens browser for consent; cached for subsequent runs
- On Mac → local config; in Cowork VM → mounted Downloads folder (persists across resets)

**Privacy default:**
- Always default to `unlisted` unless user explicitly asks for `public`

**Resumable uploads:**
- Google API client supports resumable uploads — large files (100MB+) upload smoothly

### Transcription

**Prefer mlx_whisper on Apple Silicon (10x faster):**
- `mlx_whisper` (`pipx install mlx-whisper`): ~1300 frames/s → ~2 min for 27 min audio
- `openai-whisper` CLI: ~95 frames/s → ~28 min for same audio
- `openai-whisper` with `--device mps` produces NaN errors with turbo/large models — **avoid**, use mlx_whisper instead

**Turbo model is the sweet spot:**
- Fast enough for real-time use
- Quality nearly as good as large
- Small is too inaccurate for chapter generation

**Diarization is aspirational:**
- Requires whisperX + pyannote + HuggingFace token
- Adds 5-10 min processing
- Quality varies with audio clarity
- Use `transcribe-anything` with `--diarize` flag when available

### Chapter Generation

**Garbage filtering is essential:**
- Filter out pure filler segments: "Yeah.", "Cool.", "Mm-hmm.", "Right."
- Filter repetitive filler: "Yeah. Yeah. Yeah." (3+ garbage words in a row)
- Null segments (empty text, zero duration) at the end are common

**Word-boundary truncation:**
- Don't truncate chapter titles mid-word
- "What areas of data do you feel are underserved by now that l" → truncate at last space

**LLM titles when quality matters:**
- Raw transcript chapters are functional but ugly
- For polished output, use `podcast-publishing-assistant` or feed segments to an LLM
- Prompt: "Generate concise chapter titles (<60 chars) for these transcript segments with timestamps"

**Interval tuning:**
- Default 30s gives ~46 chapters for 27 min video — good for navigation
- 60s gives ~27 chapters — cleaner but less granular
- 10s is too granular for YouTube (chapter limit is ~100)

## Checkpoint Pattern

Before each action phase, present a summary and get confirmation. This catches mismatches early:

1. **Pre-flight**: Scan source (tweet, Zoom recordings, etc.) → list what's available
2. **Title check**: Present 3-5 title candidates, user picks
3. **Thumbnail check**: Generate 3 thumbnail variants, user picks
4. **Download complete**: Confirm file, title, duration
5. **Upload complete**: Confirm URL, privacy, playlist
6. **Transcription complete**: Confirm segment count, quality
7. **Final**: Present all results, offer title A/B test setup

## Troubleshooting

### YouTube API not enabled
```bash
gcloud services enable youtube.googleapis.com --project=<PROJECT_ID>
```

### OAuth redirect fails (ERR_CONNECTION_REFUSED)
- Ensure port is free: `lsof -i :8080`
- GCP OAuth must have `http://localhost` in redirect URIs

### mlx_whisper "Failed to load audio"
- `brew install ffmpeg`

### Chapter quality is poor
- Raw transcript chapters work for quick navigation but look unprofessional
- For publication-quality, use `podcast-publishing-assistant` or LLM post-processing
- Garbage filtering catches most bad chapters but may miss edge cases ("I mean", "you know")

### Thumbnail too large
- YouTube max is 2MB. Compress: `convert -resize 1280x720 -quality 85 input.png output.jpg`
- GPT-Image-2 outputs may need compression for multi-variant uploads
