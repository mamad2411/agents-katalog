---
name: rig-animation
description: "Rig, retarget, generate, and quality-gate character animation with explicit skeleton, root-motion, deformation, and loop requirements."
---

# Rig Animation

## Outcome

Deliver animation that deforms cleanly and behaves predictably in the target engine.

## Required inputs

- rights-cleared character mesh
- target skeleton and engine
- clip list, frame rate, root-motion policy, and gameplay constraints

Ask for missing information only when it changes the route materially. Otherwise
state conservative assumptions and proceed with read-only analysis.

## Workflow

1. Inspect topology, pose, scale, symmetry, and deformation readiness before rigging.
2. Define skeleton naming, hierarchy, twist bones, facial scope, root, and retarget profile.
3. Generate or author weights and clips into preserved working copies.
4. Review deformations at stress poses and animation from multiple views.
5. Validate root motion, contacts, foot sliding, loop continuity, additive assumptions, events, and engine import.

## Expected artifacts

- rig specification
- rigged source copy
- validated clips
- contact and loop report
- engine animation proof
- provenance record

## Workflow-specific gates

- Reject unexpected bone scale, unstable constraints, collapsing joints, penetrations, foot skating, and discontinuous loops.
- Retargeting must preserve the original source and record both source and destination skeletons.
- Identity-based motion or performance capture requires documented performer consent.

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
