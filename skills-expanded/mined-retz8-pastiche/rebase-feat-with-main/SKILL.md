---
name: rebase-feat-with-main
description: Rebase the current pastiche feature branch onto main to absorb hotfixes. Use when the user invokes `/rebase-feat-with-main`, when resuming a task, or after a hotfix lands on main while a feature branch is in flight.
---

# rebase-feat-with-main

## Workflow

1. **Guard.** Current branch must be a feature branch (`<version>/<task-name>`) or sub-task branch — never main. Working tree must be clean; if not, stop and ask.
2. `git fetch origin main`
3. `git rebase origin/main`
4. **On conflict:** stop immediately, show the conflicting files, and let the user decide — never auto-resolve, never `--abort` without asking.
5. **If the branch is already pushed:** `git push --force-with-lease`. Never force-push main.
6. Report: how many commits were replayed and whether main had moved at all (no-op is a valid outcome).
