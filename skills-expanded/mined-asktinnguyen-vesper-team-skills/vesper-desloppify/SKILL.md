---
name: vesper-desloppify
description: Use Desloppify inside Vesper to run a repeatable quality-improvement loop with session tools (`quality_scan`, `quality_status`, `quality_next`) and the `/desloppify` slash command.
---

# Vesper Desloppify Workflow

Use this skill when users ask to improve code quality, reduce technical debt, or run a structured cleanup loop.

## Available Vesper Surfaces

- Slash command: `/desloppify`
- Session tools:
- `quality_scan`
- `quality_status`
- `quality_next`

## Default Loop

1. Run `quality_scan` at workspace root.
2. Run `quality_status` to capture current score/status.
3. Run `quality_next` with `count=5`.
4. Propose a fix plan before mutating code.
5. After each batch of fixes, repeat from step 1.

## Slash Command Usage

- `/desloppify` or `/desloppify help` to view workflow help.
- `/desloppify run` to queue the full scan/status/next workflow.
- `/desloppify scan` to queue scan only.
- `/desloppify status` to queue status only.
- `/desloppify next` to queue next findings only.

## Notes

- `quality_scan` writes Desloppify state in the target repo.
- `quality_status` and `quality_next` are read-only and safe for inspection.
- If `desloppify` is missing, tools return an install hint.
