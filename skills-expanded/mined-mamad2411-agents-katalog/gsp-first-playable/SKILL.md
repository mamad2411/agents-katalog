---
name: gsp-first-playable
description: "Use when the chosen quality target is intentionally first-playable or spike-quality."
---

# Game First Playable

You are the workflow for turning a prompt into a **real first playable**.
This is a specialized mode, not the universal target for all game work.

## Primary goal
Convert the user's idea into:
1. a concrete first-playable spec,
2. a narrow scope,
3. a backend recommendation or comparison,
4. a working vertical slice,
5. a verification report.

## Outputs

Follow the `gsp-orchestrator` output strategy:
- **inline** (default): present findings in conversation.
- **minimal** or **full**: write to `docs/game-studio/spec.md`, `docs/game-studio/backend-decision.md`, `docs/game-studio/ux-flow.md`, `docs/game-studio/architecture.md`, `docs/game-studio/plan.md`, `docs/game-studio/quality-report.md`.

Use the shared template at `../../shared/templates/first-playable-spec.md`.

## Workflow
1. Compile the prompt into a minimal spec.
2. Scope aggressively using `gsp-scope-guard`.
3. Choose the backend profile with `gsp-backend-selector`.
4. Design the first 30 seconds with `gsp-ux-flow-designer`.
5. Bootstrap the loop with `gsp-loop-bootstrap`.
6. Implement the thinnest vertical slice that proves the main fantasy.
7. Verify with `gsp-playability-verifier`.
8. Repair readability and feedback gaps with `gsp-screenshot-critic` and `gsp-hud-feedback-polish`.

## Important
Use this only when a minimal first-playable is truly the right target.
If the user wants a stronger prototype or a production-grade feature, route elsewhere.
