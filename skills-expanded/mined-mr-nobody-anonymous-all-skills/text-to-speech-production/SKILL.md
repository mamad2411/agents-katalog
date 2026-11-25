---
name: text-to-speech-production
description: "Produce production text-to-speech: voice selection, SSML and pacing, chunking long scripts, loudness normalization and QA listening."
type: procedural
category: media
domain: media
version: 1.0.0
author: Mr-Nobody-Anonymous
license: MIT
risk: medium
level: intermediate
triggers:
  - text to speech production
  - elevenlabs voice clone
  - ssml pacing control
  - audio loudness normalization
  - narration chunking
keywords:
  - tts
  - voice
  - ssml
  - loudness
  - elevenlabs
  - narration
source: custom
enabled: true
---

# Production Text-to-Speech

## Purpose

Produce production text-to-speech: voice selection, SSML and pacing, chunking long scripts, loudness normalization and QA listening.

## When to Use

- Narration or voiceover must be generated at scale.
- Generated audio needs consistent loudness and pacing.
- A voice must be selected and approved before bulk generation.

## When NOT to Use

- The content requires emotive performance only a human voice actor delivers.
- The script contains pronunciation that cannot be corrected without a lexicon.
- Rights for the cloned voice are not established.

## Capabilities

- Select and audition voices against the actual script.
- Control pacing with punctuation and SSML where supported.
- Chunk long scripts at sentence boundaries and stitch seamlessly.
- Normalize loudness and verify with a listening pass.

## Inputs

- The final script, pronunciation notes and target duration.
- The output format, sample rate and loudness target (e.g. -16 LUFS).
- Voice rights: licensed, cloned with consent, or stock.

## Workflow

1. Lock the script before generating; edits invalidate every rendered clip.
2. Audition two or three voices on a representative paragraph.
3. Split the script at sentence boundaries and keep a paragraph of context.
4. Normalize loudness and trim silences consistently across chunks.
5. Listen to the assembled track end to end and log any mispronunciations.

## Tools

- ElevenLabs (or another TTS provider)
- ffmpeg for stitching and loudness
- a loudness meter

## Examples

- `allskills mcp install --harness cursor --servers elevenlabs`
- `ffmpeg -i in.wav -af loudnorm=I=-16:TP=-1.5:LRA=11 out.wav`
- `allskills route "narrate this article"`

## Safety

- Cloning a voice requires documented consent from the speaker.
- Never present synthetic audio as a real person's statement.
- Check provider terms for commercial use of generated audio.

## Source

All-Skills canonical library (`skills/media/text-to-speech-production`). First-party skill, maintained in this repository.

## Notes

- Chunking mid-sentence causes unnatural prosody; split on punctuation.
- Loudness normalization is required for consistent playback across platforms.
- Pairs with: `media/audio-transcribe`, `media/veo-video-generator`.
