---
name: brief
description: Generate a concise briefing on current state, priorities, and blockers
---

# Brief — Status Briefing

Generate a concise, actionable briefing for your partner.

## Process

1. Read `ion/state.md` for current snapshot
2. Read `ops/action-items.md` for open items and overdue tasks
3. Read recent files in `knowledge/decisions/` (last 7 days)
4. Read recent files in `knowledge/meetings/` or `knowledge/journal/` (last 7 days)
5. Scan mode-relevant areas for status:
   - **Company mode**: `product/`, `customers/`, `financials/`
   - **Personal mode**: `goals/current.md`, `projects/active.md`
   - **Creative mode**: `drafts/`, `plot/`
   - **Research mode**: `experiments/active.md`, `findings/preliminary.md`

## Output Format

```
# Brief — [Date]

## Where We Are
[2-3 sentences on the current situation and what matters most right now]

## Open Action Items
[Grouped by owner if multiple people, otherwise as a flat list]

## Recent Decisions
[Decisions from the last 7 days — title, date, one-line summary]

## Attention Needed
[Anything overdue, contradictory, at risk, or time-sensitive]

## Status
[Mode-specific status block: pilot status, project status, current sprint, etc.]
```

## Rules

- Keep it to one page
- Be direct
- Flag problems clearly — don't bury them in qualifications
- If something is overdue, lead with it
- Don't pad — if there's nothing to report in a section, omit it
