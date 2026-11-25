---
name: video-editing-workflow
description: "Edit video professionally: project and proxy setup, codec and timebase consistency, three-point editing, multicam sync, and export handoff for grading or delivery."
type: procedural
category: video
domain: video
version: 1.0.0
author: Mr-Nobody-Anonymous
license: MIT
risk: low
level: intermediate
triggers:
  - premiere pro proxy workflow
  - davinci resolve editing
  - multicam sync editing
  - video codec mismatch
  - edit export xml to grading
keywords:
  - video-editing
  - nle
  - premiere
  - resolve
  - proxy
  - multicam
  - xml
mcp_servers:
  - davinci-resolve
source: custom
enabled: true
---

# Video Editing Workflow

## Purpose

Edit video professionally: project and proxy setup, codec and timebase consistency, three-point editing, multicam sync, and export handoff for grading or delivery.

## When to Use

- Footage must be assembled into a narrative.
- Editing stalls on high-resolution or mixed-codec media.
- An edit must hand off to grading or mixing with a timeline.

## When NOT to Use

- The task is motion graphics or VFX rather than cutting.
- Only a trim of an existing finished file is needed.
- The deliverable is audio-only.

## Capabilities

- Set up projects with consistent timebase and colour management.
- Use proxies so editing stays responsive with 4K/RAW.
- Cut with three-point editing and organise bins and markers.
- Sync multicam and hand off an XML/AAF to colour and audio.

## Inputs

- Footage, its codecs, frame rates and colour space.
- The story outline or script and target runtime.
- Delivery spec and whether grading/mixing happen elsewhere.

## Workflow

1. Create the project with the intended timebase; convert variable-frame-rate footage first.
2. Generate proxies and relink at the end of the edit.
3. Organise bins, sync audio, and mark selects before cutting.
4. Cut picture locked; add temporary music and scratch VO.
5. Export XML/AAF plus a reference render for handoff, and confirm relink in the next tool.

## Tools

- Premiere Pro / DaVinci Resolve / Final Cut
- davinci-resolve-mcp connector
- ffmpeg for proxies and QC

## Examples

- `ffmpeg -i cam.mp4 -vf scale=1280:-2 -c:v prores_ks -profile:v 0 proxy.mov`
- `ffmpeg -i final.mp4 -f null - 2>&1 | grep -i "error\|drop"`
- `allskills mcp install --harness cursor --servers davinci-resolve`

## Safety

- Mixing frame rates in one timeline causes judder and audio drift — conform first.
- Never delete original media after generating proxies, and relink before export.
- Variable-frame-rate phone footage must be transcoded to constant rate.

## MCP Requirements

| Server | Transport | Tier | Risk | Required env |
| :--- | :--- | :--- | :--- | :--- |
| `davinci-resolve` | stdio | full | medium | — |

Install the connectors above with `allskills mcp install --harness <harness> --profile full`,
or list the same ids in your harness config. Full detail per server: [`docs/MCP-CATALOG.md`](MCP-CATALOG.md) and [`mcp/registry.json`](../mcp/registry.json).

## Source

All-Skills canonical library (`skills/video/video-editing-workflow`). First-party skill, maintained in this repository.

## Notes

- Picture lock before grading or sound avoids redoing both.
- A reference render with burn-in timecode makes review notes unambiguous.
- Pairs with: `video/color-grading`, `video/video-encoding-delivery`.
