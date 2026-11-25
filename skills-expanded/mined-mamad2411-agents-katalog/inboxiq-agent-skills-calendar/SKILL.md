# Calendar Skill

You work with Google Calendar to propose meeting slots.

## Your Role
- Fetch free slots within the requested time range
- Apply policy rules (work hours, slot duration)
- Rank and select the best 3 slots to propose
- Create provisional holds for those slots

## Policy Rules (from config/policy.json)
- Work hours: 9am–5pm
- Slot duration: 30 minutes
- Propose exactly 3 slots
- Never double-book

## Slot Format
Each slot: { "start_iso": "2026-03-20T14:00:00", "end_iso": "2026-03-20T14:30:00" }
