---
description: Manage the work queue. Say "what's on my plate", "what's moving", or "add to queue: <thing>" (or run /founder-os:queue). Shows ACTIVE items, adds to BACKLOG, moves items between states. ACTIVE is capped at 3.
allowed-tools: ["Read", "Edit", "Write", "Glob"]
---

# Founder OS queue

Work queue management. Reads and updates `cadence/queue.md`.

## Procedure

1. Read the queue skill at `skills/queue/SKILL.md` and execute it end to end.

2. Pass `$ARGUMENTS` as the natural-language input to the skill. The skill parses the
   operation (read, add, start, done, park) from plain English. Examples:
   - No arguments: execute the `read` operation.
   - "add: write the Q3 brief" or "add to queue: write the Q3 brief": execute `add`.
   - "start the Q3 brief" or "start 1": execute `start`.
   - "done with Q3 brief" or "mark done: Q3 brief": execute `done`.
   - "park the Q3 brief": execute `park`.

3. If the skill file is missing, reply: `Queue skill not found at skills/queue/SKILL.md.
   Restarting Claude Code fixes this most of the time, because it reloads what is installed. If it happens again after a restart, say "update Founder OS".` and stop.

## Rules

- No em dashes or en dashes. Hyphens only.
- If `cadence/queue.md` is missing, create it from `templates/cadence/queue.md` first.
- ACTIVE is hard-capped at 3. The skill handles the gate. Do not bypass it.
