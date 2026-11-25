---
name: check
description: Check the current changes with Attentry and fix what this task added. Use when the person asks to check, review or clean up the changes, or before saying a task is done.
---

Call Attentry's `check` tool with no arguments: it lists the problems in the current changes,
security holes and crash risks first, then clean-up (copied and unused code).

- Fix the ones marked "(new in this task)" first: this task added them.
- For any finding whose fix isn't obvious, call Attentry's `explain` tool with its `file:line`.
- Older findings (not new in this task) are only worth mentioning, not fixing, unless the person asks.
- When it says there are no problems, say so in one line.
