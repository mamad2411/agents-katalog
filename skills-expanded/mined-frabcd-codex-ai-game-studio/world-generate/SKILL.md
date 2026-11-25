---
name: world-generate
description: "Generate reversible terrain, environments, procedural levels, lighting, navigation, and spawn layouts from validated design constraints."
---

# World Generate

## Outcome

Create navigable, performant environments that serve the intended player flow.

## Required inputs

- level intent and player metrics
- engine, platform, and art direction
- terrain, biome, traversal, encounter, lighting, and streaming budgets

Ask for missing information only when it changes the route materially. Otherwise
state conservative assumptions and proceed with read-only analysis.

## Workflow

1. Map critical path, optional paths, landmarks, gates, encounter beats, spawn rules, and accessibility constraints.
2. Choose deterministic procedural or generative stages with saved seeds and parameters.
3. Generate into a new scene or layer while preserving authored content.
4. Bake or update navigation, collision, lighting, occlusion, and streaming data only after plan approval.
5. Run reachability, spawn safety, sightline, readability, lighting, and performance checks in representative routes.

## Expected artifacts

- world specification
- seed and parameter manifest
- generated scene copy
- navigation and lighting evidence
- playthrough captures
- provenance record

## Workflow-specific gates

- Verify every required objective and exit is reachable from every valid spawn.
- Check geometry intersections, floating props, traversal metrics, dark dead ends, and repetition artifacts.
- Human review decides whether a generated world replaces or merges with authored work.

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
