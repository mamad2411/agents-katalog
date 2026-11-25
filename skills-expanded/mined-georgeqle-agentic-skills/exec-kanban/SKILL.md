---
name: exec-kanban
description: PoketoWork kanban variant of exec — move the active step through In Progress and Done
type: execution
version: v0.1
argument-hint: "[--phase]"
allowed-tools: Bash(poketo *)
invocation: orchestrator
---

# Exec Kanban

Invoke as `$exec-kanban`.

Use this skill only in projects that have opted into a PoketoWork kanban pack.

## Process

1. Resolve and validate the project board using `tasks/.kanban-board`, `poketo kanban boards`, and the standard lists: Backlog, Todo, In Progress, Done, Punt.
2. Fetch the board and show a brief overview.
3. Before running the base workflow:
   - Get `hostname -s` and `git branch --show-current`.
   - Read `tasks/todo.md` for the current step.
   - Search for the matching card. Move it from Todo to In Progress, leave it alone if already In Progress, or create it in In Progress.
   - Update its description with hostname, branch, and start timestamp.
4. Check In Progress cards for advisory conflicts: same branch on another host, stale cards from this host, and untracked cards without host metadata.
5. Follow the base `$exec` workflow exactly, passing through `$ARGUMENTS`.
6. After execution and shipping:
   - Move the completed step card to Done and mark it done.
   - Update the description with commit SHAs, progress, and completed timestamp.
7. After planning the next step, ensure its card exists in Todo: move from Backlog, create if missing, or skip if already Todo or later.
8. Suggest the top Todo card by priority: overdue, starred, then list order. If no Todo cards exist, check Backlog.

Kanban failures are advisory and must not block the base run workflow.

## Default Shipping Contract

Follow the shared shipping contract convention in CLAUDE.md.

