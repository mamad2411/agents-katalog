---
name: material-texture-generate
description: "Generate and validate tileable, color-managed PBR material sets for a specified engine shader and texel-density budget."
---

# Material Texture Generate

## Outcome

Create coherent material maps whose physical interpretation survives engine import.

## Required inputs

- surface brief and rights-cleared references
- target shader workflow
- resolution, texel density, tiling scale, and compression budget

Ask for missing information only when it changes the route materially. Otherwise
state conservative assumptions and proceed with read-only analysis.

## Workflow

1. Define material class, real-world scale, lighting assumptions, map channels, color spaces, and packing convention.
2. Choose a licensed generation route compatible with available hardware.
3. Generate source maps without replacing existing project textures.
4. Validate seamless tiling, albedo range, roughness response, normal orientation, height continuity, and channel packing.
5. Preview on representative geometry under neutral and production lighting, then test engine import and compression.

## Expected artifacts

- material specification
- source and packed maps
- sphere and plane previews
- engine material instance
- provenance record

## Workflow-specific gates

- Treat base color as color data and linear maps as non-color data.
- Never infer legal reuse from a reference image being publicly visible.
- Flag baked lighting, inconsistent scale, edge seams, clipping, and implausible metallic values.

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
