---
name: music-production-daw
description: "Produce music in a DAW: session setup and gain staging, MIDI and audio recording, arrangement, editing and comping, and project hygiene for collaboration."
type: procedural
category: audio
domain: audio
version: 1.0.0
author: Mr-Nobody-Anonymous
license: MIT
risk: low
level: intermediate
triggers:
  - daw session setup
  - gain staging mixing
  - comping vocal takes
  - midi arrangement workflow
  - ableton live session
keywords:
  - daw
  - music-production
  - midi
  - recording
  - arrangement
  - ableton
mcp_servers:
  - ableton
source: custom
enabled: true
---

# Music Production in a DAW

## Purpose

Produce music in a DAW: session setup and gain staging, MIDI and audio recording, arrangement, editing and comping, and project hygiene for collaboration.

## When to Use

- A track must be written, arranged and edited.
- Recorded takes need comping and timing correction.
- A project must be handed to a mix engineer cleanly.

## When NOT to Use

- The deliverable is a finished master (that is mixing/mastering).
- The task is sound design for picture.
- Only a reference listen is needed.

## Capabilities

- Set up a session with correct sample rate, buffer and gain staging.
- Record MIDI and audio with monitoring and latency compensated.
- Comp and edit takes without destroying alternatives.
- Prepare a session for handoff (named tracks, printed stems).

## Inputs

- The musical brief: genre, tempo, key, reference tracks.
- Available instruments/plugins and hardware.
- Deliverable: stems, session, or final mix.

## Workflow

1. Create a template: tempo map, track naming, bus structure, gain staging at -18 dBFS RMS-ish for virtual instruments.
2. Track to a click and keep a consistent bar-aligned arrangement.
3. Comp takes with playlists/lanes so every alternative stays available.
4. Arrange with markers for sections; commit decisions to keep the session lean.
5. Print stems and document tempo, key and plugin versions for handoff.

## Tools

- Ableton Live / Logic / Reaper / FL Studio
- ableton-mcp connector
- reference-metering plugin

## Examples

- `allskills mcp install --harness claude --servers ableton`
- `allskills explain audio/music-production-daw --query "gain staging"`
- `allskills route "produce a demo track"`

## Safety

- Recording without headroom clips the input and cannot be recovered.
- Unnamed tracks and plugins make handoff sessions unusable.
- Autosave and versioned copies protect against plugin crashes.

## MCP Requirements

| Server | Transport | Tier | Risk | Required env |
| :--- | :--- | :--- | :--- | :--- |
| `ableton` | stdio | full | medium | — |

Install the connectors above with `allskills mcp install --harness <harness> --profile full`,
or list the same ids in your harness config. Full detail per server: [`docs/MCP-CATALOG.md`](MCP-CATALOG.md) and [`mcp/registry.json`](../mcp/registry.json).

## Source

All-Skills canonical library (`skills/audio/music-production-daw`). First-party skill, maintained in this repository.

## Notes

- Commit decisions (freeze/print) to keep large sessions workable.
- Reference tracks on the same monitoring path calibrate your ears.
- Pairs with: `audio/audio-mixing-mastering`, `audio/podcast-production`.
