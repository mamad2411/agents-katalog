---
name: commit
description: Stage and commit the current changes with a clear message.
disable-model-invocation: true
allowed-tools: Bash(git status *) Bash(git diff *) Bash(git add *) Bash(git commit *)
---

1. Run git status and git diff to see what changed.
2. If you see secret keys, .env files or large build folders, stop and tell me. Don't commit them.
3. Write a one-line commit message in plain English that says what changed and why.
4. Stage the files and commit. Don't push.
