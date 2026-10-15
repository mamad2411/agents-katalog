---
name: tixmd-next
description: Pick the next best ready ticket and orchestrate the full work loop — work on each criterion, check it off, repeat until done. Use when the user wants to start working on the next task.
---

# /tixmd-next

Pick the next best ticket and work through it criterion by criterion.

## Instructions

1. **Read `.tixmd/project.md`** for project context and conventions (ticket style, commit strategy, definition of done).

2. **Find candidate tickets** by running:

```bash
npx tixmd list --status ready
```

If no ready tickets exist, inform the user and suggest using `/tixmd-groom` to refine spikes or `/tixmd-new` to create tickets.

3. **Pick the best candidate**. Read each ready ticket from `.tixmd/tixs/<ticket-id>.md`, then select the one most relevant to the project's current goals as described in `project.md`. Consider:
   - Alignment with the project vision and current priorities
   - Whether it unblocks other tickets
   - Natural sequencing (foundations before features)

4. **Present the selected ticket** to the user — show the title, description, and acceptance criteria. Ask the user to confirm before starting work. If the user prefers a different ticket, let them pick.

5. **Work loop** — after confirmation, iterate through the acceptance criteria:

   a. Read the ticket file to find the next unchecked criterion (`- [ ]`)
   b. If all criteria are checked, the ticket is done — congratulate the user and stop
   c. Work on the current criterion — implement the code changes needed to satisfy it
   d. Once the criterion is satisfied, check it off by editing the ticket file (change `- [ ]` to `- [x]` for that criterion)
   e. Inform the user of progress and what was done
   f. Go back to step (a)

6. **Respect project conventions** throughout:
   - Follow the **definition of done** — if the project requires linting/tests to pass, verify before marking criteria complete
   - Follow the **commit strategy** — if the project specifies one, apply it (e.g. commit after each criterion). If "up to the developer", let the user decide when to commit
