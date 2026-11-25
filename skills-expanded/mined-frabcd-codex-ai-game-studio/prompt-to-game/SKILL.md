---
name: prompt-to-game
description: "Convert a game idea into a scoped playable prototype through explicit design, stack selection, implementation, and evidence gates."
---

# Prompt To Game

## Outcome

Produce the smallest playable proof of the requested experience, not an unbounded production game.

## Required inputs

- one-sentence game idea
- target platform
- time, team, engine, art, and licensing constraints

Ask for missing information only when it changes the route materially. Otherwise
state conservative assumptions and proceed with read-only analysis.

## Workflow

1. Clarify the player fantasy, core verb, fail and success conditions, session length, and non-goals.
2. Define a one-loop prototype acceptance test and asset budget.
3. Run toolchain diagnosis and recommend a compatible engine and generation route.
4. Create a reversible implementation plan; require approval before files or external tools change.
5. Implement in thin vertical slices with a playable build after every slice.
6. Capture controls, known limitations, screenshots, test evidence, and provenance.

## Expected artifacts

- prototype brief
- approved plan
- playable build
- controls sheet
- evidence and provenance bundle

## Workflow-specific gates

- Prefer placeholder assets until the core loop is demonstrably fun.
- Keep generated code and content reviewable in small, testable increments.
- Stop scope growth that does not improve the prototype acceptance test.

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
