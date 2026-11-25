---
name: opencode-git-workflow
description: Branch, worktree, commit, merge, and PR protocol for OpenCode worker tasks with conflict and authorization rules.
---

# OpenCode Git Workflow

Opinionated protocol for worker code changes. Coordinator owns integration.

## Setup

- `git fetch` first so branches start from current upstream.
- Never let concurrent writers share a checkout. One branch and one worktree per worker.
- Name branches `<type>/<short-topic>` (conventional prefix: `feat/`, `fix/`, `chore/`).

## Commits

- Small conventional commits (`feat:`, `fix:`, `chore:`, ...). One logical change per commit.
- Never commit secrets (`.env`, tokens, passwords). Never commit unrelated files.

## Integrate sequentially

- Integrate workers one at a time, never in parallel into the same branch.
- Rebase the worker branch before merge so history stays linear.
- The coordinator resolves conflicts and reruns the full checks after each resolution.
- Remove worktrees after merge (`git worktree remove`).

## Hard rules

- Never force-push a shared branch.
- Never push and never open a PR without explicit authorization from the boss.
