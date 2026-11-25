---
name: conduct-handoff
description: "Update HANDOFF.md so any AI (or a new session) can continue the work"
disable-model-invocation: true
allowed-tools: "Read, Edit, Bash(git status:*), Bash(git log:*), Bash(git branch:*), Bash(git stash list), Bash(conductor-ai status:*)"
---

Update `HANDOFF.md` from the facts: `git log --oneline -15`, `git status`, the active plan's task statuses, `conductor-ai status`, and this session. Fill in Done, In progress, Next up (with exact commands), Problems, and provider notes. Keep it under 40 lines and don't invent progress.

Then tell the user: if the controller runs out of usage, they can open another agent (e.g. `agy` or `codex`) here and say "Read HANDOFF.md and act as the controller described in .conductor-ai/ORCHESTRATOR.md."
