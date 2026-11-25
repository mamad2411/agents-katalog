---
name: blender-modeling-topology
description: "Model clean assets in Blender: quad topology and edge flow, subdivision and creasing, non-destructive modifier stacks, UV unwrapping and scale discipline."
type: procedural
category: 3d
domain: 3d
version: 1.0.0
author: Mr-Nobody-Anonymous
license: MIT
risk: low
level: intermediate
triggers:
  - blender modeling topology
  - blender subdivision surface
  - blender uv unwrap seams
  - blender hard surface modeling
  - blender modifier stack
aliases:
  - blender
keywords:
  - blender
  - 3d
  - modeling
  - topology
  - uv
  - subdivision
  - retopology
mcp_servers:
  - blender
source: custom
enabled: true
---

# Blender Hard-Surface and Organic Modeling

## Purpose

Model clean assets in Blender: quad topology and edge flow, subdivision and creasing, non-destructive modifier stacks, UV unwrapping and scale discipline.

## When to Use

- A game or render asset must deform, subdivide or bake cleanly.
- Silhouette and shading need to hold at multiple distances.
- An imported mesh has bad topology and needs to be rebuilt.

## When NOT to Use

- The object is a background prop that only needs a silhouette.
- The target is CAD-accurate manufacture — use a CAD modeller.
- You need organic detail beyond a practical poly budget — sculpt instead.

## Capabilities

- Build quad-dominant topology with edge loops supporting deformation.
- Control subdivision with creases and holding loops instead of extra geometry.
- Unwrap with deliberate seams and check texel density is consistent.
- Keep a non-destructive modifier stack that others can follow.

## Inputs

- The asset's role: hero, gameplay, background, or print.
- Target poly budget and the engine/renderer that consumes it.
- Real-world dimensions and the unit scale of the scene.

## Workflow

1. Set the unit scale and reference dimensions before modelling.
2. Block the primary forms, then secondary, then detail — never detail first.
3. Keep the modifier stack readable (Mirror, Subsurf, Bevel) with named modifiers.
4. Unwrap and pack UVs, then verify texel density matches other assets.
5. Test the silhouette from the actual viewing distance and check normals.

## Tools

- Blender (Edit Mode, Modifiers, UV Editor)
- blender-mcp connector
- mesh checkers (MeshLab, Blender 3D-Print toolbox)

## Examples

- `blender -b scene.blend -P check_mesh.py`
- `allskills mcp install --harness cursor --servers blender`
- `allskills route "model a game-ready crate"`

## Safety

- Boolean and bevel stacks that are unapplied can silently produce non-manifold geometry.
- Inconsistent normals ruin shading and printability — recalculate outside.
- Non-uniform object scale breaks modifiers and physics; apply scale first.

## MCP Requirements

| Server | Transport | Tier | Risk | Required env |
| :--- | :--- | :--- | :--- | :--- |
| `blender` | stdio | standard | medium | `BLENDER_HOST`, `BLENDER_PORT` |

Install the connectors above with `allskills mcp install --harness <harness> --profile full`,
or list the same ids in your harness config. Full detail per server: [`docs/MCP-CATALOG.md`](MCP-CATALOG.md) and [`mcp/registry.json`](../mcp/registry.json).

## Source

All-Skills canonical library (`skills/3d/blender-modeling-topology`). First-party skill, maintained in this repository.

## Notes

- Edge flow matters where the mesh deforms; elsewhere density is what matters.
- N-gons are acceptable on flat, non-deforming surfaces and problematic everywhere else.
- Pairs with: `3d/blender-sculpting-retopology`, `3d/three-d-asset-pipeline`.
