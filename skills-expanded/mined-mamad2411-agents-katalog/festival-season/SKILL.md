---
name: festival-season
skill_id: browser-skill:festival-season
description: Lineups, tickets dropping, and who is playing where this summer
when_to_use:
  - intent_keywords: [festival, coachella, rolling loud, edc, lollapalooza, outside lands, lineup, tickets]
    require_auth: false
    mutation_boundary: read_only
steps:
  - caption: lineup announcements, ticket drops and dates for
    capability_target: web_search
    mutation_boundary: read_only
  - caption: what people are saying about this year's lineup for
    capability_target: web_search
    mutation_boundary: read_only
trigger:
  kind: schedule
  recurrence: weekly
  weekday: 3
  time: 08:30
  timezone: America/Los_Angeles
  follows_device: true
parameters:
  - name: festivals
    current_value: the major music festivals
    fill_rule: say which festivals you are chasing
adapter_preferences:
  preferred: browserbase
  fallback: owned_browser
  declined: []
schema_version: 1
metadata:
  luke:
    tags: [festivals, lineups, tickets, summer, travel]
    related_skills: []
platforms: [macos]
---
# Festival season

## Purpose
Tuesday, lineups and ticket dates for the festivals you're chasing. So you're there when they drop, and there in the summer.

## Reads
- Search results for lineup announcements, ticket drops and dates for the major music festivals.
- Search results for what people are saying about this year's lineup for the major music festivals.

## Lands in
- Says when tickets actually drop, with the date. Short enough to act on straight away.

## Steps
1. Look up lineup announcements, ticket drops and dates for the major music festivals.
2. Look up what people are saying about this year's lineup for the major music festivals.
3. Says when tickets actually drop, with the date.

## Success criteria
- Says when tickets actually drop, with the date.
- Names who was added to the lineup since last week.
- Flags the one that will sell out fastest.

## Failure behavior
- If a source will not load, skip it and keep going.
- If there is genuinely nothing, say so in one line and move on.

## Never
- Never sign in, buy tickets, book travel or join a waitlist.
- Never invent a date, a price, a lineup or a venue.
- Never pass a promoter's announcement off as independent reaction.

## Redaction
Omit query strings, account details, ticket orders, passport and booking
references, saved cards, home address, and anything shown after a page
unexpectedly asks for a login.
