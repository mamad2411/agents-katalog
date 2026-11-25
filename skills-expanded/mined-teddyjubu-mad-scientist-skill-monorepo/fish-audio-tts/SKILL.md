---
name: fish-audio-tts
description: fish-audio-tts lets the user convert text into natural-sounding speech using the Fish Audio API, which is useful for creating voiceovers, audio content, or AI narration without needing a recording studio or voice actor.
---

## What This Skill Does

This skill fish-audio-tts lets the user convert text into natural-sounding speech using the Fish Audio API, which is useful for creating voiceovers, audio content, or AI narration without needing a recording studio or voice actor.

## Usage

When the user asks to:
- "Convert this to speech"
- "Make an audio file from..."
- "Text to speech..."
- "Generate voice for..."
- "Create audio of..."
- "Add narration to..."

## How It Works

1. Load API key from `~/.openclaw/.secrets/fish-audio.env`
2. Call Fish Audio TTS API with text and voice model
3. Save the returned MP3 audio file
4. Return the file path to the user

## Voice Models

Default voice: `8ef4a238714b45718ce04243307c57a7` (E-Girl Voice)

Browse voices at: https://fish.audio and copy the model ID from the URL.

## Command Line Usage

Basic usage (default voice):
```bash
cd ~/.openclaw/workspace/skills/fish-audio-tts
python3 scripts/generate_audio.py \
  --text "Your text here" \
  --output audio.mp3
```

With custom voice:
```bash
python3 scripts/generate_audio.py \
  --text "Your text here" \
  --voice "voice_model_id" \
  --output audio.mp3
```

## API Details

- **Endpoint:** `https://api.fish.audio/v1/tts`
- **Method:** POST
- **Headers:** 
  - `Authorization: Bearer YOUR_API_KEY`
  - `Content-Type: application/json`
- **Body:**
  ```json
  {
    "text": "Your text here",
    "reference_id": "voice_model_id"
  }
  ```
- **Response:** Audio file (MP3 format, 128 kbps, 44.1 kHz)

## Requirements

✅ API key stored in `~/.openclaw/.secrets/fish-audio.env`:
```bash
FISH_AUDIO_API_KEY=your_key_here
```

✅ Python 3 with `requests` library

## Example Workflow

**User:** "Add narration to this clip: 'Welcome to the Real Deal Meetup!'"

**Agent:**
1. Runs: `python3 scripts/generate_audio.py --text "Welcome to the Real Deal Meetup!" --output narration.mp3`
2. Replies: "✅ Narration generated! Saved to `narration.mp3` (45.2 KB)"

## Testing

Test the API key:
```bash
cd ~/.openclaw/workspace/skills/fish-audio-tts
python3 scripts/generate_audio.py \
  --text "Testing Fish Audio TTS" \
  --output test.mp3
```

## Cost

Usage-based pricing. Check your Fish Audio account for credits/billing.

## Configuration

API key location: `~/.openclaw/.secrets/fish-audio.env`

File permissions should be `600` (readable only by owner):
```bash
chmod 600 ~/.openclaw/.secrets/fish-audio.env
```
