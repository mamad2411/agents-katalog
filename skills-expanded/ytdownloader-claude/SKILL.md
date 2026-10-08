# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

CLI utility for downloading YouTube videos in MP4 format. Uses yt-dlp as a Python library (not subprocess) and click for CLI. All output is re-encoded to H.264+AAC via ffmpeg for universal player compatibility.

## Commands

```bash
# Install dependencies
uv sync

# Run the CLI
uv run ytdownloader <URL> [-o <output-dir>]

# Run all tests
uv run pytest tests/ -v

# Run a single test file or test
uv run pytest tests/test_validator.py -v
uv run pytest tests/test_validator.py::TestValidateUrl::test_short_url -v
```

## Architecture

The app follows a pipeline: **validate URL → fetch info → select quality → download**.

- `cli.py` — Entry point (`main`), wires the full pipeline, handles Ctrl+C
- `validator.py` — YouTube URL validation and video ID extraction. Supports `/watch`, `/embed`, `/shorts`, `youtu.be`. Raises `ValidationError`
- `info.py` — Fetches video metadata via `yt_dlp.YoutubeDL.extract_info`. Groups formats by resolution preferring H.264 (avc1). Raises `VideoInfoError`
- `downloader.py` — Downloads via yt-dlp with progress hook, re-encodes to H.264+AAC via ffmpeg postprocessor. Handles filename sanitization and deduplication

Each module defines its own exception type; `cli.py` catches them and exits with user-friendly messages.

## Key Design Decisions

- **Always re-encode to H.264+AAC** — YouTube serves VP9/Opus for high resolutions, which QuickTime and many players can't open. The `postprocessor_args` in `download_video` force `libx264 -crf 18` + `aac -b:a 192k`.
- **ffmpeg is required** — Checked at startup with `shutil.which("ffmpeg")`.
- **Format grouping** — `_build_quality_options` deduplicates by resolution height, preferring avc1 codec, then formats with audio.

## Language

User-facing messages and UI are in Russian.
