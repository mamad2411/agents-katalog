---
name: photography-raw-workflow
description: "Manage a RAW photography workflow: import and catalogue structure, non-destructive develop settings, colour management and soft proofing, and export presets per use."
type: procedural
category: photography
domain: photography
version: 1.0.0
author: Mr-Nobody-Anonymous
license: MIT
risk: low
level: intermediate
triggers:
  - lightroom raw workflow
  - darktable editing
  - raw color management soft proof
  - photo export presets
  - catalog backup photos
keywords:
  - photography
  - raw
  - lightroom
  - darktable
  - colour-management
  - catalog
mcp_servers:
  - filesystem
source: custom
enabled: true
---

# Photography RAW Workflow

## Purpose

Manage a RAW photography workflow: import and catalogue structure, non-destructive develop settings, colour management and soft proofing, and export presets per use.

## When to Use

- A photo library must be organised and non-destructively developed.
- Images must be delivered for print, web and archive with correct profiles.
- A shoot must be culled and delivered on a deadline.

## When NOT to Use

- Only screenshot markup is needed.
- The source files are already final JPEGs with no latitude.
- The task is video footage.

## Capabilities

- Structure a catalogue with a consistent import and naming scheme.
- Develop non-destructively with a repeatable edit order.
- Soft-proof and export with the correct colour space and sharpening.
- Back up the catalogue as carefully as the images.

## Inputs

- The shoot's raw files and the client's delivery requirements.
- Target output: print (with paper profile) or screen (sRGB).
- Storage/backup capacity and archive policy.

## Workflow

1. Import with a naming and folder convention plus a second-copy backup.
2. Cull aggressively before editing; rate and reject with consistent criteria.
3. Edit in a fixed order: profile, exposure, white balance, tone curve, colour, local adjustments.
4. Soft-proof for print and resize/sharpen per output.
5. Export with presets and verify colour profile and metadata.

## Tools

- Lightroom / darktable / Capture One
- colour-managed display
- backup tooling

## Examples

- `exiftool -r -ext CR3 -o ~/exports/%f.jpg ~/shoot/`
- `allskills explain photography/photography-raw-workflow --query "soft proof"`
- `allskills route "deliver photos for print"`

## Safety

- A single-drive library is a data loss waiting to happen; use two copies plus offsite.
- Exporting for print without the paper profile produces colour surprises.
- Destructive edits lose the original latitude — keep raws untouched.

## MCP Requirements

| Server | Transport | Tier | Risk | Required env |
| :--- | :--- | :--- | :--- | :--- |
| `filesystem` | stdio | core | low | — |

Install the connectors above with `allskills mcp install --harness <harness> --profile full`,
or list the same ids in your harness config. Full detail per server: [`docs/MCP-CATALOG.md`](MCP-CATALOG.md) and [`mcp/registry.json`](../mcp/registry.json).

## Source

All-Skills canonical library (`skills/photography/photography-raw-workflow`). First-party skill, maintained in this repository.

## Notes

- Cull before editing: time spent on images that never ship is wasted.
- Consistent export presets keep a portfolio visually coherent.
- Pairs with: `design/graphic-design`, `utilities/image`.
