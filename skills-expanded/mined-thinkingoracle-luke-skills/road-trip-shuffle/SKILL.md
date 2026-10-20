---
name: road-trip-shuffle
skill_id: browser-skill:road-trip-shuffle
description: A drive worth doing this weekend with the stops that make it good
when_to_use:
  - intent_keywords: [scenic drive, road trip, day trip, drive, route, back roads, stops]
    require_auth: false
    mutation_boundary: read_only
steps:
  - caption: best scenic drives and day trip routes starting from
    capability_target: web_search
    mutation_boundary: read_only
  - caption: roadside stops, viewpoints and places to eat along scenic routes from
    capability_target: web_search
    mutation_boundary: read_only
trigger:
  kind: schedule
  recurrence: weekly
  weekday: 7
  time: 08:30
  timezone: America/Los_Angeles
  follows_device: true
parameters:
  - name: route
    current_value: scenic drives in Los Angeles
    fill_rule: say your city and Luke uses it instead
adapter_preferences:
  preferred: browserbase
  fallback: owned_browser
  declined: []
schema_version: 1
metadata:
  luke:
    tags: [road trip, scenic drive, day trip, weekend, weekly]
    related_skills: [browser-skill:weekend-escape]
platforms: [macos]
---
# Road trip shuffle

## Purpose
Saturday morning, tank half full and the day wide open. One route worth driving,
with the two or three stops that turn a drive into a day.

## Reads
- Search results for best scenic drives and day trip routes starting from scenic drives in Los Angeles.
- Search results for roadside stops, viewpoints and places to eat along scenic routes from scenic drives in Los Angeles.

## Lands in
- Names one route with a real total drive time, out and back. Short enough to act on straight away.

## Steps
1. Look up best scenic drives and day trip routes starting from scenic drives in Los Angeles.
2. Look up roadside stops, viewpoints and places to eat along scenic routes from scenic drives in Los Angeles.
3. Names one route with a real total drive time, out and back.

## Success criteria
- Names one route with a real total drive time, out and back.
- Gives two or three stops in driving order, with one place to eat.
- Says when to leave so the best stretch is not driven in the dark.

## Failure behavior
- If a source will not load, skip it and keep going.
- If a road is closed, say so in one line and give the route that goes around it.

## Never
- Never sign in, book a table or buy a pass.
- Never invent a route, a drive time or a stop along the way.
- Never pass a sponsored roadside listing off as a real recommendation.

## Redaction
Omit query strings, account details, order history, saved cards, home address,
and anything shown after a page unexpectedly asks for a login.
