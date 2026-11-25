---
name: clear-and-prime
description: Reset session and reload project context. Use when switching to an unrelated task, or when starting fresh after a long session.
allowed-tools: Bash, Read, Glob
disable-model-invocation: true
---

# Clear and prime

Combines `/clear` and `/prime` for clean task transitions.

## Process

1. Tell the user what's about to happen ("Clearing context, then re-priming").
2. Run `/clear` to reset the conversation.
3. Run `/prime` to reload CLAUDE.md, README.md, and `.claude/rules/`.
4. Confirm ready to start the new task.

## When to use

- Switching from one feature to an unrelated one.
- After a long debugging session where context is noisy.
- Returning to a project after a break (start of day).

## When NOT to use

- Mid-task: you'll lose the thread. Use `/compact <focus>` instead.
- Right before a commit: you need the recent context to write a good message.
