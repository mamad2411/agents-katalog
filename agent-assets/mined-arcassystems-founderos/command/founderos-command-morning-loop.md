---
description: The morning answer loop. Say "morning loop" or run /founder-os:morning-loop. At most four sharp questions drawn from what is actually waiting, every answer written back to the file that owns it, then one coach line naming today's single step. Once a day.
allowed-tools: ["Read", "Edit", "Write", "Grep", "Glob", "Bash"]
---

# Founder OS morning loop

Run the morning-loop skill at `skills/morning-loop/SKILL.md` end to end.

## Procedure

1. Check `brain/log.md` for a `#morning-loop` entry dated today. If one exists, say so and stop unless the founder explicitly asks to run it again.
2. Read `skills/morning-loop/SKILL.md`.
3. Gather silently (step 1), pick at most four questions (step 2), ask them in one batch with a recommendation first on each.
4. Write every answer back through the owning file, then close the thing that raised it.
5. Score yesterday's coach line and name today's one step. Write the `Coach:` line into the closing log entry.
6. Report in under 15 lines, ending with the coach line in plain words.

## Rules

- Four questions maximum. If nothing qualifies, say "Nothing needs you this morning" and stop. Never invent a question to fill the batch.
- Every answer lands in a file, and the source that asked gets closed in the same pass.
- Parse a freeform answer ("1 yes, 2 skip") rather than asking for a tidier format.
- Never send anything, never run a recurring job, never start a build.
- No em dashes or en dashes. No banned words.
