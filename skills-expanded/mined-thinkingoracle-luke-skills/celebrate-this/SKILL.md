---
name: celebrate-this
skill_id: browser-skill:celebrate-this
description: Something good happened. Here is how you mark it tonight
when_to_use:
  - intent_keywords: [celebrate, promotion, good news, cheers, milestone, toast]
    require_auth: false
    mutation_boundary: read_only
steps:
  - caption: best places to celebrate something tonight in
    capability_target: web_search
    mutation_boundary: read_only
  - caption: where people go for good news and big nights in
    capability_target: web_search
    mutation_boundary: read_only
parameters:
  - name: occasion
    current_value: best places to celebrate in Los Angeles
    fill_rule: say your city and Luke uses it instead
adapter_preferences:
  preferred: browserbase
  fallback: owned_browser
  declined: []
schema_version: 1
metadata:
  luke:
    tags: [celebration, milestones, nights out, joy]
    related_skills: []
platforms: [macos]
---
# Celebrate this

## Purpose
Something good happened and it deserves more than a text. Where to go tonight, who to call, and what to order first.

## Reads
- Search results for best places to celebrate something tonight in best places to celebrate in Los Angeles.
- Search results for where people go for good news and big nights in best places to celebrate in Los Angeles.

## Lands in
- One place, bookable or walk-in, and says which. Short enough to act on straight away.

## Steps
1. Look up best places to celebrate something tonight in best places to celebrate in Los Angeles.
2. Look up where people go for good news and big nights in best places to celebrate in Los Angeles.
3. One place, bookable or walk-in, and says which.

## Success criteria
- One place, bookable or walk-in, and says which.
- Names the first drink or dish to order so nobody dithers.
- Scales to the news: a raise is not a wedding.
- Says how many people it works for.

## Failure behavior
- If a source will not load, skip it and keep going.
- If nothing is on, say so in one line and give the best fallback.

## Never
- Never sign in, book, buy tickets or reserve anything.
- Never invent a venue, a time, a price or a lineup.
- Never pass a promoted listing off as what people rate.

## Redaction
Omit query strings, account details, order history, saved cards, home address,
and anything shown after a page unexpectedly asks for a login.
