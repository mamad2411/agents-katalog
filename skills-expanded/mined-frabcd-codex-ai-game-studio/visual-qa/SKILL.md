---
name: visual-qa
description: "Run evidence-based multi-view visual, temporal, import, and runtime checks for generated game assets and scenes."
---

# Visual Qa

## Outcome

Find visible and technical failures that single-view or file-only validation misses.

## Required inputs

- asset, scene, or build under review
- reference target and acceptance criteria
- representative cameras, states, platforms, and budgets

Ask for missing information only when it changes the route materially. Otherwise
state conservative assumptions and proceed with read-only analysis.

## Workflow

1. Confirm the comparison baseline, capture settings, color pipeline, cameras, states, and tolerances.
2. Capture consistent front, side, rear, three-quarter, close-up, silhouette, wireframe, and motion views as applicable.
3. Compare against references and prior approved artifacts without hiding uncertainty behind a single similarity score.
4. Inspect temporal stability, animation contacts, particles, lighting, UI states, and transition frames.
5. Run engine import and representative runtime captures, then classify findings by severity and reproducibility.

## Expected artifacts

- capture manifest
- annotated contact sheet
- temporal review
- runtime metrics
- reproducible findings

## Workflow-specific gates

- Control resolution, camera, lighting, exposure, pose, animation time, and platform before comparing images.
- Review transparent assets over light, dark, and checkerboard backgrounds.
- A visual pass never overrides license, format, performance, playability, or human-approval gates.

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
