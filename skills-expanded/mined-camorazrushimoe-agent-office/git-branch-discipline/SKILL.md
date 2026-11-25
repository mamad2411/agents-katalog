---
name: git-branch-discipline
description: Feature-branch workflow. Use when working with git — creating a branch for a task, committing, or opening a PR. Never commit directly to main/master.
---

# Git Branch Discipline

The Dev Crew works on feature branches. **Never commit or push directly to `main`/`master`.**

## Branch naming

`feature/<ticket>-<slug>`, e.g. `feature/BON-15-login`. Lowercase slug, hyphen-separated, derived from the ticket title.

## Rules

1. Check out a new branch from `main` for every task: `git checkout -b feature/<ticket>-<slug>`.
2. Commit small, logical changes with clear messages in English.
3. Push the branch and open a pull request — do not merge directly.
4. Request review (the qa agent, or self-review via the `code-review` skill) before merging.
5. Delete the branch after merge.

## Blocked (destructive) commands

Never run: `git push` to `main`/`master`, `git reset --hard`, `git clean -fd`, `git branch -D` on an in-flight feature branch, `git checkout .` / `git restore .`.
