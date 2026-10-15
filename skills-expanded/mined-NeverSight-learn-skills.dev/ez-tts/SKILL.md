---
name: ez-tts
description: Local text-to-speech using Kyutai Pocket TTS. Fast CPU-based TTS with 8 preset voices and voice cloning support. Runs fully offline after model download.
---

# ez-tts - Local Text-to-Speech

Local text-to-speech using Kyutai's Pocket TTS. **Fully offline** after initial model download. ~10x realtime on CPU, no GPU needed.

## Usage

```bash
# Basic (outputs to /tmp/tts_output.wav)
uv run scripts/tts.py "Hello, this is a test"

# Specify preset voice
uv run scripts/tts.py "Hello world" --voice marius

# Custom output file
uv run scripts/tts.py "Hello world" --out ~/my_audio.wav

# Output as OGG (for voice messages, requires ffmpeg)
uv run scripts/tts.py "Hello world" --ogg

# Voice cloning (requires HF_TOKEN)
uv run scripts/tts.py "Hello world" --voice /path/to/sample.ogg
```

## Preset Voices

| Voice | Description |
|-------|-------------|
| `alba` | Female, neutral American (default) |
| `marius` | Male, casual |
| `javert` | Male, authoritative |
| `jean` | Male, warm |
| `fantine` | Female, expressive |
| `cosette` | Female, gentle |
| `eponine` | Female, British |
| `azelma` | Female, youthful |

Custom cloned voices can be placed in the skill's `voices/` directory and used by name (e.g., `--voice myvoice` if `voices/myvoice.ogg` exists).

## Voice Cloning

Clone any voice from a 15-30 second audio sample:

```bash
# Use a custom voice sample for cloning
uv run scripts/tts.py "Hello world" --voice ~/voices/my_voice.ogg

# Supported formats: WAV, OGG, MP3, FLAC
```

**Requirements for voice cloning:**
- `HF_TOKEN` environment variable must be set (Hugging Face token)
- Audio sample should be 15-30 seconds of clear speech

Preset voices work without HF_TOKEN.

## Options

- `--voice/-v` — Voice name or path to audio file for cloning (default: alba)
- `--out/-o` — Output file path (default: /tmp/tts_output.wav)
- `--ogg` — Convert output to OGG format (requires ffmpeg)
- `--quiet/-q` — Suppress progress messages

## Setup

No installation needed. The script uses `uv run` with inline dependencies (PEP 723) - deps are fetched automatically on first run.

## Environment Variables

| Variable | Purpose |
|----------|---------|
| `HF_TOKEN` | Hugging Face token for voice cloning (not needed for preset voices) |
