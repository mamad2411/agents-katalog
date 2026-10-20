---
name: karaoke-and-late-nights
skill_id: browser-skill:karaoke-and-late-nights
description: Where the night keeps going, karaoke, late food and dancing
when_to_use:
  - intent_keywords: [karaoke, late night, dancing, after hours, late food, club, keep going]
    require_auth: false
    mutation_boundary: read_only
steps:
  - caption: best karaoke bars, dancing and late night food
    capability_target: web_search
    mutation_boundary: read_only
  - caption: where the night keeps going after midnight
    capability_target: web_search
    mutation_boundary: read_only
trigger:
  kind: schedule
  recurrence: weekly
  weekday: 7
  time: 20:00
  timezone: America/Los_Angeles
  follows_device: true
parameters:
  - name: night
    current_value: in Los Angeles
    fill_rule: say your city and Luke uses it instead
adapter_preferences:
  preferred: browserbase
  fallback: owned_browser
  declined: []
schema_version: 1
metadata:
  luke:
    tags: [karaoke, late night, dancing, nightlife, weekend]
    related_skills: [browser-skill:dance-floor]
platforms: [macos]
---
# Karaoke and late nights

## Purpose
Saturday, nine at night, the good part just starting. Where the night keeps
going near you, from the first song to the last plate of food.

## Reads
- Search results for best karaoke bars, dancing and late night food in Los Angeles.
- Search results for where the night keeps going after midnight in Los Angeles.

## Lands in
- Names closing time or last call, so the plan survives past midnight. Short enough to act on straight away.

## Steps
1. Look up best karaoke bars, dancing and late night food in Los Angeles.
2. Look up where the night keeps going after midnight in Los Angeles.
3. Names closing time or last call, so the plan survives past midnight.

## Success criteria
- Names closing time or last call, so the plan survives past midnight.
- Pairs one music or dancing spot with one food stop nearby.
- Says which one is the good one if the user only picks a single stop.

## Failure behavior
- If a listing will not load, skip it and keep going.
- If the city is quiet, name the one place that reliably stays open late.

## Never
- Never sign in, reserve a table, or buy tickets.
- Never invent a venue, a closing time, or a cover charge.
- Never pass a sponsored listing off as a real recommendation.

## Redaction
Omit query strings, account details, order history, saved cards, home address,
and anything shown after a page unexpectedly asks for a login.
