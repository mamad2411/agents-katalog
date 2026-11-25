---
name: pbr-texture-authoring
description: "Author PBR texture sets: UV/UDIM layout, base colour, roughness and metallic maps, height/normal baking, texel density and engine-correct export presets."
type: procedural
category: 3d
domain: 3d
version: 1.0.0
author: Mr-Nobody-Anonymous
license: MIT
risk: low
level: advanced
triggers:
  - substance painter workflow
  - pbr texture maps setup
  - udim texture layout
  - bake height to normal
  - texel density consistency
keywords:
  - pbr
  - texturing
  - substance
  - udim
  - normal-map
  - texel-density
source: custom
enabled: true
---

# PBR Texture Authoring

## Purpose

Author PBR texture sets: UV/UDIM layout, base colour, roughness and metallic maps, height/normal baking, texel density and engine-correct export presets.

## When to Use

- An asset needs physically consistent surface detail.
- Multiple materials must share a consistent texel density.
- Textures must export in the engine's expected channel packing.

## When NOT to Use

- Flat colours are enough for the project's art direction.
- The model has no UVs and cannot be unwrapped reliably.
- The pipeline is procedural-only shader work.

## Capabilities

- Lay out UVs/UDIMs so seams fall out of sight and density is uniform.
- Bake height/AO/curvature and derive normal, roughness and mask maps.
- Author wear and detail that reads at the target viewing distance.
- Export presets matching the engine (ORM packing, colour spaces).

## Inputs

- The asset's UV layout and texel density target.
- The engine's texture conventions and channel packing.
- Reference material photographs and the desired wear story.

## Workflow

1. Fix UVs and texel density before texturing — redoing them invalidates all work.
2. Bake the support maps from the high-poly or from geometry.
3. Author layers from large-scale variation to fine detail.
4. Export with the engine preset and verify the packed channels.
5. Check the asset in-engine under real lighting, not only in the painter.

## Tools

- Substance Painter / Quixel / Blender
- baking tools
- engine import preview

## Examples

- `npx gltf-transform optimize model.glb model.glb --texture-compress ktx2`
- `allskills explain 3d/pbr-texture-authoring --query "texel density"`
- `allskills route "texture a game prop"`

## Safety

- Inconsistent texel density between assets is the most visible quality defect.
- Exporting normal maps as sRGB breaks shading subtly and is hard to spot.
- UDIM tiles missing from an export show as black patches on the model.

## Source

All-Skills canonical library (`skills/3d/pbr-texture-authoring`). First-party skill, maintained in this repository.

## Notes

- Author at final resolution when possible; upscaling loses authored detail.
- Channel packing must match the engine exactly — it is not portable.
- Pairs with: `3d/blender-shading-materials`, `3d/three-d-asset-pipeline`.
