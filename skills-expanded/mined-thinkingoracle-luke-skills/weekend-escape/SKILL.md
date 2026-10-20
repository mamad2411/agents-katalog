---
name: weekend-escape
skill_id: browser-skill:weekend-escape
description: A road trip or overnight within a few hours, decided Friday
when_to_use:
  - intent_keywords: [road trip, weekend away, overnight, escape, getaway, drive, out of town]
    require_auth: false
    mutation_boundary: read_only
steps:
  - caption: best weekend road trips and overnight escapes
    capability_target: web_search
    mutation_boundary: read_only
  - caption: small towns, cabins and coast stops worth an overnight trip
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
  - name: range
    current_value: in Los Angeles
    fill_rule: say your city and Luke uses it instead
adapter_preferences:
  preferred: browserbase
  fallback: owned_browser
  declined: []
schema_version: 1
metadata:
  luke:
    tags: [road trip, weekend, travel, escape, weekly]
    related_skills: [browser-skill:trip-ideas]
platforms: [macos]
---
# Weekend escape

## Purpose
Friday afternoon, right when leaving town still sounds like a great idea. One
place worth driving to, close enough that you can pack a bag and go.

## Reads
- Search results for best weekend road trips and overnight escapes in Los Angeles.
- Search results for small towns, cabins and coast stops worth an overnight trip in Los Angeles.

## Lands in
- One destination with a real drive time, not a list of every town nearby. Short enough to act on straight away.

## Steps
1. Look up best weekend road trips and overnight escapes in Los Angeles.
2. Look up small towns, cabins and coast stops worth an overnight trip in Los Angeles.
3. One destination with a real drive time, not a list of every town nearby.

## Success criteria
- One destination with a real drive time, not a list of every town nearby.
- Names one thing to actually do or eat there, so the trip has a shape.
- Gives one closer backup for a lighter, shorter version of the same idea.

## Failure behavior
- If a source will not load, skip it and keep going.
- If nothing new turns up, name a place worth returning to and say why.

## Never
- Never sign in, book a room, or buy anything.
- Never invent a drive time, a place, or a price.
- Never pass a sponsored listing off as a real recommendation.

## Redaction
Omit query strings, account details, order history, saved cards, home address,
and anything shown after a page unexpectedly asks for a login.
