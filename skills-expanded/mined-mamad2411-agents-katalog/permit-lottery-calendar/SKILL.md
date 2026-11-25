---
name: permit-lottery-calendar
skill_id: browser-skill:permit-lottery-calendar
description: The permit lottery closing next, and the back door if you missed it
when_to_use:
  - intent_keywords: [permit, lottery, wilderness permit, timed entry, half dome, whitney, backpacking, quota]
    require_auth: false
    mutation_boundary: read_only
steps:
  - caption: wilderness permit lottery application dates and results timeline
    capability_target: web_search
    mutation_boundary: read_only
  - caption: walk up permits daily lottery and last minute release for
    capability_target: web_search
    mutation_boundary: read_only
trigger:
  kind: schedule
  recurrence: weekly
  weekday: 1
  time: 08:30
  timezone: America/Los_Angeles
  follows_device: true
parameters:
  - name: permit
    current_value: wilderness permit lottery dates 2026
    fill_rule: name the hike, park or river you want a permit for
adapter_preferences:
  preferred: browserbase
  fallback: owned_browser
  declined: []
schema_version: 1
metadata:
  luke:
    tags: [permits, lottery, hiking, backpacking, weekly]
    related_skills: [browser-skill:trail-today]
platforms: [macos]
---
# Permit lottery calendar

## Purpose
Sunday morning, coffee in hand, the big trip still a maybe. The famous hikes are
not won on the day, they are won on a date months earlier that almost nobody has
in their calendar. This puts the next closing window in front of you while you
can still act on it.

## Reads
- Search results for wilderness permit lottery application dates and results timeline wilderness permit lottery dates 2026.
- Search results for walk up permits daily lottery and last minute release for wilderness permit lottery dates 2026.

## Lands in
- Names a real window with real dates. Short enough to act on straight away.

## Steps
1. Look up wilderness permit lottery application dates and results timeline wilderness permit lottery dates 2026.
2. Look up walk up permits daily lottery and last minute release for wilderness permit lottery dates 2026.
3. Names a real window with real dates. The big ones cluster early in the year and then shut for good: Mount Whitney applications run February 1 to March 1 with results March 15, the Enchantments lottery opens February 15, Half Dome runs the whole of March with results in mid April, and The Wave runs rolling monthly four months ahead instead of once a year.

## Success criteria
- Names a real window with real dates. The big ones cluster early in the year and
  then shut for good: Mount Whitney applications run February 1 to March 1 with
  results March 15, the Enchantments lottery opens February 15, Half Dome runs
  the whole of March with results in mid April, and The Wave runs rolling monthly
  four months ahead instead of once a year.
- Names the back door, which is where most people actually get in. Yosemite holds
  back 40 percent of its wilderness quota and releases it seven days before your
  start date at 7am Pacific. Half Dome runs a daily lottery two days out, open
  midnight to 4pm Pacific. Enchantments runs a walk up lottery for people who lost
  the annual one.
- Separates a permit from a park entry ticket, because they are different lines.
  Only a handful of parks still run timed entry in 2026, and Yosemite, Glacier,
  Arches and Mount Rainier dropped theirs. Rocky Mountain still needs one for the
  Bear Lake corridor from 5am to 6pm, and releases extra tickets at 7pm Mountain
  the night before, which is the easiest ticket in the system to get.
- Says the first move plainly: pick your date and your group size now, because
  every lottery form asks for both and a vague application is a wasted one.

## Failure behavior
- If a permit page will not load, skip it and keep going.
- If the lottery already closed for the year, say so in one line and lead with the
  walk up or short notice path instead.

## Never
- Never sign in, enter a lottery, apply for a permit or pay a fee.
- Never invent a lottery date, a quota, a fee or a results timeline.
- Never present a reseller or third party permit site as an official source.

## Redaction
Omit query strings, account details, order history, saved cards, home address,
and anything shown after a page unexpectedly asks for a login.
