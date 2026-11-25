---
name: color-grading
description: "Grade video: colour-managed workflows, primary and secondary correction, shot matching, LUT discipline, scopes-based verification and grade delivery."
type: procedural
category: video
domain: video
version: 1.0.0
author: Mr-Nobody-Anonymous
license: MIT
risk: low
level: advanced
triggers:
  - davinci resolve color grade
  - shot matching grade
  - lut vs manual grade
  - scopes waveform vectorscope
  - hdr grade workflow
keywords:
  - color-grading
  - resolve
  - lut
  - scopes
  - aces
  - rec709
  - hdr
mcp_servers:
  - davinci-resolve
source: custom
enabled: true
---

# Color Grading

## Purpose

Grade video: colour-managed workflows, primary and secondary correction, shot matching, LUT discipline, scopes-based verification and grade delivery.

## When to Use

- Shots must be matched and given a consistent look.
- A film needs a colour-managed pipeline for reliable delivery.
- HDR or a specific deliverable colour space is required.

## When NOT to Use

- The footage is unexposed or clipped beyond recovery.
- Only a minor exposure trim of a finished video is needed.
- The task is compositing, not grading.

## Capabilities

- Set up a colour-managed pipeline (DaVinci Wide Gamut/ACES) before grading.
- Balance shots with primaries using scopes, not the monitor alone.
- Isolate corrections with qualifiers, windows and tracking.
- Deliver in the required colour space with correct tags.

## Inputs

- The footage, camera and its colour space/log format.
- The look reference and the delivery spec (Rec.709, HDR PQ, DCI).
- A calibrated monitoring path.

## Workflow

1. Confirm the project colour management and input colour space per camera.
2. Grade the hero shot first, then match the rest to it.
3. Use scopes: waveform for levels, vectorscope for skin-tone line, parade for balance.
4. Save stills for reference and use them to keep consistency across the timeline.
5. Render with the correct output colour space and verify the tags on the delivered file.

## Tools

- DaVinci Resolve
- davinci-resolve-mcp connector
- calibrated display + scopes

## Examples

- `allskills mcp install --harness claude --servers davinci-resolve`
- `ffprobe -v error -show_entries stream=color_space,color_primaries,color_transfer final.mp4`
- `allskills route "grade this footage and match shots"`

## Safety

- Grading on an uncalibrated display produces work that fails on other screens.
- A creative LUT applied before primary balance hides exposure problems.
- Missing colour tags cause players to render the file with wrong gamma.

## MCP Requirements

| Server | Transport | Tier | Risk | Required env |
| :--- | :--- | :--- | :--- | :--- |
| `davinci-resolve` | stdio | full | medium | — |

Install the connectors above with `allskills mcp install --harness <harness> --profile full`,
or list the same ids in your harness config. Full detail per server: [`docs/MCP-CATALOG.md`](MCP-CATALOG.md) and [`mcp/registry.json`](../mcp/registry.json).

## Source

All-Skills canonical library (`skills/video/color-grading`). First-party skill, maintained in this repository.

## Notes

- Scopes are the objective check; your eyes adapt and drift.
- Match skin tones first — everything else reads against them.
- Pairs with: `video/video-editing-workflow`, `video/video-encoding-delivery`.
