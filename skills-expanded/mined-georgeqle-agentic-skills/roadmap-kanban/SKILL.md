---
name: roadmap-kanban
description: PoketoWork kanban variant of roadmap — sync roadmap phases and current steps to cards
type: planning
version: v0.1
argument-hint: "[--existing] [path-to-spec]"
allowed-tools: Bash(poketo *)
---

# Roadmap Kanban

Invoke as `$roadmap-kanban`.

Use this skill only in projects that have opted into a PoketoWork kanban pack.

## Process

1. Follow the base `$roadmap` workflow exactly, passing through `$ARGUMENTS`.
2. Resolve and validate the project board using `tasks/.kanban-board`, `poketo kanban boards`, and the standard lists: Backlog, Todo, In Progress, Done, Punt.
3. Fetch the board and show a brief overview before roadmap work.
4. After the base roadmap writes or updates `tasks/roadmap.md` and `tasks/todo.md`, sync cards:
   - For each unchecked current step in `tasks/todo.md`, search for a matching card. Move it from Backlog to Todo, leave it alone if already Todo or later, or create it in Todo with phase context.
   - For each future roadmap phase, search for a matching phase card. Create a Backlog summary card when missing.
   - Do not create ordinary Todo cards from `tasks/record-todo.md` or `tasks/recurring-todo.md`. Report advisory counts separately unless an item has been promoted into `tasks/todo.md`.
5. Report cards created, moved, skipped, and any failures.

Only move cards from Backlog to Todo. Never move cards backward. If kanban fails, warn and keep the roadmap output.

## Next-Step Routing

In the final response, include either `Recommended next skill: <command>` or the two-line pair `**Next work:** <specific task or "none">` and `**Recommended next command:** <one command or route>`. Route to the matching kanban workflow when board state can advance; otherwise route to the documented non-kanban fallback or say `No follow-up skill recommended` with the reason.

## Alignment Page

Follow the shared Alignment Page convention in CLAUDE.md. Output: `alignment/roadmap-kanban-{topic}.html`.

