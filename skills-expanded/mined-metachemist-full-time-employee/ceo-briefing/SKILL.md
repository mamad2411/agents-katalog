---
name: ceo-briefing
description: |
  Generate a structured CEO/owner briefing from vault state. Use when a
  BRIEFING_*.md file appears in vault/Inbox/ (placed by cron), or when
  the user asks for a daily/weekly summary. Reads Done/, Pending_Approval/,
  Plans/, Logs/, and Dashboard.md to produce a concise executive report
  written to vault/Briefings/. No human approval required — read-only action.
---

# CEO Briefing

Generate a daily or weekly executive briefing from vault state.

## When to Use

- A `BRIEFING_YYYY-MM-DD.md` file appears in `vault/Inbox/`
- User asks for a daily/weekly summary or status report
- Triggered by `scripts/generate_briefing.py` from cron

## What the Briefing Includes

1. **Headline metrics** — counts from Done, Pending_Approval, Failed, Needs_Action
2. **Actions completed** — list of Done/ items since last briefing
3. **Awaiting your approval** — summary of Pending_Approval/ items
4. **Failures to review** — any items in vault/Failed/
5. **Today's audit highlights** — key events from Logs/
6. **Open plans** — Plans/ items still in progress
7. **Recommended next steps** — 3 bullets for the owner

## Output

Briefing written to:
```
vault/Briefings/BRIEFING_<scope>_<YYYY-MM-DD>.md
```

## Cron Setup

```
# Daily briefing at 08:00 Mon-Fri
0 8 * * 1-5 cd /path/to/project && python .claude/skills/ceo-briefing/scripts/generate_briefing.py --scope daily >> logs/briefing.log 2>&1

# Weekly briefing at 09:00 Monday
0 9 * * 1 cd /path/to/project && python .claude/skills/ceo-briefing/scripts/generate_briefing.py --scope weekly >> logs/briefing.log 2>&1
```

## Rules

- **Always** write output to `vault/Briefings/` — never to Inbox or elsewhere
- **Never** send the briefing anywhere without human approval
- **Always** append a briefing-generated event to `vault/Logs/`
- Keep briefings under 800 words for readability
