---
name: gsp-subagent-build-loop
description: "Use when game implementation should default to a builder-reviewer-verifier loop instead of one monolithic pass."
---

# Game Subagent Build Loop

## Goal
Turn a game build into a default multi-agent workflow: builder, reviewer, verifier.
The goal is stronger and more stable output from one user prompt, not thrift.

## Outputs

Follow the `gsp-orchestrator` output strategy:
- **inline** (default): present subagent build loop plan in conversation.
- **minimal** or **full**: write `docs/game-studio/subagent-build-loop.md`.

## Default loop
For each meaningful build task or end-to-end slice:
1. Dispatch a **builder** subagent to implement the slice.
2. Dispatch a **reviewer** subagent using `gsp-build-review`.
3. Dispatch a **verifier** subagent using `gsp-playability-verifier`.
4. If review or verification fails, send the builder back with the concrete findings.
5. Repeat until the slice is acceptable or the blocker should be surfaced to the user.

## Parallel policy
Parallel builders are allowed only when ownership is disjoint.
Examples: core loop vs HUD, feedback vs content pass, gameplay slice vs menus.
Do not parallelize builders that fight over the same files or architectural choices.

## Quality policy
- benchmark and showcase builds should prefer this loop by default
- greenfield polished-prototype work should usually prefer this loop
- live-risky work may still use a tighter reviewer / verifier loop with smaller tasks

## Important
Do not claim completion after the builder finishes. Review and verification are expected to find problems.
