---
name: gemini-tts
description: >
  Generate read-aloud audio (text-to-speech) using Google Gemini TTS
  (gemini-3.1-flash-tts-preview). Automatically detects the mode from the
  input: single-speaker narration for plain text, and multi-speaker dialogue
  when the input has two "Name:" speaker labels. Supports 30 prebuilt voices,
  natural-language style control and audio tags, text or file input, and
  WAV output. Works with both the Gemini Developer API and Vertex AI.
---

# Gemini TTS - Read-Aloud Speech Skill

Use the Python script in `scripts/` to turn text into natural read-aloud audio
via Google Gemini TTS. Model: **`gemini-3.1-flash-tts-preview`** (single TTS
model — there is no Pro variant).

The mode is **automatically detected** from the input:

| Mode | When used | Voices |
|---|---|---|
| **Single-speaker** | Plain text / narration | One voice (`--voice`) |
| **Multi-speaker** | A 2-person dialogue: lines like `Name: ...` with exactly two distinct speakers | Two voices (`--speaker`) |

- Detected **2 speaker labels** → multi-speaker (2 is a hard limit)
- Detected **1 or 0** → single-speaker
- Detected **3+** → warns and falls back to single-speaker narration
- Override with `--single` / `--multi`

## Prerequisites

### 1. Install dependencies

```bash
pip install google-genai
```

### 2. Configure API credentials (one of the following)

#### Option A: Gemini Developer API (recommended for personal use)

Set the `GEMINI_API_KEY` environment variable.
Get a key at https://aistudio.google.com/apikey

```bash
export GEMINI_API_KEY="your-api-key"
```

#### Option B: Vertex AI API (for Google Cloud users)

Set `GOOGLE_CLOUD_PROJECT` and optionally `GOOGLE_CLOUD_LOCATION`.
Requires a GCP project with the Vertex AI API enabled and
Application Default Credentials configured (`gcloud auth application-default login`).

```bash
export GOOGLE_CLOUD_PROJECT="your-project-id"
export GOOGLE_CLOUD_LOCATION="us-central1"   # optional, defaults to us-central1
```

> **Priority:** If both `GOOGLE_CLOUD_PROJECT` and `GEMINI_API_KEY` are set,
> Vertex AI is used.

### 3. Optional environment variables

| Variable | Default | Description |
|---|---|---|
| `TTS_MODEL` | `gemini-3.1-flash-tts-preview` | Force a specific model |
| `AUDIO_OUTPUT_DIR` | `./gemini-tts` | Default output directory |
| `GEMINI_TTS_NO_SSL_VERIFY` | _(unset)_ | Set to `1` / `true` / `yes` to disable SSL certificate verification |

---

## Script

### `scripts/generate.py` - Text-to-speech generation

#### Basic narration (single voice)

```bash
python scripts/generate.py "Have a wonderful day!" -o hello.wav
```

#### Choose a voice and style

```bash
python scripts/generate.py "Welcome aboard!" --voice Puck --style cheerfully -o welcome.wav
```

You can also steer delivery inline with audio tags, e.g. `[whispers]`, `[shouting]`,
`[excitedly]`, or a natural-language prefix like `Say in a calm voice:`.

#### Read text from a file (good for long input)

```bash
python scripts/generate.py -f article.txt -o article.wav
```

#### Multi-speaker dialogue (auto-detected)

Given `dialogue.txt`:

```
Taro: How's it going today, Hanako?
Hanako: Not too bad, how about you?
```

```bash
python scripts/generate.py -f dialogue.txt -o conversation.wav
```

#### Assign voices to speakers explicitly

```bash
python scripts/generate.py -f dialogue.txt \
  --speaker "Taro:Kore" --speaker "Hanako:Puck" -o conversation.wav
```

#### List available voices

```bash
python scripts/generate.py --list-voices
```

#### Disable SSL verification (for corporate proxies or self-signed certs)

```bash
python scripts/generate.py "hello" --no-ssl-verify -o hello.wav
```

#### JSON output (for programmatic use)

```bash
python scripts/generate.py "hello" --json -o hello.wav
```

#### Full options

```
usage: generate.py [-h] [-f FILE] [-o OUTPUT] [--voice VOICE]
                   [--speaker "Name:Voice"] [--style STYLE]
                   [--temperature T] [--single] [--multi] [--list-voices]
                   [-v] [--json] [--no-ssl-verify] [text]

Arguments:
  text                Text to read aloud (or use -f)

Options:
  -f, --file PATH     Read input text from a file
  -o, --output PATH   Output .wav file path (auto-generated if omitted)
  --voice VOICE       Voice for single-speaker mode (default: Zephyr)
  --speaker "N:V"     Multi-speaker voice mapping "Name:Voice" (repeatable)
  --style STYLE       Style prefix for single speaker (e.g. "cheerfully")
  --temperature T     Sampling temperature (default: 1.0)
  --single            Force single-speaker mode
  --multi             Force multi-speaker mode (requires 2 "Name:" speakers)
  --list-voices       List the available prebuilt voices and exit
  -v, --verbose       Show detailed output
  --json              Output result as JSON
  --no-ssl-verify     Disable SSL certificate verification
```

> `--single` and `--multi` are mutually exclusive.

---

## Output Format

Gemini TTS returns raw PCM (`audio/L16;rate=24000`, mono). The script wraps it
in a WAV header and saves a playable **`.wav`** file (16-bit, 24 kHz, mono).

---

## Voices

30 prebuilt voices are available (e.g. **Zephyr** bright, **Puck** upbeat,
**Charon** informative, **Kore** firm, **Sulafat** warm, **Leda** youthful,
**Enceladus** breathy, **Achernar** soft). 70+ languages are supported — the
output language follows the input text's language.

See `references/voices.md` for the full voice list with characteristics and a
style / audio-tag guide.

---

## Style & Delivery Control

- **Natural-language prefix**: `Say cheerfully: ...`, `Read this slowly and calmly: ...`
  (or use `--style cheerfully`, which prepends `Say cheerfully:`).
- **Audio tags** (inline): `[whispers]`, `[shouting]`, `[laughs]`, `[excitedly]`,
  `[sarcastically]`, etc. — 200+ tags steer vocal style, pace, and delivery.
- **Multi-speaker**: label each line `Name: text`; the speaker names must match
  the `--speaker "Name:Voice"` mappings exactly.

---

## Limitations

- **Single TTS model**: `gemini-3.1-flash-tts-preview` (no Pro variant).
- **Multi-speaker cap**: at most **2** speakers per request.
- **No voice cloning**: requests to imitate a specific real person's voice are
  blocked by safety filters.

---

## Error Handling

| Error | Solution |
|---|---|
| `google-genai package not installed` | Run `pip install google-genai` |
| `No API credentials found` | Set `GEMINI_API_KEY` or `GOOGLE_CLOUD_PROJECT` |
| `Input text is empty` | Provide non-empty text via argument or `-f` |
| `Multi-speaker mode requires 2 ... speakers` | Use `Name:` labels for exactly 2 speakers, or drop `--multi` |
| `Content blocked by safety filters` | Rephrase the input (avoid impersonating real people) |
| `API rate limit reached` | Wait and retry |
| `SSL: CERTIFICATE_VERIFY_FAILED` | Use `--no-ssl-verify` or set `GEMINI_TTS_NO_SSL_VERIFY=1` |
