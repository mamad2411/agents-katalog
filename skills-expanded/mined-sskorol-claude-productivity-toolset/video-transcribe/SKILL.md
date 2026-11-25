---
name: video-transcribe
description: Download and transcribe a video from any source — Vimeo, YouTube, Loom, or Google Drive (including canDownload:false restricted files). Outputs a transcript file. Use when the user says "transcribe", "transcribe video", or when a workflow needs to extract audio and text from a video.
argument-hint: "<video-url-or-drive-file-id> [output-dir] [language] [summarize]"
---

# Video Transcribe Skill

Download a video from any source and transcribe it with mlx_whisper on Apple Silicon.

## Required Tools

- `yt-dlp` — video downloading (streaming platforms)
- `ffmpeg` — audio extraction
- `mlx_whisper` — Apple Silicon GPU transcription
- `node` — for Google Drive protected video download
- `drive-video-download` skill — for `canDownload:false` Drive files

## Step 1: Identify the video source

| URL pattern | Method |
|---|---|
| `vimeo.com`, `youtube.com`, `youtu.be`, `loom.com` | yt-dlp |
| `drive.google.com/file/d/...` | Check `canDownload` via Drive API, then choose method |
| Drive MIME type `video/*` with `canDownload: true` | `mcp__gws__drive_files_get` with `alt=media` |
| Drive MIME type `video/*` with `canDownload: false` | `drive-video-download` skill |

## Step 2: Generate a timestamp-based filename

Always derive the output filename from the current timestamp, not from the video title or date.
This ensures multiple transcriptions on the same day never overwrite each other.

```bash
FILENAME=$(date +%Y%m%d-%H%M%S)
echo "Using filename stem: $FILENAME"
```

Use `$FILENAME` as the stem for all audio, transcript, and summary files below.

## Step 3: Download audio

### Streaming platforms (Vimeo, YouTube, Loom, etc.)

**CRITICAL: Always prefer HTTP single-file format over fragmented DASH/HLS streams.**
DASH and HLS formats split audio into hundreds of tiny fragments, resulting in ~150 KB/s downloads due to per-fragment HTTP overhead. HTTP formats download as a single file at ~8-14 MB/s.

```bash
# List available formats
yt-dlp -F "VIDEO_URL"

# Download using HTTP format (fastest)
# For Vimeo: http-240p (lowest quality with audio, ~120MB/hr, downloads in ~20s)
# For YouTube: pick a format with protocol "https" (not "m3u8" or "dash")
yt-dlp -f "http-240p" -o "/tmp/video-$FILENAME.%(ext)s" "VIDEO_URL"

# Extract audio
ffmpeg -y -i /tmp/video-$FILENAME.mp4 -vn -acodec libmp3lame -q:a 2 /tmp/video-$FILENAME.mp3
```

**Format selection priority:**
1. `http-*` formats (protocol: https) — fastest, single-file
2. `hls-audio-*` formats (protocol: m3u8) — fallback, audio-only fragmented
3. `dash-audio-*` formats (protocol: dash) — AVOID, slowest

Fallback if no HTTP format:
```bash
yt-dlp -x --audio-format mp3 -o "/tmp/video-%(id)s.%(ext)s" "VIDEO_URL"
```

### Google Drive videos — canDownload: false (corporate recordings, Meet recordings)

yt-dlp and the Drive API both return 403. Use the `drive-video-download` skill:

**Prerequisites:** Brave running, user logged in, remote debugging enabled (`brave://inspect/#devices` → toggle).

```bash
node ~/.claude/skills/drive-video-download/scripts/download.mjs <file-id-or-url> /tmp/video-$FILENAME.m4a
```

The script intercepts the `workspacevideo-pa` streaming manifest via CDP and downloads with exact browser headers. No conversion needed — `.m4a` is accepted directly by mlx_whisper.

### Google Drive videos — canDownload: true

```
mcp__gws__drive_files_get with params: {"fileId": "...", "alt": "media", "supportsAllDrives": true}
```
Save to `/tmp/video-$FILENAME.mp4`, then extract audio with ffmpeg if needed.

## Step 4: Transcribe

**IMPORTANT: Use the local HuggingFace snapshot path, NOT the model name string.** The short form (`mlx-community/whisper-medium-mlx`) fails with `FileNotFoundError` because Hub path resolution is broken in this environment.

The language is taken from the 3rd skill argument (e.g. `uk`, `de`). Default to `en` if not provided.

```bash
# Resolve local snapshot path
SNAPSHOT_DIR=~/.cache/huggingface/hub/models--mlx-community--whisper-large-v3-turbo/snapshots
SNAPSHOT=$(ls "$SNAPSHOT_DIR" | head -1)
MODEL_PATH="$SNAPSHOT_DIR/$SNAPSHOT"

# LANGUAGE = 3rd skill argument, default "en"
LANGUAGE="${3:-en}"

# Run in background for long videos (NEVER pipe — SIGPIPE kills mlx_whisper silently)
nohup mlx_whisper /tmp/video-$FILENAME.m4a \
  --model "$MODEL_PATH" \
  --output-name "$FILENAME" \
  --language "$LANGUAGE" \
  --output-format all \
  --output-dir /tmp/transcripts \
  > /tmp/whisper-$FILENAME.log 2>&1 &

# Monitor progress
tail -f /tmp/whisper-$FILENAME.log
```

**Critical rules:**
- Always use `mlx_whisper` — runs on Apple Silicon GPU (~3 min/hour of video on M4 Pro)
- Never use `whisper` (openai-whisper) — falls back to CPU, 10-20x slower
- Never use `--device mps` with openai-whisper — produces NaN errors on Apple Silicon
- Always run as background job (`nohup ... &`) for videos over 10 minutes
- Never pipe (`| head`, `| tee`) — SIGPIPE silently kills the process
- `.m4a` input works directly — no need to convert to `.mp3` first
- If model not downloaded yet: `mlx_whisper --model mlx-community/whisper-large-v3-turbo /dev/null` downloads it (ignore the error)

## Step 5: Summarize (optional)

If the 4th skill argument is `summarize` (or the user requested a summary), read the transcript and produce a structured summary.

```bash
cat /tmp/transcripts/$FILENAME.txt
```

Then write a markdown summary to `/tmp/transcripts/$FILENAME-summary.md` covering:
- **Date / meeting title** (from filename or transcript context)
- **Participants** mentioned
- **Key topics discussed** (bullet points)
- **Decisions made**
- **Action items** (with owner if mentioned)

Save it alongside the transcript and show it to the user inline.

## Output

- Audio file: `/tmp/video-$FILENAME.m4a` (or `.mp3`)
- Transcript files: `/tmp/transcripts/$FILENAME.{txt,vtt,srt,json,tsv}`
- Summary (if requested): `/tmp/transcripts/$FILENAME-summary.md`
- Copy transcript/summary to project directory as needed, **preserving the `$FILENAME` timestamp stem** — never rename to the meeting date or video title

## Usage Examples

```
# Transcribe a Vimeo video
/video-transcribe https://vimeo.com/123456789

# Transcribe a protected Google Drive recording
/video-transcribe https://drive.google.com/file/d/1GJqYdf.../view

# Specify language (default: en)
/video-transcribe https://vimeo.com/123456789 /tmp/transcripts uk

# Transcribe and summarize
/video-transcribe https://drive.google.com/file/d/1GJqYdf.../view /tmp/transcripts uk summarize
```
