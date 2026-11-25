---
name: houdini-procedural-vfx
description: "Build procedural effects in Houdini: SOP/DOP context, VEX, simulation caching, wedging parameters and exporting geometry or caches to other pipelines."
type: procedural
category: 3d
domain: 3d
version: 1.0.0
author: Mr-Nobody-Anonymous
license: MIT
risk: medium
level: advanced
triggers:
  - houdini procedural workflow
  - vex wrangle syntax
  - houdini simulation cache
  - wedge parameter exploration
  - houdini to blender alembic
keywords:
  - houdini
  - vfx
  - procedural
  - vex
  - simulation
  - alembic
  - cache
source: custom
enabled: true
---

# Houdini Procedural VFX

## Purpose

Build procedural effects in Houdini: SOP/DOP context, VEX, simulation caching, wedging parameters and exporting geometry or caches to other pipelines.

## When to Use

- Effects need simulation or rule-based generation at scale.
- Variation must be explored across parameter ranges reproducibly.
- Heavy geometry must be cached for a render or downstream tool.

## When NOT to Use

- The effect is simple enough for a DCC's built-in tools.
- The team has no Houdini licences or pipeline support.
- A realtime result is needed inside a game engine.

## Capabilities

- Organise SOP networks with named, cached milestones.
- Write VEX for per-primitive/per-point logic.
- Cache simulations to disk with versioned file paths.
- Wedge parameters to compare variants systematically.

## Inputs

- The effect specification and its visual target reference.
- Simulation scale, frame range and resolution.
- Delivery format: alembic, USD, or rendered passes.

## Workflow

1. Block the effect at low resolution and lock the look before simulating at full quality.
2. Cache intermediate geometry at named SOPs so re-simulation is cheap.
3. Simulate and cache to a versioned directory; never simulate twice for the same shot.
4. Wedge the key parameters and compare renders side by side.
5. Export alembic/USD with explicit frame ranges and check in the destination tool.

## Tools

- Houdini (SOP/DOP/VEX)
- husk/rendering
- alembic/USD export

## Examples

- `houdini -batch -execute "hou.hipFile.load('fx.hip')"  # via hython script`
- `allskills explain 3d/houdini-procedural-vfx --query "cache simulation"`
- `allskills route "procedural destruction effect"`

## Safety

- Full-resolution simulations without caching waste hours on re-runs.
- Missing frame ranges in exports truncate effects silently.
- Scale errors in simulation setups make physics implausible.

## Source

All-Skills canonical library (`skills/3d/houdini-procedural-vfx`). First-party skill, maintained in this repository.

## Notes

- Cache at every stable stage; simulation is the most expensive step to repeat.
- Wedge renders answer creative questions faster than guessing parameters.
- Pairs with: `3d/vfx-compositing`, `3d/blender-geometry-nodes`.
