---
name: romance-radar
skill_id: browser-skill:romance-radar
description: Something to do together that is better than another dinner
when_to_use:
  - intent_keywords: [romance, date, together, couple, anniversary, surprise]
    require_auth: false
    mutation_boundary: read_only
steps:
  - caption: genuinely good things for two people to do this week in
    capability_target: web_search
    mutation_boundary: read_only
  - caption: what people say was the best date they have had in
    capability_target: web_search
    mutation_boundary: read_only
trigger:
  kind: schedule
  recurrence: weekly
  weekday: 3
  time: 12:30
  timezone: America/Los_Angeles
  follows_device: true
parameters:
  - name: together
    current_value: Los Angeles
    fill_rule: say your city
adapter_preferences:
  preferred: browserbase
  fallback: owned_browser
  declined: []
schema_version: 1
metadata:
  luke:
    tags: [romance, dates, together, evenings]
    related_skills: []
platforms: [macos]
---
# Romance radar

## Purpose
One idea that is better than another dinner, with the timing that makes it work and the small thing that makes it feel planned.

## Reads
- Search results for genuinely good things for two people to do this week in Los Angeles.
- Search results for what people say was the best date they have had in Los Angeles.

## Lands in
- One idea, with a time and a place. Short enough to act on straight away.

## Steps
1. Look up genuinely good things for two people to do this week in Los Angeles.
2. Look up what people say was the best date they have had in Los Angeles.
3. One idea, with a time and a place.

## Success criteria
- One idea, with a time and a place.
- Names the small detail that makes it land: the hour, the seat, the thing to bring.
- Works for a first date and a fifth year, and says which it suits.
- Always has a cheap version.

## Failure behavior
- If a source will not load, skip it and keep going.
- If nothing is on, say so in one line and give the best fallback.

## Never
- Never sign in, book, buy tickets or reserve anything.
- Never invent a venue, a time, a price or a lineup.
- Never pass a promoted listing off as what people rate.

## Redaction
Omit query strings, account details, order history, saved cards, home address,
and anything shown after a page unexpectedly asks for a login.
