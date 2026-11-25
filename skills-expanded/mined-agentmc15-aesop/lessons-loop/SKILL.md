---
name: lessons-loop
description: Capture a durable lesson every time the human corrects the agent, so the same mistake doesn't recur. Use immediately after any user correction, course-correction, or "no, do it this way". Also use at session start to load relevant past lessons. Trigger on corrections and on session start.
---
# lessons-loop

A prompted-Reflexion pattern: the model forgets between runs, so lessons live on disk. After a
correction, write down the pattern and a rule that prevents it; review lessons at session start.
Iterate until the mistake rate drops.

## Steps
1. **On correction:** append to `tasks/lessons.md` an entry with: the failure pattern, the lesson
   (a rule for next time), and the contexts it applies to.
2. **On session start:** read `tasks/lessons.md`; surface the lessons relevant to the current task.
3. **Hygiene:** deduplicate, keep entries concise, add a date, and prune stale/contradicted ones so
   bad lessons don't pollute future behavior.

## Example entry
```json
{"failure_pattern": "matched Stripe email to Google email to assign credits", "lesson": "correlate accounts by persistent user ID, never email", "applies_to": ["payments", "auth", "identity"]}
```

## Notes
- Keep lessons project-scoped to avoid leaking one project's quirks into another.
- This is the same trick the eval harness uses: every production failure becomes a durable test/rule.
