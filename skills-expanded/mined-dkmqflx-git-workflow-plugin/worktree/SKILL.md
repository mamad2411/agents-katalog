---
name: worktree
description: Create a new git worktree on a fresh branch and switch into it before starting work. Use when the user asks to start a task in a new worktree, work in isolation from the main checkout, or invokes "/worktree" — phrases like "워크트리 만들어줘", "새 브랜치 파서 작업해줘", "worktree에서 작업 시작". Do NOT use for removing or cleaning up an existing worktree.
---

# Worktree

Create a sibling worktree on a fresh branch, then continue the user's task inside it.

Heavy lifting → `scripts/create.sh` (handles uniqueness, error checks).

## When to apply

Start a task in an isolated worktree. **Do not apply** for removal — that is `/worktree-done`.

## Steps

1. Derive a kebab-case branch name (≤ 4 words) from the user's task description.
   If no description was given (bare `/worktree`), ask one short question first.
2. Run from the repo root:
   ```bash
   bash <skill-dir>/scripts/create.sh <branch-name>
   ```
   The script's **stdout is the new worktree path** (stderr is progress).
   If it exits non-zero, stop and surface the error.
3. `cd` into that path (separate Bash call — child shells can't change parent cwd).
4. Confirm in one line: `Worktree ready: <path> (branch: <branch>)`
5. Begin the user's task.
