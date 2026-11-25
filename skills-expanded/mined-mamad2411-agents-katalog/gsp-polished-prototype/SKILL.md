---
name: gsp-polished-prototype
description: "Use when the target is a coherent, demo-ready prototype rather than a minimal first playable."
---

# Game Polished Prototype

## Goal
Produce a **polished prototype**, not just a barely playable vertical slice.

## Required quality bar
A valid polished prototype should usually include:
- the requested core loop,
- core requested features in scope,
- a coherent menu / start / retry / pause flow when relevant,
- readable HUD and affordances,
- meaningful feedback and feel,
- clear visual direction,
- production-grade code structure for the critical path.

Use:
- `../../shared/checklists/polished-prototype-rubric.md`
- `../../shared/checklists/production-code-checklist.md`
- `../../shared/checklists/game-feel-pillars.md`

## Workflow
1. Protect the user’s real ask. Do not cut away defining features merely to move faster.
2. Build a strong first minutes experience.
3. Implement the requested feature set for this pass, not just one isolated mechanic.
4. Make the build feel deliberate: feedback, transitions, fail/retry, readability.
5. Keep architecture clean enough to continue development.
6. Verify and repair before calling it done.

## Important
If the user asked for a strong prototype, `first-playable` is not enough.
This skill exists to resist that accidental down-scoping.
