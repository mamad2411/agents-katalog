---
name: audio-mixing-mastering
description: "Mix and master audio: gain staging and bus structure, EQ and compression decisions, stereo image, loudness targets (LUFS/true peak) and delivery specs per platform."
type: procedural
category: audio
domain: audio
version: 1.0.0
author: Mr-Nobody-Anonymous
license: MIT
risk: low
level: advanced
triggers:
  - loudness target lufs
  - mastering true peak
  - mix bus compression
  - spotify loudness normalization
  - podcast loudness -16 lufs
keywords:
  - mixing
  - mastering
  - lufs
  - true-peak
  - eq
  - compression
  - loudness
source: custom
enabled: true
---

# Audio Mixing and Mastering

## Purpose

Mix and master audio: gain staging and bus structure, EQ and compression decisions, stereo image, loudness targets (LUFS/true peak) and delivery specs per platform.

## When to Use

- Multitrack audio must be balanced into a finished mix.
- A master must meet a platform's loudness and peak spec.
- Tracks sound inconsistent across a playlist or album.

## When NOT to Use

- The source recording is unusable (noise, clipping) — fix at the source first.
- The task is composition or arrangement.
- Only a rough reference is needed.

## Capabilities

- Set gain staging and bus architecture for a clean mix.
- Use EQ and dynamics to solve problems rather than to add loudness.
- Control the stereo image and mono compatibility.
- Master to a stated LUFS/true-peak target with metered verification.

## Inputs

- The multitrack session and its sample rate/bit depth.
- Reference tracks and the intended playback context.
- Delivery target: podcast (-16 LUFS stereo), streaming (-14), broadcast (-23), etc.

## Workflow

1. Balance at unity with faders down and headroom on the master.
2. Fix frequency conflicts with subtractive EQ before adding anything.
3. Compress for control, then for character; check gain reduction amounts.
4. Check mono compatibility and phase on correlated sources.
5. Master with an integrated LUFS meter and a true-peak limiter; verify with the target platform's spec.

## Tools

- DAW + metering suite (Youlean, iZotope, FabFilter)
- ffmpeg `loudnorm` for batch QC
- reference tracks

## Examples

- `ffmpeg -i mix.wav -af loudnorm=I=-16:TP=-1.5:LRA=11 -ar 48000 -c:a aac -b:a 192k out.m4a`
- `ffmpeg -i master.wav -af ebur128=peak=true -f null -`
- `allskills route "master this track for spotify"`

## Safety

- Loudness war mastering is destructive: check the spec, not the competitor's loudness.
- True-peak overs cause clipping after lossy encoding — leave headroom.
- Unreferenced monitoring makes EQ decisions unreliable.

## Source

All-Skills canonical library (`skills/audio/audio-mixing-mastering`). First-party skill, maintained in this repository.

## Notes

- Integrated LUFS is the delivery metric; short-term LUFS is for live balance.
- Mix decisions that only work loud usually fall apart when turned down.
- Pairs with: `audio/music-production-daw`, `video/video-encoding-delivery`.
