---
name: picnic-plan
skill_id: browser-skill:picnic-plan
description: The spot, the food, and what time the light gets good
when_to_use:
  - intent_keywords: [picnic, park, outside, blanket, wine, golden hour, hang out]
    require_auth: false
    mutation_boundary: read_only
steps:
  - caption: best picnic spots, parks and green space with a view near
    capability_target: web_search
    mutation_boundary: read_only
  - caption: what to bring and where to buy it for a picnic in
    capability_target: web_search
    mutation_boundary: read_only
trigger:
  kind: schedule
  recurrence: weekly
  weekday: 6
  time: 12:30
  timezone: America/Los_Angeles
  follows_device: true
parameters:
  - name: area
    current_value: best picnic spots and parks in Los Angeles
    fill_rule: say your city and Luke uses it instead
adapter_preferences:
  preferred: browserbase
  fallback: owned_browser
  declined: []
schema_version: 1
metadata:
  luke:
    tags: [picnic, parks, outdoors, summer, friends]
    related_skills: []
platforms: [macos]
---
# Picnic plan

## Purpose
A spot with good light, food you can carry, and the hour to be there. The lowest effort way to have the best afternoon of the week.

## Reads
- Search results for best picnic spots, parks and green space with a view near best picnic spots and parks in Los Angeles.
- Search results for what to bring and where to buy it for a picnic in best picnic spots and parks in Los Angeles.

## Lands in
- One spot, with what time the light gets good there. Short enough to act on straight away.

## Steps
1. Look up best picnic spots, parks and green space with a view near best picnic spots and parks in Los Angeles.
2. Look up what to bring and where to buy it for a picnic in best picnic spots and parks in Los Angeles.
3. One spot, with what time the light gets good there.

## Success criteria
- One spot, with what time the light gets good there.
- A food list you can buy in one stop, with where.
- Says the practical thing: shade, toilets, whether alcohol is fine.
- Scales to the number of people asked about.

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
