---
name: gsp-scope-profile
description: "Use when setting scope tier, completeness bar, and allowed refactor range for a game build."
---

# Game Scope Profile

## Goal
Translate project state and quality target into a concrete scope tier.

## Outputs

Follow the `gsp-orchestrator` output strategy:
- **inline** (default): present scope profile in conversation.
- **minimal** or **full**: write `docs/game-studio/scope-profile.md`.

Use:
- `../../shared/templates/scope-profile.md`
- `../../shared/reference/scope-tiers.md`

## Workflow
1. Read `project-state.md`, `requirements.md`, and `quality-target.md`.
2. Classify scope as `micro`, `small`, `medium`, or `ambitious`.
3. State what is non-negotiable for this tier.
4. Explicitly list what may be deferred.
5. Decide whether the build should use:
   - small surgical tasks
   - medium coherent chunks
   - large AI-native coherent chunks
6. Decide whether a rolling supervisor is recommended.

## Relationship to scope guard
- `gsp-scope-profile` defines the intended scope.
- `gsp-scope-guard` protects that scope during execution.
