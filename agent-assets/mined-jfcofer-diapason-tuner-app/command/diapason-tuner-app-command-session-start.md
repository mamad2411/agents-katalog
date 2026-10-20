---
description: Load project context and pick up the active task
---

Start a working session on this repository by following `AGENTS.md` §2. The protocol lives there,
not here.

1. Run `just session-start`. It prints the reading order, the working tree, branches not merged into
   `main`, open PRs with their check verdicts, and `just doctor`.
2. Read what it lists, in that order: `docs/agents/STATE.md`, the active task file, and only the
   reference docs that task points to.

Then give me, in under fifteen lines:

- Where the project is and what the active task is.
- The concrete next action you propose, and roughly how you would do it.
- Every contradiction between STATE.md, the task file and what `session-start` printed: a PR
  merged or still open, a branch STATE does not mention, red checks. This is the most valuable thing
  you can report — a stale STATE.md silently misleads every later session.
- Any open question in STATE.md that blocks the next action.

Do not start implementing. Wait for me.
