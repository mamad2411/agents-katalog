---
name: video-encoding-delivery
description: "Encode and deliver video: codec and container choice, bitrate ladders, HLS/DASH packaging, caption sidecars, and verification that the file plays everywhere."
type: procedural
category: video
domain: video
version: 1.0.0
author: Mr-Nobody-Anonymous
license: MIT
risk: low
level: advanced
triggers:
  - h264 vs h265 bitrate
  - hls encoding ladder
  - web video encoding settings
  - burn captions sidecar srt
  - video delivery spec
keywords:
  - encoding
  - ffmpeg
  - hls
  - codec
  - bitrate
  - captions
  - delivery
source: custom
enabled: true
---

# Video Encoding and Delivery

## Purpose

Encode and deliver video: codec and container choice, bitrate ladders, HLS/DASH packaging, caption sidecars, and verification that the file plays everywhere.

## When to Use

- A master must be delivered to web, broadcast or a platform.
- Playback must work across devices and bandwidths.
- Accessibility requires captions and transcripts.

## When NOT to Use

- Only a private review copy is needed.
- The task is editing the timeline.
- The platform handles all transcoding from a single master.

## Capabilities

- Choose codec/container and bitrate for the delivery target.
- Produce a consistent encoding ladder for adaptive streaming.
- Package HLS/DASH and ship caption sidecars (SRT/VTT).
- Verify streams, colour tags and audio loudness before handoff.

## Inputs

- The master file, its resolution, frame rate and colour space.
- The delivery targets and their documented specs.
- Caption/subtitle requirements.

## Workflow

1. Confirm the delivery spec: codec, resolution, bitrate, audio layout, captions.
2. Encode from the highest-quality master, never from a previous encode.
3. Build the bitrate ladder from the target device range and test the lowest rung.
4. Package HLS/DASH with correct segment durations and manifests.
5. Verify with ffprobe and a real playback test on the target device.

## Tools

- ffmpeg
- packagers (Shaka, Bento4)
- ffprobe + device playback tests

## Examples

- `ffmpeg -i master.mov -c:v libx264 -preset slow -crf 20 -pix_fmt yuv420p -c:a aac -b:a 192k -movflags +faststart out.mp4`
- `ffmpeg -i master.mov -vf "scale=1280:-2" -c:v libx264 -b:v 2500k -maxrate 2675k -bufsize 5350k -c:a aac -b:a 128k 720p.mp4`
- `ffprobe -v error -show_streams out.mp4 | grep -E "codec_name|width|bit_rate"`

## Safety

- Encoding from an already-compressed file compounds artefacts.
- Missing `-pix_fmt yuv420p` breaks playback in some players and browsers.
- Wrong colour tags shift gamma on every viewer that respects them.

## Source

All-Skills canonical library (`skills/video/video-encoding-delivery`). First-party skill, maintained in this repository.

## Notes

- `+faststart` moves the moov atom so playback can begin before full download.
- Always test the lowest bitrate rung — it is where quality fails first.
- Pairs with: `video/color-grading`, `video/video-editing-workflow`.
