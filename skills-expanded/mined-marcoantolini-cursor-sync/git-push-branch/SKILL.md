---
name: git-push-branch
description: Pushes existing commits on the current branch to its upstream. No stage, commit, or history rewrite.
disable-model-invocation: true
---

# Git push branch

Push **only** what is already committed on the current branch.

## Steps

1. Identify the branch: `git branch --show-current` and `git status -sb`.
2. Push:
   - Upstream set → `git push`
   - No upstream → `git push -u origin HEAD` (or the branch’s remote-tracking equivalent)
3. **Done when:** the remote reports a successful update for this branch, or you have explained a rejection and stopped for instructions.

## Guardrails

- Working tree and local commits stay untouched: no `add`, `commit`, amend, rebase, or reset.
- Non-fast-forward rejection → explain and ask how to proceed. Force-push only if the user explicitly requests it in this message.
