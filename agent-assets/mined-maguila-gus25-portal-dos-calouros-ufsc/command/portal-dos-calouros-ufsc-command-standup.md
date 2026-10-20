---
description: Quick read-only status check — summarizes sprint progress, blockers, and next steps from docs/SPRINT.md and recent git history.
---

Act as the **Scrum Master**, giving a quick standup update. This is a **read-only** ritual — no file writes unless a blocker needs to be recorded.

1. Read `docs/SPRINT.md` and run `git log --oneline -10`.
2. Output a 3-part summary:
   - **Done since last standup**: stories marked Done, with a one-line note each.
   - **In progress**: stories currently In Progress, and what's left.
   - **Blockers / next steps**: any Blocked stories (with reason) and what should happen next (e.g. "ready for /sprint-run", "needs /sprint-plan").

Keep it short — this is a status check, not a report.
