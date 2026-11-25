---
name: editor-post-production
description: >-
  Assemble and finalize AI videos — concat, loudnorm, STS voice swap, overlay, music,
  edit, resize, and upload. Only runs the steps that apply based on format config.
requires:
  env:
    - VIDJUTSU_API_KEY
compatibility: >-
  Called by the director skill as pipeline step 4.
  Uses VidJutsu API (overlay, upload, transcribe).
  ElevenLabs required only if STS voice swap is enabled.
  Full API reference at https://docs.vidjutsu.ai/llms.txt
---

# Director — Post

Assemble the final video from passed clips. Each step is conditional — only run what the format config requires.

## Step 1 — Concat

Join all passed clips with ffmpeg hard cuts (no crossfades):

```bash
ffmpeg -f concat -safe 0 -i concat.txt -c copy concat.mp4
```

If sound is disabled, strip any residual audio:
```bash
ffmpeg -i concat.mp4 -an -c:v copy concat-silent.mp4
```

## Step 2 — Loudnorm (if speech enabled)

Skip if the video has no spoken audio.

Two-pass FFmpeg loudnorm at -16 LUFS to normalize volume across scenes:

```bash
# Pass 1: measure
ffmpeg -i concat.mp4 -af loudnorm=I=-16:print_format=json -f null /dev/null
# Pass 2: apply with measured values
ffmpeg -i concat.mp4 -af "loudnorm=I=-16:measured_I=<val>:measured_LRA=<val>:measured_TP=<val>:measured_thresh=<val>" normalized.mp4
```

## Step 3 — STS voice swap (if enabled)

Skip if no spoken dialogue or character has no `voiceId`.

Single-pass ElevenLabs Speech-to-Speech on the full concatenated audio. **Always on the final concat, never per-scene** — this produces consistent levels and is cheaper.

After STS, run `POST /v1/transcribe` to catch any artifacts introduced by the voice swap.

Save a pre-STS copy — if STS introduces issues, you can re-swap or fall back to native voice.

## Step 4 — Overlay (if enabled)

Skip if no overlay text.

```
POST /v1/overlay
{
  "videoUrl": "<videoUrl>",
  "text": "<overlayText>",
  "position": "<top|center|bottom>",
  "fontSize": <optional>
}
```

Returns `{ "id": "ovl_...", "resultUrl": "https://cdn.vidjutsu.ai/..." }`.

Apply overlay **before** captions (ZapCap renders on top of everything).

## Step 5 — Music (if provided)

Skip if no music prompt or URL.

**Generate via Suno (through KIE):**
```
POST https://api.kie.ai/api/v1/generate
{
  "prompt": "<music prompt>",
  "instrumental": true,
  "model": "V5",
  "customMode": false
}
```
Poll `GET /generate/record-info?taskId=<taskId>` every 5s.

**Mix onto video:**
```bash
ffmpeg -i video.mp4 -i music.mp3 -t <duration> \
  -map 0:v:0 -map 1:a:0 -c:v copy -c:a aac -b:a 192k \
  -af "afade=t=in:st=0:d=0.5,afade=t=out:st=<fadeStart>:d=1.5,volume=0.6" \
  -shortest output.mp4
```

Defaults: volume 0.6, fade in 0.5s, fade out 1.5s. User can override.

## Step 6 — Edit (if speech enabled)

Skip if no spoken dialogue.

- Trim dead air at start/end
- Shorten silence gaps > 0.5s to 0.3s
- Mute audio artifacts at specific timestamps
- Run final `POST /v1/transcribe` to verify the edit is clean

## Step 7 — Resize

Scale to exact 1080x1920 for Instagram Reels:

```bash
ffmpeg -i output.mp4 -vf "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black" -c:a copy final.mp4
```

## Step 8 — Upload and report

Upload final video via `POST /v1/upload`. Report:

- Output file path and CDN URL
- File size and duration
- Model used
- Per-scene results: critic score, attempt count
- Which post-production steps were applied
