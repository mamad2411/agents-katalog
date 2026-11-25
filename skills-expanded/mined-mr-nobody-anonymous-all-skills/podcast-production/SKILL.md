---
name: podcast-production
description: "Produce a podcast end to end: recording setup and remote capture, editing and cleanup, loudness-normalised delivery, chapters, transcripts and distribution."
type: procedural
category: audio
domain: audio
version: 1.0.0
author: Mr-Nobody-Anonymous
license: MIT
risk: low
level: intermediate
triggers:
  - podcast editing workflow
  - remote podcast recording
  - podcast loudness and cleanup
  - podcast chapters id3
  - podcast transcript publishing
keywords:
  - podcast
  - audio-editing
  - loudness
  - transcript
  - rss
  - id3
source: custom
enabled: true
---

# Podcast Production

## Purpose

Produce a podcast end to end: recording setup and remote capture, editing and cleanup, loudness-normalised delivery, chapters, transcripts and distribution.

## When to Use

- A spoken-word show must be recorded, edited and published.
- Multiple remote speakers need clean, separate tracks.
- Episodes need transcripts and chapters for accessibility.

## When NOT to Use

- The deliverable is music, not speech.
- A one-off voice memo is enough.
- The platform requires video-first production.

## Capabilities

- Capture local tracks per speaker for clean remote recordings.
- Edit out mistakes while preserving natural pacing.
- Normalise to podcast loudness targets with true-peak headroom.
- Produce transcripts and chapter markers.

## Inputs

- Speaker count and recording setup (local vs remote).
- Target loudness and platform spec (commonly -16 LUFS stereo).
- Distribution method: RSS host, YouTube, or internal.

## Workflow

1. Have each remote speaker record locally; sync tracks on a clap or marker.
2. Edit for content first (ums, false starts), then for noise.
3. Apply noise reduction gently; aggressive processing sounds unnatural.
4. Normalise to the target with a true-peak limiter and verify with a meter.
5. Publish with chapters, transcript and consistent show metadata.

## Tools

- remote recording (Riverside/Zencastr) or OBS per-track
- Audacity/Reaper/Descript
- ffmpeg `loudnorm`, Auphonic

## Examples

- `ffmpeg -i episode.wav -af loudnorm=I=-16:TP=-1.5:LRA=11 -c:a libmp3lame -b:a 128k episode.mp3`
- `allskills explain audio/podcast-production --query "remote tracks"`
- `allskills route "produce a podcast episode"`

## Safety

- Recording a remote call as a single mixed track limits every repair option.
- Heavy noise gate artefacts are more distracting than the noise.
- Always check the published file, not just the export dialog.

## Source

All-Skills canonical library (`skills/audio/podcast-production`). First-party skill, maintained in this repository.

## Notes

- Local per-speaker capture beats platform recording quality every time.
- Consistent intro/outro loudness is what listeners notice.
- Pairs with: `audio/audio-mixing-mastering`, `media/text-to-speech-production`.
