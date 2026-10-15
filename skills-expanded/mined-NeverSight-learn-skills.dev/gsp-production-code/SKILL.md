---
name: gsp-production-code
description: "Use when game implementation quality must be maintainable, understandable, and safe to extend."
---

# Game Production Code

## Goal
Raise the code-quality floor.
Unless the user explicitly asks for a throwaway spike, code should be written as though the project may continue and ship.

## Reference
Use:
- `../../shared/checklists/production-code-checklist.md`
- `../../shared/reference/game-dev-abstractions.md`

## Apply these rules
- Prefer explicit ownership of state and side effects.
- Use game-native boundaries: `GameManager`, controllers, state machines, systems, UI flow owners, sound layers.
- Avoid fake implementations in the main path.
- Avoid copy-paste architecture in critical systems.
- Keep the code readable for the next developer or next session.
- If refactoring, document compatibility and rollback concerns.

## Outputs

Follow the `gsp-orchestrator` output strategy:
- **inline** (default): present production code expectations in conversation.
- **minimal** or **full**: update `docs/game-studio/architecture.md` and `docs/game-studio/quality-target.md`.
