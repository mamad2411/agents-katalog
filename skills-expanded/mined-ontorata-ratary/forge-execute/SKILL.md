---
name: forge-execute
description: >-
  Execute blueprint tasks with checkpoints or fresh subagent per task. Use when
  a forge-blueprint plan is approved.
---
# Forge Execute

**Activates:** blueprint approved.

## Modes

### A — Sequential checkpoints (default)

1. Take next unchecked task from `{slug}-plan.md`
2. Run `forge-prove` for that task (tests first when behavior changes)
3. Run `forge-inspect` before marking task done
4. Commit with single-intent message; update plan checkbox
5. Pause for owner on ambiguous scope creep

### B — Subagent per task

1. Dispatch one subagent with: task text, file paths, constitution link, verify command
2. Review output with **two passes**: (1) spec match to task, (2) code quality / layers
3. Parent agent integrates; never merge unreviewed subagent diffs blindly

## Rules

- One concern per commit
- No drive-by refactors
- Stop on red tests — invoke `forge-diagnose`
- Update phase docs only when task explicitly requires it

## Progress

Report after each task: files touched, tests run, commit hash.
