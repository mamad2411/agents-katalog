---
description: Read AGENTS.MD and CLAUDE.MD before working in a folder
alwaysApply: true
---

# Check agent instruction files first

At the start of every prompt — before reading, editing, or creating files — look for agent instruction files in the workspace and in any folder you plan to touch.

## Files to check

Search for these names (case may vary):

- `AGENTS.MD` / `AGENTS.md`
- `CLAUDE.MD` / `CLAUDE.md`

## Where to look

1. **Workspace root** — e.g. `/AGENTS.MD`, `/CLAUDE.MD`
2. **Each subproject or folder you will work in** — e.g. `testapp/`, `geo-analyzer/`, or any directory whose files you read or modify

Walk up from the target file path if needed (e.g. `src/components/` → check `src/`, then project root).

## What to do when found

- **Read the file(s) immediately** and treat their contents as binding instructions for that scope.
- If `CLAUDE.md` references another file (e.g. `@AGENTS.md`), read that file too.
- Prefer folder-local instructions over generic assumptions when they conflict.

## When none exist

Proceed normally; do not create placeholder instruction files unless the user asks.
