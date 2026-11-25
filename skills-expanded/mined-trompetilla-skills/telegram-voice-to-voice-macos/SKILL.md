---
name: telegram-voice-to-voice-macos
description: "Telegram voice-to-voice workflow (macOS Apple Silicon only): handle incoming Telegram voice notes (.ogg), transcribe locally with yap (Speech.framework), generate a reply, and send back a Telegram voice note using local TTS (macOS say + ffmpeg). Also support /audio on and /audio off toggles with persistent per-user state. Use when you want voice-to-voice chat on Telegram without cloud transcription/TTS."
---

# Telegram voice-to-voice (macOS)

## Requirements

- macOS Tahoe on Apple Silicon (Macintosh Silicon).
- `yap` CLI available in `PATH` (Speech.framework transcription).
  - Project: https://github.com/finnvoor/yap (by finnvoor)
- `ffmpeg` available in `PATH`.

## Persistent reply mode (voice vs text)

Store a small per-user preference file in the workspace:

- State file: `voice_state/telegram.json`
- Key: Telegram sender user id (string)
- Values:
  - `"voice"` (default): reply with a Telegram voice note
  - `"text"`: reply with a single text message

If the file does not exist or the sender id is missing: assume `"voice"`.

### Toggle commands

If an inbound **text** message is exactly:

- `/audio off` → set state to `"text"` and confirm with a short text reply.
- `/audio on` → set state to `"voice"` and confirm with a short text reply.

## Getting the inbound audio (.ogg)

Telegram voice notes often show up as `<media:audio>` in message text.
OpenClaw saves the attachment to disk (typically `.ogg`) under:

- `~/.openclaw/media/inbound/`

Recommended approach:

1) If the inbound message context includes an attachment path, use it.
2) Otherwise, take the most recent `*.ogg` from `~/.openclaw/media/inbound/`.

## Transcription

Default locale: `en-US`.

Preferred:

- `yap transcribe --locale "${YAP_LOCALE:-en-US}" <path.ogg>`

If transcription fails or is empty: ask the user to repeat or send text.

Helper script:

- `scripts/transcribe_telegram_ogg.sh [path.ogg]`

## Reply behavior

### Mode: voice (default)

1) Generate the reply text.
2) Convert reply text to an OGG/Opus voice note using:

- `scripts/tts_telegram_voice.sh "<reply text>" [SYSTEM|VoiceName]`

The script prints the generated `.ogg` path to stdout.

3) Send the `.ogg` back to Telegram as a **voice note** (not a generic audio file):

- use the `message` tool with `asVoice: true` and `media: <path.ogg>`
- optionally set `replyTo` to thread the response

Notes:

- Use `SYSTEM` to rely on the current macOS system voice (recommended).

### Mode: text

Reply with a single text message:

- `Transcription: <...>`
- `Reply: <...>`
