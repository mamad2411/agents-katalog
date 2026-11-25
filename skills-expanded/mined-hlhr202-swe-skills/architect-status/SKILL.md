---
name: architect-status
description: Report read-only Architect project status from core context and, when available, the tracks registry and plans. Use when the user asks for setup status, progress, current task, next action, blockers, completion percentage, or pending work.
---

# Architect Status

Report best-effort Architect state without changing it. Follow `references/status-protocol.md` as the source of truth.

## Hard Boundaries

- This skill is strictly read-only: never create, edit, move, delete, archive, or commit.
- Keep reads under safe `architect/` paths and never resolve malformed track links.
- Report integrity issues; do not repair them.

## Run

1. Read `references/status-protocol.md` and verify core context.
2. Classify missing, partial, or complete track-management state.
3. Parse safe registry entries, plan task-status granularity, and metadata best-effort.
4. Compute progress, current work, next action, blockers, and precedence-based project status.
5. Return the concise report and stop without mutations or interactive cleanup prompts.
