---
name: media-entertainment-ops
description: "Use when handling media and entertainment workflows from Hermes: GIF search, YouTube transcript/content transforms, Spotify playback, music generation, audio spectrogram analysis, or Pokemon/emulator play."
version: 1.0.0
author: Hermes Agent
license: MIT
---

# Media and Entertainment Operations

Class-level guide for media retrieval, playback, analysis, generation, and light entertainment automation.

## Search and content extraction
- GIF search: Tenor API via curl/jq for reaction GIF discovery and downloads. Requires `TENOR_API_KEY`.
- YouTube content: fetch transcripts and convert to summaries, chapters, threads, blog posts, or structured notes.

## Music and audio
- Spotify: control playback, devices, queue, search, playlists, albums, and library through Hermes Spotify tools.
- HeartMuLa: open-source song generation from lyrics and tags.
- songsee: spectrograms and audio features such as mel/chroma/MFCC via CLI.

## Game automation
- Pokemon player: headless Game Boy emulator/RAM-read gameplay through `pokemon-agent` and ROM files.

## Verification
- For downloads/generated media: report exact local path and stat the file.
- For playback: report the selected device/track or tool result.
- For YouTube: include transcript availability limitations and avoid inventing missing transcript text.
- For game state: read emulator/RAM state rather than guessing from prose.

## Common pitfalls
- Respect API key requirements and rate limits.
- Keep copyrighted transcript/media transformations bounded to what tools actually retrieved.
- Distinguish media analysis from creative visual production; use the visual umbrella when the deliverable is an image/video artifact.
