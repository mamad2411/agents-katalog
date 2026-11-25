---
name: weekly-action-report
description: Friday 4pm: generate weekly action log entry from Gmail, Google Calendar, and Claude sessions
---

> **Schedule:** Friday 4pm
> **Needs:** Gmail, Google Calendar
> **Helper scripts (yours, not included):** none

You are generating {{USER}}'s weekly action report. This runs every Friday at 4pm ET.

## Context Budget Rule

**This task runs in a single session with a finite context window.** A full week
of Gmail threads, calendar events, and Claude session transcripts can easily
cross the compaction threshold and trigger autocompact thrashing. Each data
source is read inside an isolated subagent that returns compact bullet-point
summaries. The parent session never holds raw Gmail threads or session
transcripts.

## What to do

1. **Determine the date range.** This entry covers Monday through today (Friday) of the current week.

2. **Pull data from three sources using isolated subagents:**

   Each source below runs in its own subagent. The subagent does the heavy reads
   and returns a **compact bullet list** (target: under 2,000 tokens each). The
   parent session receives only the summaries.

   a. **Gmail subagent** — Search for all threads from the past 7 days (sent and received). Return a compact bullet list of: key conversations, commitments made, follow-ups sent, decisions, new registrations, intros. Pay attention to threads with clients, SBDC colleagues, FNX Pearl contacts, and your [partner]. Skip routine/spam. Each bullet: one line max.

   b. **Google Calendar** (parent context — OK, structured data) — List all events from Monday through Friday of this week. Note who {{USER}} met with (attendee names), the meeting topic, and any patterns (recurring meetings vs. one-offs). Flag new stakeholders he hasn't met with before if possible.

   c. **Claude sessions subagent** — Read recent session transcripts to identify what projects were worked on, files created or modified, decisions made, and tools/skills used. Cover all workstations: SBDC, FNX Pearl, Northfork, Personal. Return a compact bullet list — one line per item.

3. **Synthesize into a structured entry** using the compact subagent returns and the bullet-based format below. The entry has six sections:

   - **Synthesis** — One paragraph (3-5 sentences) giving {{USER}} insight into his week: what he accomplished, patterns worth noticing, and anything that needs attention going into next week. Direct, warm, no filler.
   - **SBDC Client Meetings** — Bulleted list, grouped by day (Mon/Tue/Wed/Thu/Fri). Each bullet: `**Day:** Name / Company — meeting type (brief context)`. Include AI Co-Working Hour, AI Overflow, and any SBDC team meetings.
   - **Gmail Activity** — Bulleted list of notable email threads: new registrations, intros, follow-ups sent, key decisions, announcements. Skip routine/spam.
   - **Claude Sessions** — Bulleted list of what was worked on in Claude sessions this week: skills built, wiki updates, reports generated, dashboards refreshed, etc.
   - **Personal / Home** — Bulleted list of non-work items from the personal calendar (appointments, home services, family events). Skip if nothing notable.
   - **Open Loops** — Bulleted list of things carrying into next week that need follow-through.

4. **Append the entry** to `{{WORKSPACE_ROOT}}/action-log-2026.md`. Use this exact format:

```
## Week of [Month Day]–[Day], [Year]

### Synthesis

[One paragraph of insights about the week]

### SBDC Client Meetings

- **Mon:** Name — type (context)
- **Tue:** Name / Company — type (context)
[etc.]

### Gmail Activity

- Item one
- Item two

### Claude Sessions

- Item one
- Item two

### Personal / Home

- Item one

### Open Loops

- Item one
- Item two

```

## Important rules
- Append to the EXISTING file — never overwrite it. Read the file first, then write the full contents back with the new entry added at the bottom.
- If this is January and the file is `action-log-2026.md` but we're now in 2027, create `action-log-2027.md` instead.
- Keep each section tight — bullets should be one line each, not mini-paragraphs.
- Use plain language, not corporate filler.
- Name real people and real projects — this is a private journal, not a public doc.
- If a data source is unavailable (e.g., Gmail connector not responding), note that in the entry and proceed with what you have.

## {{USER}}'s context
- Timezone: America/New_York
- Email: {{YOUR_EMAIL}}
- Workstations: SBDC (UMD advising), FNX Pearl (consulting), Northfork (family farm), Personal
- Key people: [partner] (FNX Pearl partner), [supervisor] (SBDC supervisor), [spouse], [SBDC colleagues]
- The action log lives at the root of {{WORKSPACE_ROOT}}, not inside any workstation folder.
