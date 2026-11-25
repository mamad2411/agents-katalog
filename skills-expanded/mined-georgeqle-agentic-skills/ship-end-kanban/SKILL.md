---
name: ship-end-kanban
description: PoketoWork kanban variant of ship-end — close the active session card after wrapping up
type: shipping
version: v0.0
argument-hint: "[--no-deploy]"
allowed-tools: Bash(poketo *)
---

# Ship End Kanban

Invoke as `$ship-end-kanban`.

Use this skill only in projects that have opted into a PoketoWork kanban pack.

## Process

1. Follow the base `$ship-end` workflow exactly, passing through `$ARGUMENTS`.
2. Resolve and validate the project board using `tasks/.kanban-board`, `poketo kanban boards`, and the standard lists: Backlog, Todo, In Progress, Done, Punt.
3. Fetch the board state and find the In Progress session card matching this host or the current step.
4. If found, move it to Done, mark it done, and update the description with commit SHAs and session wrap-up notes.
5. If no matching session card is found, skip card movement and report that no active card was found.
6. Suggest the top Todo card by priority: overdue, starred, then list order. If no Todo cards exist, check Backlog.

Kanban failures are advisory and must not block the base ship-end workflow.

## Default Shipping Contract

Follow the shared shipping contract convention in CLAUDE.md.

