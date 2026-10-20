---
name: party-hard
skill_id: browser-skill:party-hard
description: Where the night actually goes off, and what time to get there
when_to_use:
  - intent_keywords: [party, club, rave, night out, dj, dancing, warehouse, afters]
    require_auth: false
    mutation_boundary: read_only
steps:
  - caption: best parties, club nights and DJ sets happening this weekend in
    capability_target: web_search
    mutation_boundary: read_only
  - caption: which nights people say actually go off in
    capability_target: web_search
    mutation_boundary: read_only
trigger:
  kind: schedule
  recurrence: weekly
  weekday: 6
  time: 17:15
  timezone: America/Los_Angeles
  follows_device: true
parameters:
  - name: scene
    current_value: best clubs and parties in Los Angeles
    fill_rule: say your city and Luke uses it instead
adapter_preferences:
  preferred: browserbase
  fallback: owned_browser
  declined: []
schema_version: 1
metadata:
  luke:
    tags: [party, clubs, nightlife, dancing, music]
    related_skills: []
platforms: [macos]
---
# Party hard

## Purpose
Where it is actually going off this weekend, what time to get there, and what it costs on the door. One place, not a listings page.

## Reads
- Search results for best parties, club nights and DJ sets happening this weekend in best clubs and parties in Los Angeles.
- Search results for which nights people say actually go off in best clubs and parties in Los Angeles.

## Lands in
- One place. Short enough to act on straight away.

## Steps
1. Look up best parties, club nights and DJ sets happening this weekend in best clubs and parties in Los Angeles.
2. Look up which nights people say actually go off in best clubs and parties in Los Angeles.
3. One place. Door time, door price, and who is playing.

## Success criteria
- One place. Door time, door price, and who is playing.
- Says when to arrive, because turning up at the wrong hour is the whole game.
- Names the one that is genuinely good, not the one with the most ads.
- Adds where people go after, if there is an after.

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
