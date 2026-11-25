---
name: heat-day
skill_id: browser-skill:heat-day
description: It's hot. Here's where to be, and what to wear getting there
when_to_use:
  - intent_keywords: [hot, heat, summer, beach, pool, bikini, swim, sunny]
    require_auth: false
    mutation_boundary: read_only
steps:
  - caption: best places to swim, sunbathe and cool off today near
    capability_target: web_search
    mutation_boundary: read_only
  - caption: where people actually go on the hottest days in
    capability_target: web_search
    mutation_boundary: read_only
trigger:
  kind: schedule
  recurrence: daily
  time: 08:30
  timezone: America/Los_Angeles
  follows_device: true
parameters:
  - name: area
    current_value: best places to swim and sunbathe in Los Angeles
    fill_rule: say your city and Luke uses it instead
adapter_preferences:
  preferred: browserbase
  fallback: owned_browser
  declined: []
schema_version: 1
metadata:
  luke:
    tags: [summer, swimming, beach, heat, outdoors]
    related_skills: []
platforms: [macos]
---
# Heat day

## Purpose
It hit the temperature where staying in is a waste. Where the water is, what time to go, and the thing everyone forgets to bring.

## Reads
- Search results for best places to swim, sunbathe and cool off today near best places to swim and sunbathe in Los Angeles.
- Search results for where people actually go on the hottest days in best places to swim and sunbathe in Los Angeles.

## Lands in
- One spot, with how to get there and when it gets busy. Short enough to act on straight away.

## Steps
1. Look up best places to swim, sunbathe and cool off today near best places to swim and sunbathe in Los Angeles.
2. Look up where people actually go on the hottest days in best places to swim and sunbathe in Los Angeles.
3. One spot, with how to get there and when it gets busy.

## Success criteria
- One spot, with how to get there and when it gets busy.
- Says the water situation honestly: warm, freezing, or a pool.
- Names the one thing people forget. Shade, cash, a towel, a reservation.
- Has a walkable option and a worth-the-drive option.

## Failure behavior
- If a listing will not load, skip it and keep going.
- If nothing good is on, say so in one line and name the reliable fallback.

## Never
- Never sign in, book, buy tickets or reserve anything.
- Never invent a price, an opening time, a venue or an appointment.
- Never pass a promoted listing off as what people rate.

## Redaction
Omit query strings, account details, order history, saved cards, home address,
and anything shown after a page unexpectedly asks for a login.
