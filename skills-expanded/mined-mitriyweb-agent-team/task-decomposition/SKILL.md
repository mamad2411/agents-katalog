---
name: task-decomposition
description: Decompose a high-priority task from ROADMAP.md into actionable sub-tasks.
compatibility: Requires bash, Claude Code
metadata:
  team: software-development
  role: team-lead
  version: "1.0"
---

## Procedure

1. Read `ROADMAP.md` to identify the highest priority task.
2. Verify that `ROADMAP.md` passes pre-flight validation.
3. Pick the highest priority task and decompose it into granular sub-tasks.
4. Assign the decomposed tasks to the architect with a written brief.

## Gotchas

- `ROADMAP.md` must pass pre-flight validation before execution.

- The `--team` flag controls which `agents/` directory is used; default is "software development" (always quote the path as it contains a space).

## Validation loop

The team-lead verifies that the brief is clear and covers all requirements of the original task before passing it to the architect.
