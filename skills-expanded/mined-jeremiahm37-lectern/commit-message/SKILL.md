---
name: commit-message
description: Write a conventional commit message for the staged change. Use when asked to commit or to describe a change.
---

# Commit message

1. Read the staged diff with `git diff --cached`.
2. Write a subject line in the imperative, at most 72 characters, that says
   what the change does for a reader of the log.
3. Add a body only when the reason for the change is not obvious from the
   diff: why, not what.
