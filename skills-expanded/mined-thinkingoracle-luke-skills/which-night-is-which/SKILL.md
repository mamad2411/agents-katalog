---
name: which-night-is-which
skill_id: browser-skill:which-night-is-which
description: The weekly rhythm near you: who does what on which night
when_to_use:
  - intent_keywords: [ladies night, industry night, weekly, which night, regular, midweek]
    require_auth: false
    mutation_boundary: read_only
steps:
  - caption: recurring weekly club nights, bar specials and themed nights in
    capability_target: web_search
    mutation_boundary: read_only
  - caption: which weeknights are actually busy and worth going out in
    capability_target: web_search
    mutation_boundary: read_only
trigger:
  kind: schedule
  recurrence: weekly
  weekday: 2
  time: 12:30
  timezone: America/Los_Angeles
  follows_device: true
parameters:
  - name: area
    current_value: Los Angeles
    fill_rule: say your city
adapter_preferences:
  preferred: browserbase
  fallback: owned_browser
  declined: []
schema_version: 1
metadata:
  luke:
    tags: [nightlife, weekly, deals, midweek, local]
    related_skills: [browser-skill:party-hard]
platforms: [macos]
---
# Which night is which

## Purpose
Monday, the map of your week: which bar does what on which night, which midweek nights are actually busy, and where the deals land. So a Tuesday can be a night out too.

## Reads
- Search results for recurring weekly club nights, bar specials and themed nights in Los Angeles.
- Search results for which weeknights are actually busy and worth going out in Los Angeles.

## Lands in
- Lays out the week by night, not as one list. Short enough to act on straight away.

## Steps
1. Look up recurring weekly club nights, bar specials and themed nights in Los Angeles.
2. Look up which weeknights are actually busy and worth going out in Los Angeles.
3. Lays out the week by night, not as one list.

## Success criteria
- Lays out the week by night, not as one list.
- Says which midweek nights are genuinely busy and which are dead.
- Names the recurring deal and which night it runs.
- Flags anything that needs a guest list and by when.

## Failure behavior
- If a listing will not load, skip it and keep going.
- If there is genuinely nothing on, say so in one line and name the reliable
  fallback nearby.

## Never
- Never sign in, book, buy tickets or join a guest list.
- Never invent a price, a deal, a venue or a closing time.
- Never pass a promoted listing off as what people rate.

## Redaction
Omit query strings, account details, order history, saved cards, home address,
and anything shown after a page unexpectedly asks for a login.
