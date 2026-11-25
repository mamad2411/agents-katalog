---
name: morning-brief
description: Compiles a single morning brief from weather, calendar, unread email themes, and yesterday's carried-over priorities. Use when the user says "morning brief", "compile my morning brief", "what's my day look like", "brief me", or wants a scheduled weekday-morning summary. Don't use for end-of-week reflection (use weekly-review) or working the inbox item-by-item (use email-triage).
version: 1.0.0
author: Gen AI Hub
license: MIT
metadata:
  hermes:
    tags: [Productivity, Automation, Daily-Brief]
    related_skills: [weekly-review, email-triage, calendar-concierge]
    blueprint:
      schedule: "0 8 * * 1-5"
      prompt: "Compile my morning brief"
---

# Morning Brief

Produces one tight, scannable brief at the start of the workday: weather, today's calendar, what's piling up in email, and the top 3 priorities carried from yesterday. The standard: every section either has real data or says plainly why it doesn't — no invented content, no silent gaps.

## When to Use

- Scheduled weekday run (the blueprint fires at 08:00 Mon–Fri with "Compile my morning brief").
- User asks "brief me", "what's on today", "morning brief".
- **Not for:** end-of-week reflection (use `weekly-review`) or working the inbox item-by-item (use `email-triage`).

## Quick Reference

| Action | Command / Call |
|---|---|
| Today's date | `date "+%A, %B %d, %Y"` |
| Weather (one line) | `curl -s --max-time 10 "wttr.in/?format=3"` |
| Weather (specific city) | `curl -s --max-time 10 "wttr.in/Singapore?format=3"` |
| Calendar | Connected calendar tool: list today's events |
| Unread email themes | Connected email tool: search unread, group by sender/subject |
| Yesterday's note | `ls` the user's notes folder for the most recent daily note, then `read_file` it |

## Procedure

1. **Precheck** — run `date "+%A, %B %d, %Y"` for the header. Note which sources are available this session: weather (curl works everywhere), calendar tool connected?, email tool connected?, notes folder known? Missing sources are fine — you'll degrade gracefully in step 6.
2. **Weather** — `curl -s --max-time 10 "wttr.in/?format=3"` (auto-locates by IP; append a city like `wttr.in/Singapore?format=3` if the user has a known location). Success looks like `Singapore: ⛅️ +29°C`. If the command times out or returns HTML, the section reads "Weather unavailable right now."
3. **Calendar** — if a calendar tool is connected, list today's events; keep only start time, title, and count of attendees. Flag the first event and any back-to-back stretch. If no calendar is connected, the section reads "Calendar not connected — nothing scheduled that I can see."
4. **Email themes** — if an email tool is connected, scan unread from the last 24h. Do NOT list every message; cluster into 2–4 themes ("3 threads about the cohort launch", "1 invoice awaiting reply"). Never open attachments, never send anything.
5. **Carried priorities** — find yesterday's daily note or task list (ask once where it lives if unknown, then remember). Pull unfinished items and pick the top 3 by deadline and impact. If no note exists, say so and suggest today's top 3 from calendar + email context instead.
6. **Deliver** — output the template below. Every section present; unavailable sources say so in one line rather than disappearing. Total length under 25 lines.

## Output Template

```
# Morning Brief — {Weekday, Month DD}

**Weather:** {one line, or "Weather unavailable right now"}

**Today's calendar:** {N events, first at HH:MM — or "Calendar not connected..."}
- HH:MM {Event} ({attendees})
- ...

**Inbox themes ({N} unread):**
- {Theme 1 — count}
- {Theme 2 — count}

**Top 3 today (carried from yesterday):**
1. {Priority — why it's #1}
2. {Priority}
3. {Priority}

**One heads-up:** {the single thing most likely to derail the day, if any}
```

## Pitfalls

- **wttr.in returns an HTML error page or rate-limit text instead of the one-liner** — detect it (output longer than ~80 chars or contains `<`), retry once, then write "Weather unavailable right now" and move on. Never paste raw HTML into the brief.
- **No calendar/email connected, agent invents plausible events** — this is the cardinal sin. If a source isn't reachable, the section must say it isn't. A brief with honest gaps beats a confident fake.
- **Yesterday's note can't be found, so priorities section is skipped silently** — don't skip; state "No note from yesterday found" and derive 3 suggested priorities from what you *can* see, labeled as suggestions.
- **Brief balloons past a screen** — the user reads this in 30 seconds. Cluster emails into themes, cap calendar lines at 6, cut anything that isn't decision-relevant.

## Verification

- [ ] Output matches the template — all five sections present
- [ ] Weather line is real curl output or an explicit "unavailable" line (no HTML fragments)
- [ ] No calendar events or emails were invented; unavailable sources are labeled as such
- [ ] Top 3 traces to yesterday's actual note, or is clearly labeled "suggested"
- [ ] Nothing was sent, replied to, or deleted while gathering — read-only run
- [ ] Brief fits in ~25 lines
