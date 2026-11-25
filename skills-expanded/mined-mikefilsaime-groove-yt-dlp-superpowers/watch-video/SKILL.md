---
name: watch-video
description: Use ONLY when the user explicitly asks to "Watch Video", "watch-video", or run the Watch Video skill. Builds a multimodal evidence bundle from a video URL or local media file by extracting transcript/subtitles plus ffmpeg screenshots at timed intervals so the AI can inspect what was visible on screen.
metadata:
  short-description: Watch videos with transcript plus timed screenshots
---

# Watch Video

Use this skill only when the user explicitly says **Watch Video** or names `watch-video`.

This is different from a transcript job. It creates a bundle with:

- source media from a URL or local video file
- subtitles/transcript, using local WhisperX/Whisper if captions are unavailable
- screenshots sampled with `ffmpeg`
- `watch_context.md`, pairing each sampled frame timestamp with nearby transcript text
- `manifest.json`, the machine-readable version of the same context

## Command

From the installed skill folder:

```bash
python3 "$HOME/.claude/skills/watch-video/scripts/watch_video.py" "VIDEO_URL_OR_FILE" --output-dir "DEST_DIR" --rate 1s
```

Default rate is `1s`, one frame every second.

Supported presets:

```text
4fps
2fps
1fps
1s
3s
5s
10s
```

Numeric seconds also work:

```bash
--rate 15
--rate 0.5
```

## Rate Selection

- Default to `1s`.
- Use `4fps` or `2fps` only when the user needs detailed UI/action analysis or the clip is short.
- Use `3s`, `5s`, or `10s` for long videos, lectures, podcasts, or low-motion screen recordings.
- If the user asks for a specific cadence, use it directly.

## Workflow

1. Run the script with the requested source and rate.
2. Open `watch_context.md` and inspect relevant frame links plus transcript context.
3. For detailed visual questions, use local image inspection on specific frames rather than relying only on the markdown.
4. Answer from both sources: what was said and what was visible.

## Dependencies

The script expects:

- `yt-dlp`
- `ffmpeg`
- local `whisperx` or `whisper` for caption fallback

It checks `PATH` first, then common local install paths:

```text
$HOME/.local/bin/whisperx
$HOME/.local/bin/whisper
$HOME/.buttercut/venv/bin/whisperx
$HOME/.perfect-cuts/venv/bin/whisperx
$HOME/GitHub/Marketing Assets and Skills/.venv-whisperx/bin/whisperx
$HOME/Library/Python/3.9/bin/whisperx
$HOME/Library/Python/3.9/bin/whisper
```

Optional overrides:

```bash
YTDLP_BIN=/path/to/yt-dlp
WHISPERX_BIN=/path/to/whisperx
WHISPER_BIN=/path/to/whisper
WHISPER_MODEL=base
WHISPER_DEVICE=cpu
WHISPER_COMPUTE_TYPE=int8
```

The script detects `yt-dlp` in this order:

```text
$YTDLP_BIN
python3 -m yt_dlp
yt-dlp on PATH
```
