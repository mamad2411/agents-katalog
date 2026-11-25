---
name: daily-task-manager
description: GBrain-inspired task lifecycle management for Codex. Use when the user wants to add, complete, defer, remove, or review tasks in a durable tracker.
---

# Daily Task Manager

Use this skill when the user wants a durable task list rather than a one-off reminder.

This port is adapted from `garrytan/gbrain` at commit `b7e3005b5b3f1b54082f9c5990482ebf81a4a807`.

## Important Adaptation

Upstream GBrain stores tasks as brain pages. In Codex, prefer:

- an existing repo task file if one exists
- otherwise a simple Markdown tracker such as `docs/daily-tasks.md`

## Workflow

1. Find the existing task tracker or create the smallest durable one.
2. Support the requested action:
   - add
   - complete
   - defer
   - remove
   - review
3. Keep priority levels explicit, for example `P0` to `P3`.
4. Preserve completion or deferment history when it matters.
5. Keep the file easy to scan and update.

## Guardrails

- Prefer updating one durable tracker over scattering tasks across multiple files.
- Do not silently delete tasks when complete or defer is the better action.
- Keep the task store simple unless the user explicitly wants a richer system.
