---
name: commit-message
description: Write a short, clear commit message for the staged changes.
disable-model-invocation: true
allowed-tools:
  - Bash(git status *)
  - Bash(git diff *)
---

Run git status and git diff --staged, then write a commit message:

- First line: under 60 characters, says what changed.
- Then 1 to 3 short bullet points on why.
- If nothing is staged, tell me and stop.

Show me the message. Don't commit until I say so.
