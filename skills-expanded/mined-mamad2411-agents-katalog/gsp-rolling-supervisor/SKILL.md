---
name: gsp-rolling-supervisor
description: "Use when game work is too large for one session and needs a guarded external build/verify/repair loop."
---

# Game Rolling Supervisor

## Goal
Push a game project through repeated autonomous passes without letting one long context rot into uselessness.

## Outputs

Follow the `gsp-orchestrator` output strategy:
- **inline** (default): present rolling supervisor plan in conversation.
- **minimal** or **full**: write `docs/game-studio/rolling-supervisor.md` and `docs/game-studio/rolling/state.json`.

Use:
- `../../shared/templates/rolling-supervisor-plan.md`
- `../../shared/reference/rolling-supervisor-architecture.md`
- `../../schemas/rolling-state.schema.json`
- `../../schemas/session-result.schema.json`

## Rules
- use this only when the repo can tolerate repeated build/verify/repair cycles
- prefer **short-lived worker sessions** over one giant session
- every worker must emit a compact structured handoff
- verification gates decide whether to continue
- use worktree isolation for parallel branches when practical
- do not create infinite hook or stop loops
- if the project is live or risky, only enable with explicit authorization

## Worker graph
Typical graph:
1. concept/requirements brainstorm
2. scope profile
3. architecture/plan
4. build
5. verify
6. feedback design/polish
7. verify again
8. repair if needed

## Important
The supervisor belongs outside the plugin runtime.
The plugin defines the contracts; an external Python supervisor executes them.
