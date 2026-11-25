---
name: blender-shading-materials
description: "Author Blender materials: Principled BSDF parameters, PBR texture wiring, colour space handling, procedural textures, and material export compatibility."
type: procedural
category: 3d
domain: 3d
version: 1.0.0
author: Mr-Nobody-Anonymous
license: MIT
risk: low
level: intermediate
triggers:
  - blender principled bsdf
  - blender normal map setup
  - color space non-color data
  - procedural material blender
  - export material to gltf
keywords:
  - blender
  - shading
  - pbr
  - materials
  - normal-map
  - color-space
mcp_servers:
  - blender
source: custom
enabled: true
---

# Blender Shading and Materials

## Purpose

Author Blender materials: Principled BSDF parameters, PBR texture wiring, colour space handling, procedural textures, and material export compatibility.

## When to Use

- An asset must look correct in Cycles, EEVEE and the target engine.
- Textures look washed out or flat after import.
- Materials must survive glTF/FBX export.

## When NOT to Use

- Only silhouette matters and flat shading is acceptable.
- The pipeline is a custom shader in an engine, not Blender materials.
- The task is compositing rather than surface definition.

## Capabilities

- Wire base colour, roughness, metallic, normal and occlusion correctly.
- Set colour space per map (Non-Color for data, sRGB for albedo).
- Build procedural detail that bakes to textures where needed.
- Keep node graphs export-compatible for glTF/FBX.

## Inputs

- The texture set and which maps exist.
- Target renderer(s) and whether export to an engine is required.
- Physically plausible values: roughness, IOR, metallic ranges.

## Workflow

1. Set up one reference material with verified texture colour spaces.
2. Wire maps into Principled BSDF; keep node names/UVs consistent.
3. Check under neutral lighting before judging colour.
4. Bake procedural nodes to textures if the target engine cannot evaluate them.
5. Verify export by importing the glTF back into a clean scene.

## Tools

- Blender Shader Editor
- texture baking (Cycles)
- glTF material validator

## Examples

- `blender -b scene.blend -P bake_material.py`
- `allskills explain 3d/blender-shading-materials --query "normal map looks wrong"`
- `allskills mcp install --harness claude --servers blender`

## Safety

- Normal/roughness/metallic maps must be Non-Color or they are gamma-corrected twice.
- Unsupported shader nodes are dropped on glTF export, changing the look.
- Over-bright albedo with high metallic produces physically implausible results.

## MCP Requirements

| Server | Transport | Tier | Risk | Required env |
| :--- | :--- | :--- | :--- | :--- |
| `blender` | stdio | standard | medium | `BLENDER_HOST`, `BLENDER_PORT` |

Install the connectors above with `allskills mcp install --harness <harness> --profile full`,
or list the same ids in your harness config. Full detail per server: [`docs/MCP-CATALOG.md`](MCP-CATALOG.md) and [`mcp/registry.json`](../mcp/registry.json).

## Source

All-Skills canonical library (`skills/3d/blender-shading-materials`). First-party skill, maintained in this repository.

## Notes

- Judge materials under a neutral HDRI before comparing to references.
- Export compatibility is a design constraint, not an afterthought.
- Pairs with: `3d/pbr-texture-authoring`, `3d/three-d-asset-pipeline`.
