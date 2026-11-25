---
name: yt-dlp-superpowers
description: >-
  Use this skill when the user wants yt-dlp Superpowers: download, inspect, archive, transcribe, or extract media from YouTube or other yt-dlp-supported sites using local yt-dlp. Includes workflows for video, audio, subtitles, metadata, playlists, exact Markdown transcripts, and handoffs to watch-video, perfect-cuts, or re-light.
metadata:
  short-description: Download, inspect, transcribe, and hand off media
---

# yt-dlp Superpowers

Use the local `yt-dlp` CLI for downloading, inspecting, archiving, and extracting media from supported sites.

## First checks

1. Confirm `yt-dlp` is available, preferring the Python package when present:
   ```bash
   python3 -m yt_dlp --version || yt-dlp --version
   ```
2. If the user asks for downloads, save outputs in a task-specific folder unless they provide a destination. In Codex projectless threads, prefer `outputs/` for user-facing files.
3. Avoid downloading private, paywalled, or copyrighted media unless the user indicates they own it, have permission, or are only doing an allowed personal/archive use.
4. If the user asks for a transcript, produce an exact transcript artifact when policy and permissions allow it. Do not substitute a summary, notes, workflow extraction, or paraphrase and label it as a transcript.

## Common Commands

Inspect a URL without downloading:

```bash
yt-dlp --dump-json --no-playlist "URL"
yt-dlp -F "URL"
```

Download a single best-quality video:

```bash
yt-dlp -P "DEST_DIR" -o "%(title).200B [%(id)s].%(ext)s" "URL"
```

Download audio as MP3:

```bash
yt-dlp -x --audio-format mp3 --audio-quality 0 -P "DEST_DIR" -o "%(title).200B [%(id)s].%(ext)s" "URL"
```

Download subtitles with metadata:

```bash
yt-dlp --write-subs --write-auto-subs --sub-langs "en.*" --write-info-json --write-thumbnail -P "DEST_DIR" "URL"
```

Download a playlist safely:

```bash
yt-dlp --yes-playlist --download-archive "DEST_DIR/archive.txt" -P "DEST_DIR" -o "%(playlist_index)03d - %(title).180B [%(id)s].%(ext)s" "URL"
```

## Helper Script

Use `scripts/ytdlp_job.sh` for predictable task folders:

```bash
scripts/ytdlp_job.sh inspect "URL"
scripts/ytdlp_job.sh video "URL" "DEST_DIR"
scripts/ytdlp_job.sh audio "URL" "DEST_DIR"
scripts/ytdlp_job.sh subs "URL" "DEST_DIR"
scripts/ytdlp_job.sh transcript "URL" "DEST_DIR"
scripts/ytdlp_job.sh transcript-json "URL" "DEST_DIR"
scripts/ytdlp_job.sh transcript-md "URL" "DEST_DIR"
scripts/ytdlp_job.sh playlist "URL" "DEST_DIR"
```

The script creates the destination folder and uses stable filenames with the media ID included.

Use `transcript` when the user wants a transcript and wants local transcription as a backup:

1. It first tries to download English subtitles/auto-subs with `yt-dlp`.
2. If no subtitle file is saved, it downloads audio.
3. It hands the downloaded audio to the global `transcribe` skill and `gpt-transcribe` for the canonical transcript. Local WhisperX/Whisper is retained as a compatibility fallback and for `transcript-json`, where local word timing is required.
4. It writes an exact Markdown transcript file ending in `.transcript.md` from the captions or local transcription output.

Use `transcript-md` when captions or transcription text already exist in the destination folder and you only need to convert them into an exact Markdown transcript.

Use `transcript-json` when a downstream tool needs machine-readable timing. It runs the same captions-first workflow, keeps the exact Markdown artifact, and adds a `.transcript.json` file with a stable `1.0` schema, timed segments, timed words, provenance, and timing confidence. WhisperX word timing is preserved; caption cue timing is converted to estimated word timing and labeled accordingly.

For transcript jobs:

- "Transcript" means exact caption/transcription text, with timing markup removed and rolling-caption duplicates cleaned up. It does not mean a summary.
- If the user wants both an exact transcript and a summary, create two separate files and name them clearly, for example `Title [id].transcript.md` and `Title [id].summary.md`.
- If permissions or policy prevent providing the full exact transcript, stop and ask the user to confirm they own or have permission to reproduce the transcript. Do not silently create a summary instead.
- If you create a summary, notes, or workflow extraction, never put `transcript` in the filename or heading unless an exact transcript is also present.

The helper detects `whisperx`/`whisper` from overrides, `PATH`, and common local installs:

```text
$WHISPERX_BIN
$WHISPER_BIN
$HOME/.local/bin/whisperx
$HOME/.local/bin/whisper
$HOME/.buttercut/venv/bin/whisperx
$HOME/.perfect-cuts/venv/bin/whisperx
$HOME/GitHub/Marketing Assets and Skills/.venv-whisperx/bin/whisperx
$HOME/Library/Python/3.9/bin/whisperx
$HOME/Library/Python/3.9/bin/whisper
```

Optional environment overrides:

```bash
YTDLP_BIN=/path/to/yt-dlp
WHISPERX_BIN=/path/to/whisperx
WHISPER_BIN=/path/to/whisper
WHISPER_MODEL=base
WHISPER_DEVICE=cpu
WHISPER_COMPUTE_TYPE=int8
```

The helper detects `yt-dlp` in this order:

```text
$YTDLP_BIN
python3 -m yt_dlp
yt-dlp on PATH
```

Prefer the Python package path when it is newer than a Homebrew or system `yt-dlp` executable.

## Practical Workflow

- For a new URL, inspect first when format, playlist behavior, or site support is unclear.
- If a command fails, rerun with `--verbose` and read the site-specific error before changing flags.
- For YouTube playlists, ask or infer whether the user wants the whole playlist; otherwise add `--no-playlist`.
- For transcript/subtitle jobs, prefer `scripts/ytdlp_job.sh transcript` so subtitles are tried first, `gpt-transcribe` is used when captions are unavailable, and an exact Markdown transcript is written.
- When returning results, include the exact saved path to the `.transcript.md` file and note whether subtitles, thumbnails, or metadata were included.

## Handoff To watch-video

If the user explicitly asks to "Watch Video", "watch-video", inspect what is visible, compare visuals to transcript, or analyze screen content:

1. Use this skill to download or inspect the media only if a local file is needed.
2. Hand the URL or downloaded local file path to the `watch-video` skill.
3. Let `watch-video` create the transcript-plus-screenshot evidence bundle.

## Handoff To perfect-cuts

If the user asks to download a video and then clean cut, perfect cut, remove retakes, rough cut, or gling it:

1. Use this skill to download the source video locally.
2. Hand the downloaded local video path to the `perfect-cuts` skill.
3. Do not use yt-dlp captions as the cut timing source; `perfect-cuts` should use WhisperX plus waveform analysis.

## Handoff To re-light

If the user asks to download a short clip and then relight, re-scene, change lighting, make it cinematic, or place the subject in a new environment:

1. Use this skill to download the source video locally.
2. If the clip is longer than 10 seconds, ask the user to choose or trim a 3-10 second segment before invoking `re-light`.
3. Hand the downloaded local video path and the requested look/scene prompt to the `re-light` skill.
4. Respect `re-light`'s still-image approval gate before any paid video generation step.

## Upstream Reference

For yt-dlp source inspection, supported-site docs, or examples, use the upstream project:

```text
https://github.com/yt-dlp/yt-dlp
```
