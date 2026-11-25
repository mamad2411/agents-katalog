---
name: three-d-asset-pipeline
description: "Ship 3D assets correctly: glTF/USD/FBX interchange, scale and axis conventions, LOD generation, Draco/KTX2 compression, validation and engine import checks."
type: procedural
category: 3d
domain: 3d
version: 1.0.0
author: Mr-Nobody-Anonymous
license: MIT
risk: medium
level: advanced
triggers:
  - gltf export optimization
  - 3d asset lod pipeline
  - usd vs fbx vs gltf
  - draco ktx2 compression
  - 3d asset validation
keywords:
  - gltf
  - usd
  - fbx
  - lod
  - draco
  - ktx2
  - asset-pipeline
source: custom
enabled: true
---

# 3D Asset Pipeline

## Purpose

Ship 3D assets correctly: glTF/USD/FBX interchange, scale and axis conventions, LOD generation, Draco/KTX2 compression, validation and engine import checks.

## When to Use

- Assets must move reliably between authoring tools and engines.
- Scene size or load time must come down.
- Multiple consumers need a consistent asset contract.

## When NOT to Use

- A single image render is the deliverable.
- The asset is CAD/CAM geometry, which should stay in STEP.
- No engine or runtime consumes the result.

## Capabilities

- Choose the interchange format for the consumer (glTF for web, USD for film/VFX, FBX for DCC).
- Normalize scale, axis and pivot conventions at export.
- Generate and name LODs with consistent metrics.
- Compress with Draco/KTX2 and validate that the result still loads.

## Inputs

- The consuming runtime and its supported formats/features.
- Poly, texture and draw-call budgets.
- Naming and folder conventions of the destination project.

## Workflow

1. Define the asset contract: units, up-axis, pivot, naming, LOD count.
2. Export from the authoring tool with explicit settings and record them.
3. Validate the file (schema, extensions, texture references) before integration.
4. Test import in the actual consumer, not just a viewer.
5. Measure load time and draw calls against the budget.

## Tools

- glTF-Validator / gltf-transform
- Blender exporter
- engine importers (Unity/Unreal/three.js)

## Examples

- `npx gltf-transform optimize in.glb out.glb --texture-compress ktx2 --compress draco`
- `npx gltf-validator model.glb`
- `allskills route "optimize a glb for the web"`

## Safety

- Axis/scale mismatches produce 100x models lying on their side — fix at export, not in-engine.
- Draco compression is not supported by every loader; check the target first.
- Lossy texture compression on UI or normal maps causes visible artefacts.

## Source

All-Skills canonical library (`skills/3d/three-d-asset-pipeline`). First-party skill, maintained in this repository.

## Notes

- glTF is the web default; USD scales better for complex shots.
- Validate before handing off — engine errors are far harder to trace.
- Pairs with: `3d/blender-python-scripting`, `game/asset-pipelines`.
