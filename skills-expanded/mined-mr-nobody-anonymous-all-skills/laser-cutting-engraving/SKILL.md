---
name: laser-cutting-engraving
description: "Prepare files for laser cutting and engraving: kerf compensation, cut order, material settings, nesting and safe operation."
type: procedural
category: cad
domain: cad
version: 1.0.0
author: Mr-Nobody-Anonymous
license: MIT
risk: high
level: intermediate
triggers:
  - laser cut file preparation
  - kerf offset tolerance
  - laser settings for plywood
  - nest parts on sheet
  - laser engraving raster settings
aliases:
  - lasercut
keywords:
  - laser
  - cutting
  - engraving
  - kerf
  - nesting
  - acrylic
  - plywood
mcp_servers:
  - inkscape
source: custom
enabled: true
---

# Laser Cutting and Engraving

## Purpose

Prepare files for laser cutting and engraving: kerf compensation, cut order, material settings, nesting and safe operation.

## When to Use

- A 2D design must be cut or engraved on a laser cutter.
- Parts do not fit because kerf was ignored.
- A job needs a safe, documented material and power setting.

## When NOT to Use

- The material is PVC or another chlorine-containing plastic — it releases corrosive fumes.
- The part needs true 3D geometry; laser cutting is 2.5D.
- No ventilation or fire safety is available.

## Capabilities

- Convert artwork to cut and engrave layers with correct stroke colours.
- Compensate for kerf and predict final part dimensions.
- Order cuts inner-first and nest parts efficiently.
- Set and record parameters per material and thickness.

## Inputs

- Vector artwork with distinct layers for cut, score and engrave.
- Material, thickness and sheet size.
- The machine's power, speed, focus and ventilation setup.

## Workflow

1. Separate cut lines, score lines and raster engraving onto different layers and colours.
2. Measure kerf on a test coupon of the same material and offset the cut path by half the kerf.
3. Order cuts inner features before outer profiles so parts do not shift.
4. Nest with rotation allowed and leave at least 3 mm between parts.
5. Run a small test coupon for a new material; record power, speed, passes and focus.
6. Supervise the cut — never leave a laser unattended.

## Tools

- inkscape
- lightburn
- deepnest
- visicut

## Examples

- `A 0.15 mm kerf means a nominal 10 mm finger joint needs its slot cut at 9.85 mm to be snug.`
- `Engraving at too high a power on acrylic crazes the surface; two lighter passes are cleaner than one heavy pass.`

## Safety

- Never cut PVC, polycarbonate or unknown plastics.
- Know where the extinguisher is and keep the lid closed while cutting.

## MCP Requirements

| Server | Transport | Tier | Risk | Required env |
| :--- | :--- | :--- | :--- | :--- |
| `inkscape` | stdio | full | low | — |

Install the connectors above with `allskills mcp install --harness <harness> --profile full`,
or list the same ids in your harness config. Full detail per server: [`docs/MCP-CATALOG.md`](MCP-CATALOG.md) and [`mcp/registry.json`](../mcp/registry.json).

## Source

All-Skills canonical library (`skills/cad/laser-cutting-engraving`). First-party skill, maintained in this repository.

## Notes

- Focus height changes with material thickness; re-set it every job.
- Humidity and material batch change results — keep a settings log per batch.
- Pairs with: `vector-illustration-svg`, `cnc-machining-fabrication`.
