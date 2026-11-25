---
name: big-night-out
skill_id: browser-skill:big-night-out
description: Three or four places, in the right order, with the travel time worked out
when_to_use:
  - intent_keywords: [big night out, bar crawl, night out, drinks then, where to go after, all night]
    require_auth: false
    mutation_boundary: read_only
steps:
  - caption: best bars and late night spots in
    capability_target: web_search
    mutation_boundary: read_only
  - caption: closing times and last entry for late bars and clubs in
    capability_target: web_search
    mutation_boundary: read_only
  - caption: which neighborhoods to stay in for a night out, and travel time between them
    capability_target: web_search
    mutation_boundary: read_only
parameters:
  - name: night
    current_value: Los Angeles
    fill_rule: say your city and Luke uses it instead
adapter_preferences:
  preferred: browserbase
  fallback: owned_browser
  declined: []
schema_version: 1
metadata:
  luke:
    tags: [night out, bars, nightlife, local, planning]
    related_skills: [browser-skill:party-plan]
platforms: [macos]
---
# Big night out

## Purpose
One night, several places, in an order that works. Start somewhere you can eat,
end somewhere still open, and never spend the night walking between them.

## Reads
- Search results for best bars and late night spots in Los Angeles.
- Search results for closing times and last entry for late bars and clubs in Los Angeles.
- Search results for which neighborhoods to stay in for a night out, and travel time between them Los Angeles.

## Lands in
- Commits to one route, not a list of good bars to pick from. Short enough to act on straight away.

## Steps
1. Look up best bars and late night spots in Los Angeles.
2. Look up closing times and last entry for late bars and clubs in Los Angeles.
3. Look up which neighborhoods to stay in for a night out, and travel time between them Los Angeles.
4. Commits to one route, not a list of good bars to pick from.

## Success criteria
- Commits to one route, not a list of good bars to pick from.
- Gives every stop a time and an order, so the night survives contact with
  real life.
- Names the first thing to do right now, usually the early table, and what can
  be left to the night itself.
- Says roughly what the night costs a head, entry included.
- Accounts for the constraint that actually breaks nights out: last entry, the
  kitchen closing, or twenty five minutes across town at eleven.

## Failure behavior
- If a venue page will not load, skip it and keep the route intact.
- If the last stop has a door policy or a guest list, say so and name the
  fallback that does not.

## Never
- Never sign in, join a guest list or a waitlist.
- Never book, reserve or buy tickets.
- Never invent an opening time, a venue, a cover charge or a door policy.

## Redaction
Omit query strings, account details, ticket orders, saved cards, home address,
and anything shown after a page unexpectedly asks for a login.
