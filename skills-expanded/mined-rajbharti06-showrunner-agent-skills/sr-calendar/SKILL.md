---
name: sr-calendar
description: Builds a content calendar sized to the hours the person actually has. Takes the hub platform, spokes, weekly hours, stage, formats and pillars, then lays out weeks of posts with the main piece first and adapted versions the next day, rotating pillars, protecting time for replies, and exporting to Markdown, CSV, an .ics file for Google, Apple or Outlook calendars, or JSON. Use when someone asks for a posting schedule, a content calendar, a month plan, or how often to post. It does not post anything.
license: MIT
compatibility: Any agent that loads Agent Skills. Python 3.9+ for the calendar engine; the by-hand method below works without it.
metadata:
  author: Raj Bharti
  version: "0.1.2"
  family: showrunner
---

# Calendar

A calendar the person cannot keep is worse than none. This one starts from hours, not from a wish.

## Ask first

If the profile is saved (`profile_get`), use it. Otherwise ask:

- Hub platform and spokes (from `sr-strategy`).
- Hours per week they can truly give. Be honest about it.
- Stage: zero, seed, growing or established.
- Formats they make: short video, long video, carousel, text. One or several.
- Two to five pillars.
- Start date. Default is next Monday.
- Posting times: only from their own analytics. If they have none, leave it blank and say the times are placeholders.

## Build

Tool `calendar_build`. CLI:

```
python scripts/sr.py calendar --hub youtube --spokes instagram,linkedin --hours-per-week 6 --stage zero --content-type long_video --weeks 4 --pillars "interviews,projects,tools" --format markdown
```

`--format ics` writes a calendar file the person imports into Google, Apple or Outlook. `csv` suits a spreadsheet and `json` suits other tools.

## How the engine decides

It estimates effort in minutes per piece (a long video about 360, a short video about 70, a carousel about 55, a text post about 15, a story about 10). Spoke versions cost about 30% of the original because they adapt an existing piece. It holds back 15% of the hours for replies and community (`sr-engage`), and gives a batching discount of 20% when similar pieces are made together. When the plan does not fit, it trims in this order: hub side formats first (stories, then carousels), then spokes, then the hub's own count, but never below one hub piece a week. It tells the person what it cut. These numbers are planning estimates from the maintainer, not measured facts. Ask the person to adjust them after two weeks of real data.

## Check the result

- Does it fit the hours, with room to spare?
- Is the hub piece first, with spokes the next day?
- Are pillars rotating, not repeating the same one?
- Is anything cut that the person cares about? Say so and ask.

## Present

Give the person the calendar in the format they asked for, and a three-line summary: pieces per week, hours used, what was left out. Offer to start the weekly sprint (`playbook_start weekly-sprint`).

## Adjust

Posting frequency is not a lever with a known best value. Consistency the person can keep beats a heroic plan. After four weeks, compare results with the plan (`sr-audit`).

## Gate

`approve`. The person posts.

## Do not

- Fill every day because empty cells look bad.
- Invent best times to post. Use their analytics or leave it blank.
- Schedule a flood of identical posts across platforms on the same day.
