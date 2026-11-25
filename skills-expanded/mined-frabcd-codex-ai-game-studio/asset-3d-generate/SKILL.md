---
name: asset-3d-generate
description: "Select and run a licensed image-or-text-to-3D workflow, then validate topology, shading, UVs, LODs, collision, and engine import."
---

# Asset 3D Generate

## Outcome

Produce a traceable 3D asset that satisfies a concrete in-engine budget and visual target.

## Required inputs

- text brief or rights-cleared reference views
- target engine and renderer
- scale, topology, material, LOD, collision, and performance budgets

Ask for missing information only when it changes the route materially. Otherwise
state conservative assumptions and proceed with read-only analysis.

## Workflow

1. Verify reference rights, identity consent when relevant, and output-license compatibility.
2. Choose a hardware-compatible generation path and document the model, weights, settings, and seed when available.
3. Generate into a new working directory and preserve raw outputs.
4. Repair orientation, units, transforms, topology, normals, UVs, materials, LODs, and collision through an approved DCC route.
5. Render multi-view turntables and test import, scale, shading, collision, and runtime budget in the target engine.

## Expected artifacts

- asset specification
- raw and processed models
- turntable and wireframe views
- engine import proof
- provenance record

## Workflow-specific gates

- Reject non-manifold geometry, inverted normals, broken UVs, missing textures, unsupported shaders, or unbounded polygon counts.
- Characters must be routed through rig and animation validation before production use.
- Do not treat a visually plausible single render as evidence of a usable 3D asset.

## Production completion gate

Before recommending production use, complete and report all seven gates:

1. Rights, consent, code/model/dataset/output license, and generation-provenance checks.
2. Technical format, naming, scale, color, metadata, and target-import validation.
3. Visual and temporal consistency review across representative views and states.
4. Runtime memory, frame-time, draw-call, streaming, and asset-budget checks.
5. Playability and interaction smoke tests in the target runtime.
6. Screenshot, capture, diff, or artifact-regression evidence with reproducible settings.
7. Human approval before replacing source assets or promoting generated output.

Unknown rights, missing consent, unsupported hardware, conflicting host adapters,
or failed quality gates block production promotion. Preserve originals and make
fallbacks explicit.
