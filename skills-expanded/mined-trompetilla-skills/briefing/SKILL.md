---
name: briefing
description: "Daily briefing: gathers today's calendar, active todos, and local weather from available workspace tools, then composes a concise summary."
metadata: {"openclaw":{"emoji":"📋"}}
user-invocable: true
disable-model-invocation: true
---

# Briefing

Compose a daily briefing by gathering data from available workspace sources.

## Step 1 — Discover sources

Check **TOOLS.md** and **USER.md** to determine which sources exist:

- **Calendar** -> available if `TOOLS.md` has a Calendar section with a skill/CLI reference.
- **Todos** -> available if `TOOLS.md` has a Todos section with a skill/CLI reference.
- **Weather** -> available if `USER.md` has a Location field (city, town, or region).

If **none** of the three are available — stop. Tell the user you have nothing to build a briefing from: no calendar skill, no todo skill, and no location for weather. Suggest adding a location to `USER.md` or configuring tools in `TOOLS.md`. Do not proceed. Do not fabricate a briefing.

## Step 2 — Determine briefing day

Decide whether the user's day is effectively over. Consider current time, the user's typical schedule (from memory, USER.md, or calendar patterns), and remaining events.

- Day still active → briefing covers **today**.
- Day winding down → briefing covers **tomorrow**.

All date-sensitive sections (calendar, weather) use the briefing day. Todos are not date-bound — always show active items regardless.

## Step 3 — Gather data

For each available source, collect data. Skip sources not detected in Step 1.

### Calendar

1. **Read the calendar skill's `SKILL.md` first** (path from TOOLS.md). Do not call the CLI without reading it.
2. Fetch the **briefing day's** agenda using the skill's documented commands.
3. If no events — note it.

### Todos

1. **Read the todo skill's `SKILL.md` first** (path from TOOLS.md). Do not call the CLI without reading it.
2. List **active/pending** items using the skill's documented commands.
3. If none — note "no active todos."

### Weather

1. Use the **web search tool** to look up weather for the **briefing day**. Query: `weather {today|tomorrow} in {location}` (location from USER.md).
2. Extract: current temperature, conditions, high/low, notable alerts.
3. Do NOT use `curl`, `wttr.in`, or other CLI tools for weather.

### On errors

If a tool command fails, skip that section and mention the failure briefly in the briefing (e.g. "Could not fetch calendar."). Do not retry more than once. Never fabricate data.

## Step 4 — Compose

Build a single message. Include only sections whose source was detected in Step 1. If a detected source returned no data (e.g. calendar exists but no events), still include the section with a one-line note.

### Structure

1. **Greeting** — one short casual line. Time-aware (morning/afternoon/evening). If the briefing day is tomorrow, mention it naturally (e.g. "Good evening — here's tomorrow").
2. **Weather** — 1–2 lines: temperature, sky, anything notable. Label as tomorrow's forecast when applicable.
3. **Calendar** — briefing day's events, chronologically. Format: `HH:MM — Title`. All-day events first. If empty: one line noting no events.
4. **Todos** — active items, briefly. Higher priority first if supported. If empty: "No active todos."

### Style

- When briefing day is tomorrow, make sure calendar header and weather header reflect that.
- Do not shorten the user's city name.
- Match the language of the user's request.
- Concise, skimmable, no filler.
- No preamble ("here is your briefing...") — dive straight in.
- Friendly but not chatty.
- Simple formatting — optimize for mobile chat. Bold section headers, short lines.
- Spacing: one empty line **between** sections, **zero** between a header and its content.
  - Right: `**Calendar**\n09:00 — Standup`
  - Wrong: `**Calendar**\n\n09:00 — Standup`
- Never invent events, todos, or weather data. Only report what tools returned.
- No call to action in the end - just the briefing.
