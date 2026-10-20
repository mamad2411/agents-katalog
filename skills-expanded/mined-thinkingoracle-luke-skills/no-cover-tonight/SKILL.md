---
name: no-cover-tonight
skill_id: browser-skill:no-cover-tonight
description: Where the door is genuinely free, and where free is the setup
when_to_use:
  - intent_keywords: [free, no cover, cheap, broke, free entry, pay what you want, no ticket]
    require_auth: false
    mutation_boundary: read_only
steps:
  - caption: free live music, no cover nights and free entry before a set hour in
    capability_target: web_search
    mutation_boundary: read_only
  - caption: what the door actually charges and what the minimum is at
    capability_target: web_search
    mutation_boundary: read_only
parameters:
  - name: scene
    current_value: free live music and no cover nights in Los Angeles
    fill_rule: say your city and Luke uses it instead
adapter_preferences:
  preferred: browserbase
  fallback: owned_browser
  declined: []
schema_version: 1
metadata:
  luke:
    tags: [free, no cover, cheap, live music, going out]
    related_skills: [browser-skill:cheap-thrills]
platforms: [macos]
---
# No cover tonight

## Purpose
Free tonight, sorted into free that stays free and free that collects at the table. One place, with the real number the user is going to spend.

## Reads
- Search results for free live music, no cover nights and free entry before a set hour in free live music and no cover nights in Los Angeles.
- Search results for what the door actually charges and what the minimum is at free live music and no cover nights in Los Angeles.

## Lands in
- Says what replaces the cover. Short enough to act on straight away.

## Steps
1. Look up free live music, no cover nights and free entry before a set hour in free live music and no cover nights in Los Angeles.
2. Look up what the door actually charges and what the minimum is at free live music and no cover nights in Los Angeles.
3. Says what replaces the cover. A no cover room pays the band out of the bar, so the ask arrives as a drink minimum or a tip bucket, and a two item minimum at a comedy club often costs more than a ticket would have.

## Success criteria
- Says what replaces the cover. A no cover room pays the band out of the bar, so the ask arrives as a drink minimum or a tip bucket, and a two item minimum at a comedy club often costs more than a ticket would have.
- Separates a music charge from a cover. Listening rooms bill per set, the walk-up charge is frequently lower than the reserved price online, there is a one drink minimum for every set, and the late set is the cheap one.
- Uses the free windows the city already runs. Museums with free or pay what you wish Friday nights book real DJ sets, run until 9 or 10pm, and cost nothing at all.
- Catches the in-store. Record shops put on free afternoon sets by touring bands, often the same day that band plays a sold out room across town, sometimes gated behind buying the record.
- Names the arrive-by time whenever entry is free only before a stated hour, because that is the most common shape free takes.

## Failure behavior
- If a listing will not load, skip it and keep going.
- If nothing free is on, say so in one line and name the cheapest thing that is actually good.

## Never
- Never sign in, RSVP, buy anything or join a list.
- Never invent a cover price, a minimum or a set time.
- Never call something free when a minimum or a purchase is required to stay.

## Redaction
Omit query strings, account details, ticket orders, saved cards, home address,
and anything shown after a page unexpectedly asks for a login.
