---
name: sound-design-foley
description: "Create sound design and foley: field and studio recording technique, layering and editing, sync to picture, and sound-effect library metadata."
type: procedural
category: audio
domain: audio
version: 1.0.0
author: Mr-Nobody-Anonymous
license: MIT
risk: low
level: advanced
triggers:
  - foley recording setup
  - sound design layering
  - sound effects sync to picture
  - field recording technique
  - sfx library metadata
keywords:
  - sound-design
  - foley
  - field-recording
  - sfx
  - layering
  - sync
source: custom
enabled: true
---

# Sound Design and Foley

## Purpose

Create sound design and foley: field and studio recording technique, layering and editing, sync to picture, and sound-effect library metadata.

## When to Use

- A film, game or video needs custom sound effects.
- Existing library sounds do not fit the picture.
- Footsteps, cloth and props must be performed to picture.

## When NOT to Use

- A licensed library sound is adequate and faster.
- The task is music composition.
- The picture is not locked, so sync work would be redone.

## Capabilities

- Record clean source material with correct mic technique and levels.
- Layer elements (transient, body, tail) for a convincing whole.
- Edit and sync to picture with frame-accurate placement.
- Metadata and organise a reusable library.

## Inputs

- Locked picture with timecode and frame rate.
- The required sound list (impacts, ambience, cloth, footsteps).
- Delivery format and stem requirements.

## Workflow

1. Wait for picture lock; sound design on a moving cut is wasted work.
2. Record or source each element separately with clean headroom.
3. Layer transient, body and tail; pitch and time-shift to fit.
4. Sync to frame-accurate positions and check against picture at full speed.
5. Name, tag and store assets with sample rate, channel layout and licence.

## Tools

- field recorder + mics
- DAW for editing
- sound library with metadata (e.g. Soundly)

## Examples

- `ffmpeg -i scene.mp4 -itsoffset 0.042 -i impact.wav -c:v copy -c:a aac out.mp4`
- `allskills explain audio/sound-design-foley --query "layer an impact"`
- `allskills route "add foley to this scene"`

## Safety

- Recording at 24-bit with headroom prevents unrecoverable clipping.
- Library licences differ for broadcast vs games — record the licence per asset.
- Always monitor on speakers and headphones; each hides different problems.

## Source

All-Skills canonical library (`skills/audio/sound-design-foley`). First-party skill, maintained in this repository.

## Notes

- Three layers (transient/body/tail) is the standard recipe for impacts.
- Metadata now saves hours when the library grows.
- Pairs with: `video/video-editing-workflow`, `audio/audio-mixing-mastering`.
