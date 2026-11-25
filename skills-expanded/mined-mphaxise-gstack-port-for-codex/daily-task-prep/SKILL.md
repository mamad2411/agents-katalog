---
name: daily-task-prep
description: GBrain-inspired morning prep for Codex. Use when the user wants a working view of today's meetings, open threads, and top tasks.
---

# Daily Task Prep

Use this skill when the user wants an actionable morning prep view, not just an informational briefing.

This port is adapted from `garrytan/gbrain` at commit `b7e3005b5b3f1b54082f9c5990482ebf81a4a807`.

## Workflow

1. Load today's meetings if calendar context is available.
2. Load the active task tracker.
3. Surface:
   - today's meetings with relevant prep context
   - unresolved threads from yesterday or the current week
   - `P0` and `P1` tasks first
4. End with a short recommendation for what to tackle first.

## Guardrails

- Do not list meetings without context if context can be loaded.
- Make uncertainty visible when calendar or task data is incomplete.
- Keep the output oriented around action, not just information.
