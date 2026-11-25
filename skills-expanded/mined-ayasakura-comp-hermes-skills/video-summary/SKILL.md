---
name: video-summary
description: Trigger when a YouTube link, X/Twitter video link, or other yt-dlp-supported video URL appears and the user wants the video understood. By default use audio transcription; only extract and recognize video frames when the user explicitly asks for visual/video recognition. Then explain and summarize it inline.
version: 1.2.0
license: MIT
metadata:
  hermes:
    tags: [video, download, audio, transcript, transcription, whisper, breeze, summary]
---

# Video URL → Audio → Transcript

Use this skill when the user asks to download one or more video URLs, keep only their audio, transcribe them, explain what they are about, or “read the whole thing.” It supports any URL accepted by `yt-dlp`, including X/Twitter and YouTube.

## Run

Always write the complete output into the active Pi session directory. `PI_SESSION_FILE` is the current session's JSONL file; do not use `/tmp` for final audio, transcripts, manifests, chunks, or visual frames.

```bash
if [ -n "${PI_SESSION_FILE:-}" ]; then
  SESSION_OUTPUT_DIR="$(dirname "$PI_SESSION_FILE")/video-summary/${PI_SESSION_ID:-current}/$(date -u +%Y%m%dT%H%M%SZ)"
else
  SESSION_OUTPUT_DIR="$PWD/video-summary"
fi
mkdir -p "$SESSION_OUTPUT_DIR"

python3 ~/.hermes/skills/media/video-summary/scripts/video-url-to-transcript.py \
  "VIDEO_URL_1" "VIDEO_URL_2" "VIDEO_URL_3" \
  --output-dir "$SESSION_OUTPUT_DIR" \
  --asr whisper \
  --workers 32
```

For a single URL, use the same `SESSION_OUTPUT_DIR`; for multiple URLs, the script creates `item_01/`, `item_02/`, etc. beneath it. This keeps every artifact for the run inside the current Pi session while preventing later runs in the same session from overwriting earlier results.

`--workers` controls concurrent download/FFmpeg preparation, not GPU inference. All Whisper jobs from all URLs enter one global FIFO queue and are handled by one persistent Whisper Turbo worker. Use a lower value such as 8 if network, disk, or CPU pressure is high; 32 is safe for GPU serialization but may be unnecessarily aggressive for downloads.

For Taiwanese Hokkien, use `--asr breeze`:

```bash
python3 ~/.hermes/skills/media/video-summary/scripts/video-url-to-transcript.py \
  "VIDEO_URL_1" "VIDEO_URL_2" \
  --output-dir "$SESSION_OUTPUT_DIR" \
  --asr breeze \
  --workers 1
```

For multiple URLs, each item is written under `item_01/`, `item_02/`, etc., and a `batch-manifest.json` is created. Preparation can run concurrently, while the single GPU worker processes the global Whisper queue one chunk at a time.

The command:
1. Downloads the source with `yt-dlp`, then deletes the source video after audio extraction.
2. Converts audio to `audio.mp3` and an ASR-compatible `audio.ogg`.
3. Splits Whisper input into five-minute chunks and enqueues all chunks globally across all URLs.
4. Loads `whisper-large-v3-turbo` once, processes queued chunks serially, and closes after the queue is drained.
5. Writes each chunk result plus `transcript.txt`, `transcript.json`, and `manifest.json`.

Completed chunk JSON files are reused, so an interrupted batch can continue without re-transcribing finished chunks. `Ctrl-C`/`SIGTERM` causes the worker process to exit after its pipe closes; `SIGKILL` cannot be intercepted, but the OS reclaims the GPU memory.

Audio is the default. Only when the user explicitly requests visual/video recognition, pass `--visual-frames 12` (or a larger number), inspect the extracted `visual-frames/frame_*.jpg` images with vision, and add visible people, objects, on-screen text, demonstrations, scene changes, and visual claims to the summary. Use `--visual-frames 0` for explicit audio-only processing.

`YOUTUBE_SUMMARY_YT_DLP`, `YOUTUBE_SUMMARY_PYTHON`, `YOUTUBE_SUMMARY_WHISPER_MODEL`, and `HF_HOME` may override local defaults. The script uses the existing `youtube-summary.py` Whisper worker and never invokes the standalone `whisper` CLI.

## Agent response

After the command completes, read every item's `manifest.json`, `transcript.txt`, and timestamped JSON. Read visual frame images only if visual recognition was explicitly requested and frames were generated. You must tell the user what each item is about, not merely report that downloading/transcription succeeded. Respond inline in the user's language with, for each URL:

1. A clear one- or two-sentence explanation of the video's subject and purpose.
2. A concise complete summary (3–7 key points).
3. A timestamped section-by-section breakdown.
4. Important facts, numbers, names, and claims.
5. A conclusion and notable quotes when useful.
6. A short comparison across URLs when more than one was supplied.
7. The complete raw transcript only when explicitly requested; otherwise provide its path and do not paste tens of thousands of characters.

If transcription is empty or obviously corrupted, report the failure and do not invent what the video says.

State the local paths to the audio and transcript. Do not upload files or use an external LLM. Preserve the audio unless the user explicitly asks to delete it; delete any downloaded video artifacts if created.

## Troubleshooting

- If `yt-dlp` is not on `PATH`, set `YOUTUBE_SUMMARY_YT_DLP=$HOME/.local/bin/yt-dlp`.
- If Whisper fails to load, use the ROCm venv at `/home/chihmin/models-work/flux2/.venv-rocm72/bin/python` and a cached `whisper-large-v3-turbo` snapshot.
- If the URL is login-protected or unavailable to yt-dlp, ask the user to provide an accessible URL or local media file.
- For music/no-speech recordings, report that the transcript is empty rather than inventing content.
