---
name: project-memory
description: Use to create and maintain durable cross-session project memory and the progress ledger, so long autonomous builds resume cleanly after compaction, restarts, or new sessions. Read it when starting work and update it as decisions and tasks land.
---

# Project Memory

**Announce at start:** "I'm using claude-engineer:project-memory to keep durable project state."

Long autonomous builds outlive a single context window. Memory lives in **files**, not your head.
The claude-engineer SessionStart hook auto-loads these at the start of every session.

## The state files (in `.claude-engineer/`)
- **`memory.md`** - durable project memory: key decisions (+ why), established conventions, the data model, open threads/risks, and "next action". The single source of truth for *why things are the way they are*.
- **`progress.md`** - the task ledger: each task with status (todo / doing / done), the commit/branch, and a one-line result. Append-only-ish; never delete history.
- **`current-phase.txt`** - one line naming the active phase (e.g. `Phase 2 - Frontend`).
- **`quality-gate-status.json`** - written by the project quality-gate runner; read by the commit gate. Do not hand-edit.

## Iron Law
**Trust the ledger and `git log` over your own recollection.** After compaction, re-read these files before acting. Never re-run a task `progress.md` marks done.

## When to update
- **After every task:** append a line to `progress.md`.
- **On every non-obvious decision:** add it to `memory.md` (mirror big ones into `docs/plan/decisions.md`).
- **On phase change:** update `current-phase.txt`.

## Initialize (Phase 0 / planning)
Create `.claude-engineer/` with seed `memory.md` (problem, stack, data model, decisions-so-far, next action), an empty `progress.md` ledger, and `current-phase.txt`. Add `.claude-engineer/quality-gate-status.json` to `.gitignore` (machine-generated); commit `memory.md`/`progress.md` so teammates and future sessions share them.

## Red flags - STOP
- Starting work without reading `memory.md` + `progress.md` first.
- A decision made in chat but never written down → write it now; chat is not durable.
- Re-deriving something already settled in `memory.md`.
