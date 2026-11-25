---
name: swim-and-sun
skill_id: browser-skill:swim-and-sun
description: Water worth getting to this week, lakes, coast, springs and pools
when_to_use:
  - intent_keywords: [swim, swimming, lake, beach, river, springs, pool, water]
    require_auth: false
    mutation_boundary: read_only
steps:
  - caption: best places to swim, lakes, beaches, springs and outdoor pools near
    capability_target: web_search
    mutation_boundary: read_only
  - caption: water temperature, water quality and parking this week at swim spots near
    capability_target: web_search
    mutation_boundary: read_only
trigger:
  kind: schedule
  recurrence: weekly
  weekday: 4
  time: 12:30
  timezone: America/Los_Angeles
  follows_device: true
parameters:
  - name: water
    current_value: swimming spots in Los Angeles
    fill_rule: say your city and Luke uses it instead
adapter_preferences:
  preferred: browserbase
  fallback: owned_browser
  declined: []
schema_version: 1
metadata:
  luke:
    tags: [swimming, lakes, beach, summer, weekly]
    related_skills: [browser-skill:trail-today]
platforms: [macos]
---
# Swim and sun

## Purpose
Wednesday lunchtime, when the week is long enough that water sounds like the
answer. One place to get in, close enough to reach after work.

## Reads
- Search results for best places to swim, lakes, beaches, springs and outdoor pools near swimming spots in Los Angeles.
- Search results for water temperature, water quality and parking this week at swim spots near swimming spots in Los Angeles.

## Lands in
- Names one spot with a real drive time and a real sense of the water. Short enough to act on straight away.

## Steps
1. Look up best places to swim, lakes, beaches, springs and outdoor pools near swimming spots in Los Angeles.
2. Look up water temperature, water quality and parking this week at swim spots near swimming spots in Los Angeles.
3. Names one spot with a real drive time and a real sense of the water.

## Success criteria
- Names one spot with a real drive time and a real sense of the water.
- Says where to park and what to bring, towel, shoes, cash for the gate.
- Offers one backup that is easier to reach on a short evening.

## Failure behavior
- If a source will not load, skip it and keep going.
- If a spot is closed or the water is posted as unsafe, say so in one line and
  name the next one.

## Never
- Never sign in, buy a day pass or reserve a spot.
- Never invent a water temperature, a quality reading or an opening time.
- Never pass a sponsored listing off as a real recommendation.

## Redaction
Omit query strings, account details, order history, saved cards, home address,
and anything shown after a page unexpectedly asks for a login.
