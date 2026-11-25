---
name: sprite-generate
description: "Plan, generate, normalize, and validate consistent 2D sprites, tiles, portraits, and animation sheets with preserved sources."
---

# Sprite Generate

## Outcome

Create engine-ready 2D art that remains visually consistent across poses, directions, and frames.

## Required inputs

- art bible or reference images with rights
- sprite purpose and camera
- dimensions, palette, directions, frame count, and engine format

Ask for missing information only when it changes the route materially. Otherwise
state conservative assumptions and proceed with read-only analysis.

## Workflow

1. Lock silhouette, palette, line weight, lighting direction, baseline, pivot, and scale in a sprite specification.
2. Generate a single approved key pose before requesting a full sheet.
3. Generate variants with fixed identity anchors and deterministic settings when supported.
4. Normalize canvas, alpha, baseline, pivots, padding, palette, and filenames without overwriting sources.
5. Preview every animation loop and import a copy into the target engine for a smoke test.

## Expected artifacts

- sprite specification
- source generations
- normalized sprites or atlas
- loop previews
- engine import evidence
- provenance record

## Workflow-specific gates

- Check transparent edges, accidental matte colors, cropped silhouettes, duplicate frames, baseline drift, timing, and loop continuity.
- For tiles, verify edge matching, terrain transitions, grid size, and representative map assembly.
- Require human approval of the key pose and final before replacing any project asset.

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
