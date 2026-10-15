---
name: gsp-build-strategy
description: "Use when deciding development mode, quality target, task granularity, or refactor policy for game work."
---

# Game Build Strategy

## Goal
Choose the right build strategy for the project.

## Outputs

Follow the `gsp-orchestrator` output strategy:
- **inline** (default): present build strategy and quality target in conversation.
- **minimal** or **full**: write `docs/game-studio/build-strategy.md` and `docs/game-studio/quality-target.md`.

Use:
- `../../shared/reference/development-modes.md`
- `../../shared/reference/quality-targets.md`
- `../../shared/templates/build-strategy.md`
- `../../shared/templates/quality-target.md`

## Development modes
- `yolo-super`
- `guided-build`
- `refactor-open`
- `surgical-live`

## Quality targets
- `first-playable`
- `polished-prototype`
- `production-feature`
- `live-patch`

## Selection rules
- **greenfield + narrow mechanic spike** -> `yolo-super` + `first-playable`
- **greenfield + serious showcase build** -> usually `yolo-super` or `guided-build` + `polished-prototype`
- **existing product-facing feature work** -> usually `guided-build` or `refactor-open` + `production-feature`
- **shipped or live-risky** -> `surgical-live` + `live-patch`

## Planning policy
Match task size to the mode:
- aggressive modes can use large coherent implementation chunks
- production-feature work can use medium coherent chunks
- live work should use smaller changes with tighter verification

Choose the exploration budget explicitly:
- `minimal` when the task is narrow and already shape-locked
- `standard` for normal product work
- `high` for single-prompt showcase generation, benchmark runs, or any task where first-result quality matters more than token thrift

For `high` exploration budget work:
- spend more tokens up front on concept lock, UX shape, and visual anchor decisions
- prefer `polished-prototype` over `first-playable` unless the user explicitly wants only a spike
- add runtime verification and screenshot critique before claiming completion
- if the host supports subagents, default to builder + reviewer + verifier instead of a single uninterrupted build pass
- if the task splits cleanly, allow multiple builders in parallel with a shared reviewer / verifier gate

## Guardrail
Do not let “safe” planning ruin the result on low-risk greenfield work.
Do not let “fast” planning justify broad rewrites on live products.
For benchmark or showcase builds, do not optimize for token thrift if that weakens the result.
