---
name: blender-rendering-lighting
description: "Light and render in Blender: Cycles versus EEVEE trade-offs, sampling and denoising, HDRI and three-point lighting, render layers/passes and reproducible render settings."
type: procedural
category: 3d
domain: 3d
version: 1.0.0
author: Mr-Nobody-Anonymous
license: MIT
risk: low
level: intermediate
triggers:
  - blender cycles render settings
  - blender noise reduction render
  - blender hdri lighting setup
  - eevee vs cycles
  - blender render passes compositing
keywords:
  - blender
  - rendering
  - cycles
  - eevee
  - lighting
  - denoise
  - passes
mcp_servers:
  - blender
source: custom
enabled: true
---

# Blender Rendering and Lighting

## Purpose

Light and render in Blender: Cycles versus EEVEE trade-offs, sampling and denoising, HDRI and three-point lighting, render layers/passes and reproducible render settings.

## When to Use

- An asset must be presented as a final image or turntable.
- Renders are noisy, slow, or inconsistent between frames.
- The output needs passes for compositing.

## When NOT to Use

- The deliverable is realtime in-engine only.
- A viewport screenshot is sufficient.
- Lighting design requires on-set data you do not have.

## Capabilities

- Choose Cycles or EEVEE from the requirement, not habit.
- Set sampling and denoising per noise tolerance, not by guessing.
- Light with HDRI plus shaped key/fill/rim and check exposure.
- Emit render passes and reproducible settings.

## Inputs

- Final resolution, frame count and deadline.
- Whether reflection/refraction or volumetrics are needed (Cycles territory).
- Output contract: format, colour management, alpha, passes.

## Workflow

1. Lock the colour management view transform before judging the image.
2. Block light with an HDRI, then refine with shaped lights.
3. Set samples low, measure noise, raise only as needed with denoising.
4. Render layers/passes separately so compositing can fix rather than re-render.
5. Save the .blend with the exact settings and record hardware/time.

## Tools

- Blender Cycles/EEVEE
- HDRI library
- render farm or local GPU

## Examples

- `blender -b scene.blend -o //render/frame_#### -F PNG -a`
- `allskills explain 3d/blender-rendering-lighting --query "reduce noise"`
- `allskills mcp install --harness cursor --servers blender`

## Safety

- Denoising hides real sampling problems at the cost of detail — check with it off first.
- High sample counts on CPU for an animation rarely finish; test one frame first.
- Colour management changes make old and new renders incomparable.

## MCP Requirements

| Server | Transport | Tier | Risk | Required env |
| :--- | :--- | :--- | :--- | :--- |
| `blender` | stdio | standard | medium | `BLENDER_HOST`, `BLENDER_PORT` |

Install the connectors above with `allskills mcp install --harness <harness> --profile full`,
or list the same ids in your harness config. Full detail per server: [`docs/MCP-CATALOG.md`](MCP-CATALOG.md) and [`mcp/registry.json`](../mcp/registry.json).

## Source

All-Skills canonical library (`skills/3d/blender-rendering-lighting`). First-party skill, maintained in this repository.

## Notes

- Render a single hero frame to final quality before committing to a sequence.
- Separate passes are cheap insurance against a re-render.
- Pairs with: `3d/vfx-compositing`, `3d/blender-shading-materials`.
