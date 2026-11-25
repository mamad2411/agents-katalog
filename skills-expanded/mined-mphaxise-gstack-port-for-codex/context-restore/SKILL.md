---
name: context-restore
description: Restore saved working context and orient a new Codex session before continuing work.
---

# Context Restore

Use this skill when the user asks to resume, restore context, pick up where they left off, or figure out where the work stands.

## Workflow

1. Inspect current state:
   - current branch
   - `git status --short`
   - recent commits
   - any reports, checkpoints, or brain pages related to the task
2. Read the latest relevant saved context:
   - prefer explicit user-provided context
   - then the newest repo-local report or checkpoint for the current branch
   - if the current branch has none, fall back to the newest relevant
     cross-branch checkpoint for an intentional worktree handoff
   - then local brain search via `query` or `brain-ops`
3. Reconstruct:
   - what was done
   - what changed locally
   - what remains
   - what should not be touched
4. Continue only after the working boundary is clear.

## Guardrails

- Do not overwrite local changes while restoring context.
- Do not assume untracked files are disposable.
- Do not let a newer sibling-worktree checkpoint shadow a current-branch
  checkpoint. Keep cross-branch state as a fallback, not the first choice.
- If saved context conflicts with current files, trust the current files and call out the mismatch.
