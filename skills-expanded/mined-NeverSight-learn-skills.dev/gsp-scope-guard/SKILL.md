---
name: gsp-scope-guard
description: "Use when a game project is expanding too broadly and needs scope protection without losing the core goal."
---

# Game Scope Guard

## Goal
Keep scope under control while preserving the value of the request.

## Core rule
Do **not** equate “scope control” with “remove everything interesting.”

## By mode
- **yolo-super / guided-build**: protect the user’s core requested feature set. Cut edge cases, not the fantasy.
- **refactor-open**: protect the outcome, but allow larger architecture change when it prevents endless patching.
- **surgical-live**: minimize blast radius first; here scope control often means tighter change boundaries.

## Good cuts
- optional content multiplication
- edge-case polish outside the critical path
- tooling not needed for the current target
- deep progression systems when the target does not require them

## Bad cuts
- requested core mechanic
- requested style / feel / UX quality if that is central to the ask
- essential fail/retry and onboarding clarity
- architecture cleanup that is necessary to make the requested change stable

## Outputs

Follow the `gsp-orchestrator` output strategy:
- **inline** (default): state scope decisions and rationale in conversation.
- **minimal** or **full**: record the rationale in `docs/game-studio/plan.md` or `docs/game-studio/build-strategy.md`.


## Pair with
Use `gsp-scope-profile` early to define the intended scope. This skill protects it later.
