---
allowed-tools: Bash(git branch:*), Bash(git status:*), Bash(git commit:*)
description: Remove a feature branch after it has been merged into the main branch.
---

## Context

We have a PR that has been merged into the main branch. And the current feature branch is now ready to be deleted.

## Your task

You are to delete the feature branch.

Run (only after you've moved back to the main branch, and pulled the latest changes from remote main branch):
    git branch -d $ARGUMENTS