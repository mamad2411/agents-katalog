---
name: build-local
description: Guide a new developer through setting up and running FFmpegWrapper locally after cloning the repo. Use when someone asks how to set up the project, install dependencies, get it running locally, configure ffmpeg, or troubleshoot a fresh clone. Covers Python deps, ffmpeg discovery, API key config, and launching the app.
---

# Local Setup — FFmpegWrapper

## Prerequisites

Check these before anything else:

```bash
python --version        # needs 3.9+
pip --version
```

If Python is missing or outdated, direct the user to [python.org/downloads](https://www.python.org/downloads/) and stop — don't install it for them.

## 1. Install Python dependencies

```bash
cd /path/to/ffmpeg_app
pip install -e ".[dev]"
```

This installs runtime deps (`PySide6`, `openai`) and dev deps (`pytest`) in editable mode. No separate `pip install -r requirements.txt` step needed — `pyproject.toml` is the source of truth.

If the user wants runtime-only (no pytest):

```bash
pip install -r requirements.txt
```

## 2. Discover ffmpeg

The app shells out to `ffmpeg`. Check if it's available:

```bash
which ffmpeg          # macOS/Linux
where ffmpeg          # Windows
```

**If found** — nothing to do. The app will use it automatically.

**If not found** — inform the user and ask before installing. Common options:

| Platform | How to install (user must confirm) |
|----------|-------------------------------------|
| macOS    | `brew install ffmpeg` |
| Ubuntu   | `sudo apt install ffmpeg` |
| Windows  | Download from [ffmpeg.org/download.html](https://ffmpeg.org/ffmpeg.html) and add to PATH |

**Never run the install command without explicit user approval.**

If the user has ffmpeg somewhere non-standard (e.g. `/opt/homebrew/bin/ffmpeg`), they can set a custom path in the app's Settings dialog (gear icon) under "Custom ffmpeg path". This is saved to `~/.ffmpeg_app_settings.json` as `ffmpeg_path`.

## 3. Launch the app

```bash
PYTHONPATH=src python -m ffmpeg_app.main
```

The window should open. No build step is needed for local development.

## 4. Configure API keys (optional features)

API keys are entered in the Settings dialog (gear ⚙ icon, top-left). They are saved to `~/.ffmpeg_app_settings.json` — never committed to the repo.

| Feature | Required key | Where to get it |
|---------|-------------|-----------------|
| Transcription | Deepgram | [console.deepgram.com](https://console.deepgram.com) |
| Meeting notes | OpenAI | [platform.openai.com/api-keys](https://platform.openai.com/api-keys) |

Keys are optional — Compress works with no keys at all.

## 5. Verify everything works

```bash
PYTHONPATH=src python -m pytest tests/ -v
```

All tests should pass without any API keys.

## Troubleshooting

**`ModuleNotFoundError: No module named 'ffmpeg_app'`**
→ Missing `PYTHONPATH=src`. Always prefix with `PYTHONPATH=src`.

**`ModuleNotFoundError: No module named 'PySide6'`**
→ Run `pip install -e ".[dev]"` again; check you're in the right venv.

**App opens but Compress fails with `ffmpeg not found`**
→ ffmpeg is not in PATH. See step 2 above, or set a custom path in Settings.

**Transcript/Notes buttons do nothing or show an error**
→ Check that the relevant API key is set in Settings (gear icon).

**Settings not persisting between runs**
→ Settings live at `~/.ffmpeg_app_settings.json`. Check that file is writable.
