---
name: live-streaming-broadcast
description: "Produce a reliable live stream: encoder settings, scene and audio routing, bitrate ladder, latency targets and failure recovery."
type: procedural
category: video
domain: video
version: 1.0.0
author: Mr-Nobody-Anonymous
license: MIT
risk: medium
level: intermediate
triggers:
  - set up obs stream
  - twitch youtube stream settings
  - stream bitrate and keyframe
  - live stream audio delay
  - rtmp srt ingest
aliases:
  - obs
  - livestream
keywords:
  - streaming
  - obs
  - rtmp
  - srt
  - bitrate
  - encoder
  - broadcast
source: custom
enabled: true
---

# Live Streaming and Broadcast

## Purpose

Produce a reliable live stream: encoder settings, scene and audio routing, bitrate ladder, latency targets and failure recovery.

## When to Use

- An event must go out live to one or more platforms.
- The stream stutters, desyncs audio or drops during the broadcast.
- Multiple destinations need different bitrates and aspect ratios.

## When NOT to Use

- The recording is post-produced and published later.
- A one-off screen recording with no audience.
- The platform's own web broadcaster already meets the requirement.

## Capabilities

- Choose encoder, resolution, bitrate and keyframe interval per platform.
- Route scenes, overlays and audio with correct monitoring.
- Fix audio/video drift and lip-sync offsets.
- Plan redundant ingest and a recovery path.

## Inputs

- Upload bandwidth measured at the venue, not at the office.
- Platform ingest limits and required keyframe interval (often 2 s).
- The content plan: camera angles, screen shares, intermission media.

## Workflow

1. Measure sustained upload with a real speed test and plan for 60% of it.
2. Pick CBR with a 2 s keyframe interval, hardware encoding if stable.
3. Build scenes and test the full chain to the platform's preview before doors open.
4. Set audio offset with a clap test; monitor the programme feed, not the source.
5. Record locally in parallel as the archive and the fallback.
6. Have a documented recovery: who reloads the stream, on which machine.

## Tools

- obs
- ffmpeg
- nginx-rtmp
- srt

## Examples

- ``ffmpeg -re -i in.mp4 -c:v libx264 -b:v 4500k -g 60 -c:a aac -b:a 160k -f flv rtmp://…` mirrors the encoder settings OBS would use.`
- `A 1080p60 stream at 6 Mbps needs ~10 Mbps of stable upload; below that drop to 720p60.`

## Safety

- Never stream copyrighted music or footage without a licence.
- Do not expose private screens, notifications or credentials on air.

## Source

All-Skills canonical library (`skills/video/live-streaming-broadcast`). First-party skill, maintained in this repository.

## Notes

- Wi-Fi is the usual culprit; bonded or wired uplink is the fix.
- Local recording saves the archive when the uplink fails.
- Pairs with: `video-encoding-delivery`, `video-editing-workflow`.
