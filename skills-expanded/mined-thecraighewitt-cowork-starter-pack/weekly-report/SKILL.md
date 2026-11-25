---
name: weekly-report
description: Produces a weekly report summarizing what happened this week — completed work, what stalled, decisions made, next week's priorities. Pulls from calendar, messaging, and any work logs in the project folder. Use when the user asks for a weekly report, Friday recap, weekly review, or end-of-week summary. Best run as a scheduled task late Friday afternoon.
---

# Weekly Report

Turn a week of meetings, messages, and scattered notes into a one-page recap the user can send to themselves, a manager, or a team — without spending 45 minutes writing it.

## Before starting

1. Read `context/about-me.md` — who is this report for, what does the user own?
2. Read `context/preferences.md` — what format does the user want? Who is the audience?
3. Read `context/voice.md` — for any narrative prose in the report.
4. Check `/output/` for last week's report — continuity matters. Did last week's priorities get done?

## What to produce

A markdown file saved to `/output/weekly-report-{YYYY-MM-DD}.md`, covering Monday through today (or a 7-day window if today isn't Friday).

Four sections:

1. **What moved this week** — 3–6 bullets. The wins, the meaningful progress, the decisions made. Specific. No vague "worked on X" — say what shipped, what got decided, what changed.
2. **What stalled or slipped** — 1–4 bullets. Honest. Don't cover things up. If something was on last week's list and didn't happen, say so and say why.
3. **Decisions & notable changes** — decisions taken this week that someone might want to know about later. One line each. (This section feeds a decision log over time.)
4. **Next week's focus** — 3 priorities, ranked. Each with one sentence of why.

## Inputs

- Calendar from the last 7 days
- Messages / Slack DMs from the last 7 days
- Last week's weekly report (if exists) — for continuity
- Any `/output/` files created this week — these are the trail of work done
- Any decision-journal entries in the project folder (if used)

## How it works

1. Pull the week's calendar — identify meetings that produced outputs (reviews, 1-1s, decisions)
2. Pull message/Slack history — look for commitments made, decisions mentioned, items closed
3. Scan `/output/` for files created/modified this week — this is the actual work trail
4. Compare to last week's "Next week's focus" — did those priorities move?
5. Draft the four sections
6. If the user specified an audience in `preferences.md` or `about-me.md`, tune the tone to that audience
7. Save the file, tell the user one-line what was notable

## What not to do

- Do not list every meeting. Only meetings that produced something.
- Do not pad. If the week was quiet, the report is short. A two-paragraph weekly report is better than a fake one-pager.
- Do not editorialize beyond what the evidence supports. "Team morale is high" is not something you can know from the data.
- Do not skip the "stalled" section because it's uncomfortable. That section is the whole point.

## Example output structure

```markdown
# Weekly Report — Week of 2026-04-14 to 2026-04-18

## What moved
- Shipped the Q2 planning doc; got sign-off from all three department heads
- Closed Northwind contract — signature on file, kickoff scheduled 4/28
- Hired new ops manager (starts 5/5) — offer accepted Wednesday
- Finished vendor migration to new payroll provider; first run clean

## What stalled
- Pricing review pushed to next week — blocked on finance model from Alex
- Board deck outline is still not started; needs 2 hours I haven't made

## Decisions & notable changes
- Decided to delay the Q3 hiring wave by one month (signal from April sales pipeline)
- Switched weekly reporting cadence from Monday to Friday (this report is the first)
- Approved the $18K spend on new analytics stack

## Next week's focus
1. Pricing review — unblock the finance model Monday morning. This is the #1 item on the quarterly plan.
2. Board deck — block 2 hours Tuesday. Draft is due Thursday.
3. Onboard new ops manager — calendar holds and 30/60/90 plan ready before 5/5.
```

## Customization notes

- **For a team report.** Add a fifth section: "Team highlights" — named callouts of who shipped what. Use sparingly; too many names and it reads like a bureaucratic formality.
- **For a self-only report.** Add a sixth section: "Energy & load" — one line on how the week *felt.* This is for future-you reading back in three months.
- **For manager reports.** Tighten "What stalled" to include what you're doing about it, not just what's stuck.
