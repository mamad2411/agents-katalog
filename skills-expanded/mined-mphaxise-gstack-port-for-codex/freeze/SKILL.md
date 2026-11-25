---
name: freeze
description: Edit-scope boundary for Codex. Use when changes should be restricted to one directory or subsystem during a task.
---

# Freeze

Use this skill when the user wants edits locked to a specific path or subsystem while debugging or making a focused change.

This port is adapted from `garrytan/gstack` at commit `4d2c8d94d00cc4f4f3d4c26316a4f939ceedc045`.

## Workflow

1. Define the allowed edit scope explicitly.
2. Keep all writes inside that boundary until the user widens it or invokes `unfreeze`.
3. If the best fix crosses the boundary, stop and ask before editing outside it.

## Guardrails

- Treat the boundary as a hard rule, not a suggestion.
- Do not expand scope silently.
- Preserve clarity about what is in scope and what is not.
