---
name: deadline-triage
description: Triage deadlines from user-supplied calendar or task exports. Use when prioritizing what is due soon. Do not invent deadlines or replace the user's calendar or task app as source of truth.
---

# Deadline Triage

1. Accept only user-supplied calendar/task exports or explicit lists.
2. Rank by due date and stated priority; mark UNKNOWN when dates are missing.
3. Propose a short ordered list. Do not create calendar events or silently reschedule.
4. Exit if the user's calendar/task app already answers better (beats-baseline check).

Output matches `schemas/personal/deadline-triage.schema.json`.
