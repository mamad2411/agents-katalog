---
name: gsp-mechanics-systems-design
description: "Use when translating a locked concept into concrete game systems, progression, state, and encounter rules."
---

# Game Mechanics Systems Design

## Goal
Turn the concept into a concrete systems design that game developers can reason about and extend.

## Outputs

Follow the `gsp-orchestrator` output strategy:
- **inline** (default): present systems design in conversation.
- **minimal** or **full**: write `docs/game-studio/system-design.md`.

Use:
- `../../shared/templates/system-design.md`
- `../../shared/reference/game-dev-abstractions.md`

## Spec-driven compatibility
When `gsp-spec-driven-planning` is active:
- persist the systems design into `changes/<change-id>/design.md`
- consolidate UX, feedback, and systems decisions into the same design file instead of scattering them across unrelated docs

## Cover
- primary and secondary verbs
- core loop and loop exits
- state model
- encounter / obstacle / challenge model
- progression or meta progression
- save / persistence boundaries
- sound ownership and feedback ownership

## Important
Prefer game-native concepts such as `GameManager`, `StateMachine`, `EncounterDirector`, `HUDFlow`, and `SoundLayer`.
Do not let runtime-specific jargon replace actual game design clarity.
