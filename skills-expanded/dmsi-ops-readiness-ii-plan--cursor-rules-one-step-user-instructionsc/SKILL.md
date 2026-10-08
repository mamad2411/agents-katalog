---
description: When directing the user through manual steps (AWS, GitHub UI, Confluence, etc.), give only one step per reply; wait for their confirmation before the next.
alwaysApply: true
---

# One step at a time (user instructions)

- When the **user** must do something in a browser, AWS Console, GitHub Settings, or another UI, give **exactly one** clear action per message (one screen, one field, one button — not a numbered list of many steps).
- End with a short prompt to reply when done (e.g. “Reply **done** and we’ll do the next step”).
- **Wait** for the user to confirm before describing the next step.
- **Exception:** If the user explicitly asks for the full checklist, outline, or “all steps,” you may provide a compact list in that reply only.
- This does **not** block the agent from running multiple terminal commands in Agent mode when automating work — it governs **user-facing** procedural guidance.

Nick asked for this pacing to reduce overload; default to it unless he opts out for a given question.
