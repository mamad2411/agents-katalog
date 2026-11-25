---
name: pr-merge-cleanup
description: "Execute a PR workflow: commit changes, push to a branch, create a GitHub PR, wait for CI checks to pass (no bypassing), merge the PR, and clean up all git status, branches, and scratch files. Use when a user asks to commit, PR, and clean up."
---

# PR Merge & Cleanup Workflow

Strict Git/GitHub PR workflow. Changes are CI-tested before entering `main`, local environment left clean.

## Steps

Follow strictly in order:

### 1. Branch & Commit
- `git status` to identify uncommitted changes.
- Never commit directly to `main`.
  - `git checkout main && git pull`
  - `git checkout -b <type>/descriptive-branch-name` — where `<type>` matches the conventional commit (`fix`, `feat`, `chore`, `refactor`, etc.)
- Commit with a conventional commit message (e.g., `fix(module): ...`, `feat(component): ...`).
- `git push -u origin <branch-name>`

### 2. Create PR
- `gh pr create --title "..." --body "..."`
- Clear title, description explaining *why* and *how*.

### 3. CI Validation
- Wait for CI to pass:
  - `gh pr checks` or `gh run list --limit 3`
- **Never** use `--admin` bypass unless the user explicitly says to.
- If CI fails: investigate (`gh run view <run-id> --log`), fix, commit, push, wait again.
- If the repo has no CI pipelines, confirm with the user before proceeding to merge.

### 4. Rebase & Merge
- If `main` has moved ahead, rebase before merging:
  - `git fetch origin && git rebase origin/main`
  - Resolve any conflicts, then `git push --force-with-lease`
- Merge:
  - `gh pr merge <pr-number> --squash --delete-branch`
- Pull the squash commit:
  - `git checkout main && git pull`

### 5. Cleanup
- Delete local feature branch: `git branch -D <branch-name>`
- `git branch` — remove any stale testing or task branches.
- Remove temporary scratch files (`test.ts`, `dummy.patch`, `.orig`, etc.).
- `git status` — must show clean working tree, nothing to commit.
