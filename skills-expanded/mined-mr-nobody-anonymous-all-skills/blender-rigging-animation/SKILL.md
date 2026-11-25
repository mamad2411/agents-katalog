---
name: blender-rigging-animation
description: "Rig and animate in Blender: armatures and bone roll, weight painting, IK/FK chains, drivers and constraints, actions and NLA, and export to game engines."
type: procedural
category: 3d
domain: 3d
version: 1.0.0
author: Mr-Nobody-Anonymous
license: MIT
risk: low
level: advanced
triggers:
  - blender rigging armature
  - blender weight painting
  - blender ik fk setup
  - blender nla actions
  - export rig to unity unreal
keywords:
  - blender
  - rigging
  - animation
  - armature
  - weights
  - ik
  - fcurves
mcp_servers:
  - blender
source: custom
enabled: true
---

# Blender Rigging and Animation

## Purpose

Rig and animate in Blender: armatures and bone roll, weight painting, IK/FK chains, drivers and constraints, actions and NLA, and export to game engines.

## When to Use

- A character or mechanical asset must be animated or exported to an engine.
- Deformation is collapsing or exploding at joints.
- Animation must be organised into clips for a runtime.

## When NOT to Use

- The asset is static and will never deform.
- Only a turntable render is needed — object-level animation is enough.
- The pipeline requires a proprietary rig format you cannot export.

## Capabilities

- Build armatures with correct bone orientation and naming.
- Weight paint and correct deformation artefacts with helper bones.
- Set up IK/FK with stable pole targets and stretch control.
- Organise actions/NLA and export clips the engine understands.

## Inputs

- The character's range of motion and the animation list.
- The target engine and its rig/scale conventions.
- Whether the rig is for film (dense, expressive) or gameplay (lean, strict).

## Workflow

1. Place joints from anatomy (or mechanical pivots), not from the mesh surface.
2. Enable X-axis mirror and consistent bone roll before building the full skeleton.
3. Bind with automatic weights, then fix problem areas manually.
4. Build controls (IK targets, pole vectors) and test extreme poses.
5. Name and export actions, then verify the clips import with correct bone names.

## Tools

- Blender armature/pose mode, Weight Paint, NLA editor
- Rigify (optional)
- engine importers (FBX/glTF)

## Examples

- `blender -b char.blend -P export_gltf.py`
- `allskills explain 3d/blender-rigging-animation --query "fix shoulder deformation"`
- `allskills mcp install --harness cursor --servers blender`

## Safety

- Bone roll errors cause mirrored axes and broken IK — set it once, verify visually.
- Automatic weights on intersecting geometry create hidden bleeding.
- Engine bone-name limits and scale conventions must be respected or clips break.

## MCP Requirements

| Server | Transport | Tier | Risk | Required env |
| :--- | :--- | :--- | :--- | :--- |
| `blender` | stdio | standard | medium | `BLENDER_HOST`, `BLENDER_PORT` |

Install the connectors above with `allskills mcp install --harness <harness> --profile full`,
or list the same ids in your harness config. Full detail per server: [`docs/MCP-CATALOG.md`](MCP-CATALOG.md) and [`mcp/registry.json`](../mcp/registry.json).

## Source

All-Skills canonical library (`skills/3d/blender-rigging-animation`). First-party skill, maintained in this repository.

## Notes

- Test extremes (full crouch, overhead reach) before polishing animation.
- Keep the deform skeleton separate from control rig for clean export.
- Pairs with: `3d/character-animation-principles`, `game/unity`.
