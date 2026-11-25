---
name: cheap-thrills
skill_id: browser-skill:cheap-thrills
description: Great things near you that cost almost nothing this week
when_to_use:
  - intent_keywords: [cheap, free, broke, budget, free events, cheap night out, this week]
    require_auth: false
    mutation_boundary: read_only
steps:
  - caption: free and cheap things to do this week
    capability_target: web_search
    mutation_boundary: read_only
  - caption: best free events, cheap eats and no cover nights this week
    capability_target: web_search
    mutation_boundary: read_only
trigger:
  kind: schedule
  recurrence: weekly
  weekday: 2
  time: 08:30
  timezone: America/Los_Angeles
  follows_device: true
parameters:
  - name: budget
    current_value: in Los Angeles
    fill_rule: say your city and Luke uses it instead
adapter_preferences:
  preferred: browserbase
  fallback: owned_browser
  declined: []
schema_version: 1
metadata:
  luke:
    tags: [cheap, free, local, weekly, fun]
    related_skills: [browser-skill:out-this-weekend]
platforms: [macos]
---
# Cheap thrills

## Purpose
Monday morning, the week wide open. The best things happening near you that
cost close to nothing, so a great week never has to be an expensive one.

## Reads
- Search results for free and cheap things to do this week in Los Angeles.
- Search results for best free events, cheap eats and no cover nights this week in Los Angeles.

## Lands in
- Every pick names a price, and free means free with nothing to buy at the door. Short enough to act on straight away.

## Steps
1. Look up free and cheap things to do this week in Los Angeles.
2. Look up best free events, cheap eats and no cover nights this week in Los Angeles.
3. Every pick names a price, and free means free with nothing to buy at the door.

## Success criteria
- Every pick names a price, and free means free with nothing to buy at the door.
- Picks span different days so the week has more than one good night in it.
- Leads with the one that punches hardest above its price.

## Failure behavior
- If a listing will not load, skip it and keep going.
- If the week is thin, give the best two and say the third is worth the wait.

## Never
- Never sign in, buy tickets, or reserve anything.
- Never invent a price, a venue, or a date.
- Never pass a sponsored listing off as a real recommendation.

## Redaction
Omit query strings, account details, order history, saved cards, home address,
and anything shown after a page unexpectedly asks for a login.
