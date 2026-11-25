---
name: write-lesson
description: Record a notable failure, fix, or surprise as a lessons entry so future work avoids repeating mistakes. Use after debugging incidents, regressions, or high-value discoveries.
---

# Write Lesson

Capture high-signal operational learning in `docs/lessons/`.

## Trigger conditions

Use when work reveals:

- A preventable failure or regression.
- A surprising root cause.
- A useful debugging pattern.
- A process improvement worth preserving.

## Procedure

1. Read `docs/lessons/template.md`.
2. Create a new markdown file under `docs/lessons/` with a concise kebab-case title.
3. Fill all template fields:
   - Date
   - Context
   - What happened
   - Root cause
   - Fix/takeaway
   - Reference
4. Prefer concrete details over generic advice.

## Quality bar

- Includes one clear prevention action.
- References supporting issue/PR/commit when available.
- Written so someone new can apply the lesson quickly.
