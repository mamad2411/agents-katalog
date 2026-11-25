---
name: claude-relais
description: Router-first Claude orchestration skill: fresh repos trigger guided setup, existing repos get next-step options, and BUILD is always dispatched to Cursor headless agent.
---

# claude-relais

Use this skill for deterministic orchestration with a strict split:
- Claude orchestrates/plans/verifies
- Cursor builds code

## Entry Router (first action every session)

1. If user input looks like a direct CLI command (`envoi ...`), execute it via shell instead of treating it as planning text.
2. Else inspect orchestration state under `relais/`.
3. Route:
- Fresh repo or missing `relais/ROADMAP.json` -> guided setup/onboarding
- Existing state -> show next-step options and continue loop

## Loop Contract

1. Router/Setup
2. PLAN
3. DISPATCH
4. BUILD (Cursor only)
5. VERIFY
6. UPDATE roadmap/state
7. Continue or stop based on mode

## Mode Semantics

- `task`: stop after one successful task
- `milestone`: continue until active milestone is done, then stop
- `autonomous`: continue until blocked/limits/signal

## Non-negotiable Guardrails

- BUILD must be handled by Cursor headless agent.
- Do not use Claude Task/sub-agent as BUILD worker.
- Never mark roadmap complete while pending milestones remain.
- Verify from git truth, not builder claims.

## Files this skill uses

- `BOOT.txt`
- `ORCHESTRATOR.md`
- `claude.md`
- `relais/STATE.json`
- `relais/TASK.json`
- `relais/REPORT.json`
- `relais/ROADMAP.json`

## References

- `references/how-it-works.md`
- `references/configuration.md`
- `references/troubleshooting.md`
