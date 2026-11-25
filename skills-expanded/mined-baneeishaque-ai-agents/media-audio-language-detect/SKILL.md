---
name: media-audio-language-detect
description: Detect the spoken language from a media file's audio track using SpeechRecognition + Google Web Speech API.
category: Media-Processing
---

# Media Audio Language Detect Skill (v1)

This is a **base** skill. It extracts a short audio sample from any media file via ffmpeg, sends it to the Google Web Speech API (free, no key required), and returns the detected spoken language. Domain-agnostic — usable by any video/audio workflow that needs to determine the language of spoken content.

***

## 1. Scope & Intent

- **In scope**: Detect spoken language from any media file with an audio track. Returns BCP-47 language code, language name, confidence level, and a transcript snippet.
- **Out of scope**:
    - Full transcription (only a short sample is analyzed).
    - Language detection from text or metadata tags (use `ffprobe` for container-level language tags).
    - Offline language detection (the Google Web Speech API requires internet).

***

## 2. Environment & Dependencies

### 2.1 Runtime

- **Python 3.12+** — scripts use `argparse`, `subprocess`, `json`, `tempfile`. Verify:

  ```bash
  python3 --version
  ```

- **`ffmpeg`** — for audio sample extraction. Verify:

  ```bash
  ffmpeg -version | head -1
  ```

- **`SpeechRecognition`** — Python library wrapping Google Web Speech API. Install:

  ```bash
  pip install SpeechRecognition
  ```

  Verify:

  ```bash
  python3 -c "import speech_recognition; print('OK')"
  ```

### 2.2 Internet Access

The Google Web Speech API is a free cloud service — no API key required. The script will fail if the machine has no internet access.

***

## 3. Protocol

### 3.1 Step 1 — Detect Language

```bash
python3 .agents/skills/media-audio-language-detect/scripts/detect-audio-language.py \
  --video /path/to/media.mp4 \
  [--duration 10] \
  [--format json]
```

The script:

1. Extracts a 10-second PCM WAV sample at 16 kHz mono via ffmpeg.
2. Sends the sample to Google Web Speech API.
3. Returns the detected language and a transcript snippet.
4. Cleans up the temporary WAV file.

#### 3.1.1 Arguments

| Argument | Required | Description |
|---|---|---|
| `--video` | Yes | Path to the media file |
| `--duration` | No | Sample length in seconds (default: 10) |
| `--format` | No | `text` (default) or `json` (machine-parseable) |

#### 3.1.2 Output

**Text format:**

```
Detected language: English (en)
Confidence: high
Transcript sample: "ok so lot of options is there..."
```

**JSON format:**

```json
{
  "language_code": "en",
  "language_name": "English",
  "confidence": "high",
  "transcript_snippet": "ok so lot of options is there..."
}
```

### 3.2 Step 2 — Use the Language Code

The returned BCP-47 language code (e.g. `en`) can be passed to:

- [`youtube-video-upload`](../youtube-video-upload/SKILL.md) via `--language`
- [`youtube-video-metadata-update`](../youtube-video-metadata-update/SKILL.md) via `--language`
- Any other workflow that needs the language tag

***

## 4. Edge Cases

- **No speech detected**: If the sample contains silence, music, or non-speech audio, `recognize_google` raises `UnknownValueError`. The script automatically runs a deterministic volume analysis fallback: if `ffmpeg volumedetect` reports `mean_volume ≤ -80 dB`, the script returns `language_code = "silent"` (digital silence). If `mean_volume > -80 dB`, audio is present but speech was not recognized — ask the user for the spoken language; default to `en` if unknown. The agent does NOT need to run the fallback manually — the script handles it.
- **Short files**: If the media file is shorter than `--duration`, ffmpeg extracts whatever is available. The script still processes the truncated sample.
- **No audio track**: If the file has no audio stream, ffmpeg produces an empty WAV. SpeechRecognition will return `unknown`.
- **API rate limits**: Google Web Speech API has rate limits (approximately 50 requests per day for unauthenticated use). If exceeded, the `RequestError` is raised.

***

## 5. Composition by Higher-Level Skills

| Composer Skill | Composition Mechanism |
|---|---|
| [`youtube-video-upload`](../youtube-video-upload/SKILL.md) | Calls `scripts/detect-audio-language.py` during pre-processing to auto-detect the video's spoken language before constructing the upload command with `--language`. |
