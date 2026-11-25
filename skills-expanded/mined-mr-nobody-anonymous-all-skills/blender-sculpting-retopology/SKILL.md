---
name: blender-sculpting-retopology
description: "Sculpt high-frequency detail in Blender and bring it back to a usable asset: dyntopo and multires, remeshing, manual retopology, normal baking and detail projection."
type: procedural
category: 3d
domain: 3d
version: 1.0.0
author: Mr-Nobody-Anonymous
license: MIT
risk: low
level: advanced
triggers:
  - blender sculpting workflow
  - blender retopology
  - blender remesh multires
  - bake normal map from high poly
  - blender dyntopo
keywords:
  - blender
  - sculpting
  - retopology
  - remesh
  - baking
  - normals
mcp_servers:
  - blender
source: custom
enabled: true
---

# Blender Sculpting and Retopology

## Purpose

Sculpt high-frequency detail in Blender and bring it back to a usable asset: dyntopo and multires, remeshing, manual retopology, normal baking and detail projection.

## When to Use

- A character or organic asset needs detail beyond subdivision modelling.
- A high-poly sculpt must become a game-ready low-poly with baked detail.
- An imported scan needs cleanup and a clean topology shell.

## When NOT to Use

- Hard-surface mechanical parts — bevel-based modelling is faster and cleaner.
- The asset is a static render where the dense sculpt can ship as-is.
- You need CAD tolerances rather than visual detail.

## Capabilities

- Choose between dyntopo, multires and voxel remesh for the job.
- Retopologise to a deformation-ready cage with correct loop density.
- Bake normal, curvature and AO maps from high to low poly.
- Preserve detail through projection and fix bake artefacts.

## Inputs

- The target poly budget and how the asset deforms.
- Whether the detail must be baked or shipped as geometry.
- Reference anatomy or design sheets.

## Workflow

1. Block the primary forms in sculpt mode before adding frequency.
2. Use voxel remesh for a uniform base, multires for layered detail.
3. Retopologise over the sculpt (or use a clean quad remesh) and check the silhouette matches.
4. Match the UV layout to the low-poly cage, then bake with correct cage/extrusion settings.
5. Inspect the bake for seams, ray misses and flipped normals before texturing.

## Tools

- Blender sculpt mode, Multires, Remesh
- Shrinkwrap and Data Transfer for projection
- bake settings in Cycles

## Examples

- `blender -b sculpt.blend --python bake_normals.py`
- `allskills explain 3d/blender-sculpting-retopology --query "bake detail"`
- `allskills mcp install --harness claude --servers blender`

## Safety

- Baking without an adequate cage ray distance produces gaps and artefacts at UV seams.
- Very dense meshes exhaust memory during remesh — decimate in stages.
- Never ship a sculpt as a rig target: deformation needs retopology.

## MCP Requirements

| Server | Transport | Tier | Risk | Required env |
| :--- | :--- | :--- | :--- | :--- |
| `blender` | stdio | standard | medium | `BLENDER_HOST`, `BLENDER_PORT` |

Install the connectors above with `allskills mcp install --harness <harness> --profile full`,
or list the same ids in your harness config. Full detail per server: [`docs/MCP-CATALOG.md`](MCP-CATALOG.md) and [`mcp/registry.json`](../mcp/registry.json).

## Source

All-Skills canonical library (`skills/3d/blender-sculpting-retopology`). First-party skill, maintained in this repository.

## Notes

- Multires preserves layered detail non-destructively; dyntopo does not.
- Bake one map set per material/UDIM tile and verify in the target engine.
- Pairs with: `3d/blender-modeling-topology`, `3d/pbr-texture-authoring`.
