---
name: checkpoint
description: Save-and-resume workflow for Codex. Use when work context should be captured so the same repo or thread can be resumed cleanly later.
---

# Checkpoint

Use this skill when the user is about to switch context, stop for the day, or wants a reliable resume point.

This port is adapted from `garrytan/gstack` at commit `4d2c8d94d00cc4f4f3d4c26316a4f939ceedc045`.

## Workflow

1. Capture the current working state:
   - branch
   - goal
   - what changed
   - open questions
   - next actions
2. Save the checkpoint in a durable form, preferably using the `reports` pattern.
3. When resuming, load the latest relevant checkpoint and continue from that state instead of reconstructing it from memory.
   - prefer the newest checkpoint for the current branch
   - use `context-restore` for cross-branch fallback and worktree handoff

## Guardrails

- Keep checkpoints concise and action-oriented.
- Prefer one durable checkpoint over scattered status notes.
- Do not overwrite older checkpoints when a timestamped history is safer.
- Do not let a newer sibling-worktree checkpoint shadow a current-branch save.
