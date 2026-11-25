---
name: art-break
skill_id: browser-skill:art-break
description: A show worth an hour, and the best time to walk in
when_to_use:
  - intent_keywords: [art, gallery, exhibition, museum, show, culture, free entry]
    require_auth: false
    mutation_boundary: read_only
steps:
  - caption: exhibitions, shows and openings on right now in
    capability_target: web_search
    mutation_boundary: read_only
  - caption: which shows people say are actually worth going to in
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
  - name: area
    current_value: Los Angeles
    fill_rule: say your city and Luke uses it instead
adapter_preferences:
  preferred: browserbase
  fallback: owned_browser
  declined: []
schema_version: 1
metadata:
  luke:
    tags: [art, galleries, exhibitions, culture, free]
    related_skills: []
platforms: [macos]
---
# Art break

## Purpose
One show worth an hour of your week, the quiet hour to see it, and whether it costs anything. Culture without the homework.

## Reads
- Search results for exhibitions, shows and openings on right now in Los Angeles.
- Search results for which shows people say are actually worth going to in Los Angeles.

## Lands in
- One show, with the hour it is quiet and what it costs. Short enough to act on straight away.

## Steps
1. Look up exhibitions, shows and openings on right now in Los Angeles.
2. Look up which shows people say are actually worth going to in Los Angeles.
3. One show, with the hour it is quiet and what it costs.

## Success criteria
- One show, with the hour it is quiet and what it costs.
- One line on why this one, in plain words, no art-speak.
- Says if it is free, and which evenings are free if any.
- Flags when it closes, so it does not get missed.

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
