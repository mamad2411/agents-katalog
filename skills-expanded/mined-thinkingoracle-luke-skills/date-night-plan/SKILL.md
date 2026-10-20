---
name: date-night-plan
skill_id: browser-skill:date-night-plan
description: One good plan, sorted before you have to ask
when_to_use:
  - intent_keywords: [date, date night, plans, romantic, dinner, evening]
    require_auth: false
    mutation_boundary: read_only
steps:
  - caption: best places and things on this week for an evening out
    capability_target: web_search
    mutation_boundary: read_only
  - caption: which spots people are recommending right now for a night out
    capability_target: web_search
    mutation_boundary: read_only
trigger:
  kind: schedule
  recurrence: weekly
  weekday: 4
  time: 17:15
  timezone: America/Los_Angeles
  follows_device: true
parameters:
  - name: city_and_vibe
    current_value: in Los Angeles
    fill_rule: say your city and Luke uses it instead
adapter_preferences:
  preferred: browserbase
  fallback: owned_browser
  declined: []
schema_version: 1
metadata:
  luke:
    tags: [dating, date night, restaurants, events, local]
    related_skills: []
platforms: [macos]
---
# Date night plan

## Purpose
Wednesday lunchtime, one plan good enough to just send. Place, time, and a backup, ready to go.

## Reads
- Search results for best places and things on this week for an evening out in Los Angeles.
- Search results for which spots people are recommending right now for a night out in Los Angeles.

## Lands in
- Gives one plan, start to finish, with places and times. Short enough to act on straight away.

## Steps
1. Look up best places and things on this week for an evening out in Los Angeles.
2. Look up which spots people are recommending right now for a night out in Los Angeles.
3. Gives one plan, start to finish, with places and times.

## Success criteria
- Gives one plan, start to finish, with places and times.
- Offers one backup, no more.
- Keeps it to the vibe the user asked for.

## Failure behavior
- If a source will not load, skip it and keep going.
- If there is genuinely nothing, say so in one line and move on.

## Never
- Never sign in, buy, book, reserve or join a waitlist.
- Never invent a price, a date, a venue or a review.
- Never pass an ad off as a recommendation.

## Redaction
Omit query strings, account details, order history, saved cards, home address,
and anything shown after a page unexpectedly asks for a login.
