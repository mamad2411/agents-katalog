---
name: ez-stt
description: Local speech-to-text with selectable backends - Parakeet (best accuracy) or Whisper (fastest, multilingual).
---

# ez-stt - Local Speech-to-Text

Unified local speech-to-text using ONNX Runtime with int8 quantization. Choose your backend:

- **Parakeet** (default): Best accuracy for English, correctly captures names and filler words
- **Whisper**: Fastest inference, supports 99 languages

Requires `ffmpeg` installed.

## Usage

```bash
# Default: Parakeet v2 (best English accuracy)
scripts/stt.py audio.ogg

# Explicit backend selection
scripts/stt.py audio.ogg -b whisper
scripts/stt.py audio.ogg -b parakeet -m v3

# Quiet mode (suppress progress)
scripts/stt.py audio.ogg --quiet
```

## Options

- `-b/--backend`: `parakeet` (default), `whisper`
- `-m/--model`: Model variant (see below)
- `--no-int8`: Disable int8 quantization
- `-q/--quiet`: Suppress progress
- `--room-id`: Matrix room ID for direct message

## Models

### Parakeet (default backend)
| Model | Description |
|-------|-------------|
| **v2** (default) | English only, best accuracy |
| v3 | Multilingual |

### Whisper
| Model | Description |
|-------|-------------|
| tiny | Fastest, lower accuracy |
| **base** (default) | Good balance |
| small | Better accuracy |
| large-v3-turbo | Best quality, slower |

## Benchmark (24s audio)

| Backend/Model | Time | RTF | Notes |
|---------------|------|-----|-------|
| Whisper Base int8 | 0.43s | 0.018x | Fastest |
| **Parakeet v2 int8** | 0.60s | 0.025x | Best accuracy |
| Parakeet v3 int8 | 0.63s | 0.026x | Multilingual |

## OpenClaw

See [OPENCLAW.md](references/OPENCLAW.md) for OpenClaw-specific setup and `openclaw.json` configuration.
