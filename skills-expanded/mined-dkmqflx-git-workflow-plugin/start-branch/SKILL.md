---
name: start-branch
description: Create a new git branch with an appropriate name and switch to it — from the current position by default, or from a named base branch (e.g. dev, master, main, stage) when one is specified. Use when the user wants to start work on a fresh branch — phrases like "브랜치 만들어줘", "master에서 브랜치 만들어줘", "dev 기준으로 브랜치 파줘", "stage에서 새 브랜치", "start a new branch", "create a branch for this", "branch off master", "작업 브랜치 파줘", "/start-branch". Do NOT use when the user explicitly wants a worktree (separate directory).
license: MIT
metadata:
  author: dkmqflx
  version: "1.0.0"
---

# Start Branch

Generate an appropriate branch name for the task and switch to it — from the current position, or from a named base branch.

## When to apply

Starting work on a new feature, fix, or task directly in the current directory. **Do not apply** for worktree (separate checkout directory) — that is `/worktree`.

## Branch naming convention

Format: `<type>/<short-description>`

| Type | When to use |
|------|-------------|
| `feat/` | New feature or capability |
| `fix/` | Bug fix |
| `chore/` | Maintenance, config, dependency updates |
| `refactor/` | Restructuring without behavior change |
| `docs/` | Documentation only |
| `test/` | Test additions or changes |

Description rules: lowercase, hyphen-separated, 2–5 words, describes WHAT (not HOW).

**Examples:** `feat/user-authentication`, `fix/cart-total-calculation`, `chore/update-eslint-config`, `refactor/extract-payment-service`

## Steps

1. Determine the base:
   - If the user named a specific branch (e.g. `dev`, `master`, `main`, `stage`), that is the base branch.
   - Otherwise, the base is the current position — no checkout needed before branching.
2. Derive the branch name from the user's task description using the convention above.
   If no task description was given (bare `/start-branch`), ask one short question first.
3. If a base branch was named, switch to it and pull latest, then branch from it:
   ```bash
   git checkout <base branch> && git pull
   git checkout -b <branch-name>
   ```
   Otherwise, branch directly from the current position:
   ```bash
   git checkout -b <branch-name>
   ```
4. Confirm in one line: `Switched to new branch: <branch-name>` (append `(from <base branch>)` if a base was named)
5. Begin the user's task.
