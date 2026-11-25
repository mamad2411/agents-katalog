---
name: gsp-loop-bootstrap
description: "Use when establishing core game runtime structure such as state flow, control, camera, and UI ownership."
---

# Game Loop Bootstrap

## Goal
Create a maintainable gameplay architecture that matches the chosen target quality.

## Outputs

Follow the `gsp-orchestrator` output strategy:
- **inline** (default): present architecture decisions in conversation.
- **minimal** or **full**: write or update `docs/game-studio/architecture.md`.

## Prefer abstractions like
- `GameManager`
- `InputProfile`
- `StateMachine`
- `PlayerController`
- `CameraRig`
- `HUDFlow`
- `SoundLayer`
- `EncounterDirector`

## Rules
- Separate simulation state and UI state clearly enough to reason about them.
- Avoid hiding critical gameplay state inside presentation objects.
- Choose the simplest architecture that still supports the requested result.
- In aggressive greenfield modes, do not fear building a complete coherent shell if it prevents later churn.
- In live modes, preserve compatibility unless a deliberate migration plan exists.
