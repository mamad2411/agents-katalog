---
name: happy-hour
skill_id: browser-skill:happy-hour
description: Cheap drinks and free food near you, and how long you have
when_to_use:
  - intent_keywords: [happy hour, cheap drinks, deals, free food, discount, after work]
    require_auth: false
    mutation_boundary: read_only
steps:
  - caption: happy hour deals and cheap drink specials on right now in
    capability_target: web_search
    mutation_boundary: read_only
  - caption: which bars have the best happy hour and free bar snacks in
    capability_target: web_search
    mutation_boundary: read_only
trigger:
  kind: schedule
  recurrence: daily
  time: 17:15
  timezone: America/Los_Angeles
  follows_device: true
parameters:
  - name: area
    current_value: happy hour deals in Los Angeles
    fill_rule: say your city and Luke uses it instead
adapter_preferences:
  preferred: browserbase
  fallback: owned_browser
  declined: []
schema_version: 1
metadata:
  luke:
    tags: [happy hour, deals, drinks, cheap, after work]
    related_skills: [browser-skill:party-hard]
platforms: [macos]
---
# Happy hour

## Purpose
Late afternoon, what is cheap near you right now and exactly how long the deal runs, so you get there before it ends.

## Reads
- Search results for happy hour deals and cheap drink specials on right now in happy hour deals in Los Angeles.
- Search results for which bars have the best happy hour and free bar snacks in happy hour deals in Los Angeles.

## Lands in
- One place, the deal, and the time it ends. Short enough to act on straight away.

## Steps
1. Look up happy hour deals and cheap drink specials on right now in happy hour deals in Los Angeles.
2. Look up which bars have the best happy hour and free bar snacks in happy hour deals in Los Angeles.
3. One place, the deal, and the time it ends. The cutoff is the whole point.

## Success criteria
- One place, the deal, and the time it ends. The cutoff is the whole point.
- Says how far it is, so the walk is worth it.
- Names what is actually free versus discounted.
- One backup nearby if the first is packed.

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
