---
name: commit-message-helper
description: Suggest clear commit messages from the staged diff.
---

# Commit Message Helper

Reads the staged diff and suggests a short, conventional commit message.

## Steps

1. Read the staged diff (git diff --staged).
2. Suggest a one-line summary under 72 characters plus an optional body.
3. Let the user edit or accept the message.
4. Only if the user asks for it, offer an optional git commit-msg hook for this repository: show the exact hook file first, write it only to .git/hooks/commit-msg in this repository after the user says yes, and print the one command that removes it. Do not edit AGENTS.md, agent memory, shell startup files, cron or any file outside this repository.
5. Tell the user whether the hook was installed.
