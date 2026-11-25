---
name: city-secret
skill_id: browser-skill:city-secret
description: The thing in your own city you have somehow never done
when_to_use:
  - intent_keywords: [hidden gem, local, my city, never done, explore, tourist in your own town]
    require_auth: false
    mutation_boundary: read_only
steps:
  - caption: overlooked places locals recommend and visitors never find in
    capability_target: web_search
    mutation_boundary: read_only
  - caption: opening hours, entry cost and how to get in at lesser known spots in
    capability_target: web_search
    mutation_boundary: read_only
trigger:
  kind: schedule
  recurrence: weekly
  weekday: 3
  time: 20:00
  timezone: America/Los_Angeles
  follows_device: true
parameters:
  - name: city
    current_value: Los Angeles
    fill_rule: say your city and Luke uses it instead
adapter_preferences:
  preferred: browserbase
  fallback: owned_browser
  declined: []
schema_version: 1
metadata:
  luke:
    tags: [local, hidden gems, explore, city, weekly]
    related_skills: []
platforms: [macos]
---
# City secret

## Purpose
Tuesday night, planning the next few days. One thing in the user's own city they
have walked past a hundred times and never actually gone into.

## Reads
- Search results for overlooked places locals recommend and visitors never find in Los Angeles.
- Search results for opening hours, entry cost and how to get in at lesser known spots in Los Angeles.

## Lands in
- Names one specific place with a neighborhood and real opening hours. Short enough to act on straight away.

## Steps
1. Look up overlooked places locals recommend and visitors never find in Los Angeles.
2. Look up opening hours, entry cost and how to get in at lesser known spots in Los Angeles.
3. Names one specific place with a neighborhood and real opening hours.

## Success criteria
- Names one specific place with a neighborhood and real opening hours.
- Says what it costs, including when it is free.
- Gives the best time to go, and one line on why that hour.

## Failure behavior
- If a source will not load, skip it and keep going.
- If the place is closed this week, say so in one line and name the next one.

## Never
- Never sign in, buy tickets or reserve a slot.
- Never invent a place, an opening hour or a price.
- Never pass a sponsored listing off as a local recommendation.

## Redaction
Omit query strings, account details, order history, saved cards, home address,
and anything shown after a page unexpectedly asks for a login.
