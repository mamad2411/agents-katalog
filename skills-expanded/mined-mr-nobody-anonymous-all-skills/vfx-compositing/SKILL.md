---
name: vfx-compositing
description: "Composite shots: multi-pass renders and AOVs, keying and rotoscoping, colour matching and grain, 2D tracking and cleanup, and delivery in the correct colour space."
type: procedural
category: 3d
domain: 3d
version: 1.0.0
author: Mr-Nobody-Anonymous
license: MIT
risk: low
level: advanced
triggers:
  - nuke compositing multi pass
  - aov compositing render
  - green screen keying edges
  - match grain comp
  - after effects compositing
keywords:
  - compositing
  - vfx
  - aov
  - keying
  - rotoscoping
  - grain
  - nuke
source: custom
enabled: true
---

# VFX Compositing

## Purpose

Composite shots: multi-pass renders and AOVs, keying and rotoscoping, colour matching and grain, 2D tracking and cleanup, and delivery in the correct colour space.

## When to Use

- CG must be integrated into live-action or multiple passes combined.
- Render artefacts need fixing without a re-render.
- A shot needs final grade, grain and delivery in a specific colour space.

## When NOT to Use

- The shot is a single finished render with no integration.
- The task is editorial cutting, which belongs in an NLE.
- The look can be fixed in-camera or in the render itself.

## Capabilities

- Combine AOVs (diffuse, specular, transmission, cryptomatte) with correct math.
- Key and refine edges, despill and rebuild lost detail.
- Match grain, black levels and lens characteristics to the plate.
- Track and stabilize in 2D, and deliver in the right colour space.

## Inputs

- The plate(s), their colour space and resolution.
- Render passes/AOVs with the same camera and frame range.
- Delivery spec: codec, bit depth, colour space, burn-ins.

## Workflow

1. Reconcile colour space and resolution between plate and render first.
2. Rebuild the beauty from AOVs and confirm the sum matches the render.
3. Key/roto with soft edges; despill without killing legitimate colour.
4. Match grain and add atmospheric integration last.
5. QC at 100% on a calibrated display and compare against the plate.

## Tools

- Nuke / Fusion / After Effects
- tracking and roto tools
- colour-managed viewers

## Examples

- `allskills explain 3d/vfx-compositing --query "aov rebuild"`
- `allskills route "composite a cg character into a plate"`
- `allskills mcp install --harness claude --servers davinci-resolve`

## Safety

- Mismatched colour space makes grain and black levels impossible to match.
- Over-keying edges creates halos that survive every later stage.
- Delivering in the wrong colour space is only obvious on someone else's screen.

## Source

All-Skills canonical library (`skills/3d/vfx-compositing`). First-party skill, maintained in this repository.

## Notes

- Cryptomatte removes most manual roto of CG elements.
- Grain must be applied after the grade, not before.
- Pairs with: `3d/blender-rendering-lighting`, `video/color-grading`.
