---
name: events-in-town
skill_id: browser-skill:events-in-town
description: Everything worth knowing about happening where you live
when_to_use:
  - intent_keywords: [events, in town, local, this week, happening, my city]
    require_auth: false
    mutation_boundary: read_only
steps:
  - caption: events, shows, markets, openings and pop-ups happening this week
    capability_target: web_search
    mutation_boundary: read_only
  - caption: what locals say is actually worth going to this week
    capability_target: web_search
    mutation_boundary: read_only
trigger:
  kind: schedule
  recurrence: weekly
  weekday: 2
  time: 08:30
  timezone: America/Los_Angeles
  follows_device: true
parameters:
  - name: town
    current_value: in Los Angeles
    fill_rule: say your city and Luke uses it instead
adapter_preferences:
  preferred: browserbase
  fallback: owned_browser
  declined: []
schema_version: 1
metadata:
  luke:
    tags: [events, local, city, this week, going out]
    related_skills: [browser-skill:festival-season]
platforms: [macos]
---
# Events in town

## Purpose
Monday morning, everything on where the user lives this week, so the calendar fills up on Monday instead of the weekend arriving empty.

## Reads
- Search results for events, shows, markets, openings and pop-ups happening this week in Los Angeles.
- Search results for what locals say is actually worth going to this week in Los Angeles.

## Lands in
- Covers the whole week, grouped by day. Short enough to act on straight away.

## Steps
1. Look up events, shows, markets, openings and pop-ups happening this week in Los Angeles.
2. Look up what locals say is actually worth going to this week in Los Angeles.
3. Covers the whole week, grouped by day.

## Success criteria
- Covers the whole week, grouped by day.
- Leads with the one thing to build the week around.
- Names real venues and real times, and says what is free.

## Failure behavior
- If a source will not load, skip it and keep going.
- If there is genuinely nothing, say so in one line and move on.

## Never
- Never sign in, buy tickets, book, reserve or join a waitlist. Tell the user
  where and when, and let them do it themselves.
- Never invent an on-sale time, a price, a venue or a lineup.
- Never pass a resale listing off as a general sale.

## Redaction
Omit query strings, account details, ticket orders, saved cards, home address,
and anything shown after a page unexpectedly asks for a login.
