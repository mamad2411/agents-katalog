---
name: git-check
description: "Run a read-only git preflight using the dev++ workflow. Use when the user invokes /git-check or asks to inspect branch, worktree, remotes, staged files, commits, push targets, or git risk before state-changing git actions."
---

# git-check

Run a read-only git preflight for the target or scope supplied after the slash command.

Rules:
- Inspect current branch, worktree status, remotes, upstream, recent commits, and relevant diff scope.
- Identify unrelated dirty files, detached HEAD, protected branches, unexpected remotes, and risky commit ranges.
- Do not stage, commit, switch branches, merge, rebase, tag, push, reset, clean, or delete anything.
- Report the exact current state, risks, and the approval needed for any state-changing git action.
