---
name: house-guests
skill_id: browser-skill:house-guests
description: People are staying: what to sort before they land, and what to do with them
when_to_use:
  - intent_keywords: [house guests, staying with us, visitors, family visiting, guest room, they are coming to stay]
    require_auth: false
    mutation_boundary: read_only
steps:
  - caption: best things to do with visitors over a weekend in
    capability_target: web_search
    mutation_boundary: read_only
  - caption: what to have in the house before guests arrive
    capability_target: web_search
    mutation_boundary: read_only
parameters:
  - name: visit
    current_value: two people staying for a long weekend in Los Angeles
    fill_rule: say your city and Luke uses it instead
adapter_preferences:
  preferred: browserbase
  fallback: owned_browser
  declined: []
schema_version: 1
metadata:
  luke:
    tags: [guests, hosting, visitors, weekend, local]
    related_skills: [browser-skill:dinner-party, browser-skill:big-night-out]
platforms: [macos]
---
# House guests

## Purpose
People are staying with you. This sorts the house before they land and gives
the visit a shape, so you are not deciding what to do over breakfast every day.

## Reads
- Search results for best things to do with visitors over a weekend in two people staying for a long weekend in Los Angeles.
- Search results for what to have in the house before guests arrive two people staying for a long weekend in Los Angeles.

## Lands in
- Commits to one plan for the visit, not a menu of local attractions. Short enough to act on straight away.

## Steps
1. Look up best things to do with visitors over a weekend in two people staying for a long weekend in Los Angeles.
2. Look up what to have in the house before guests arrive two people staying for a long weekend in Los Angeles.
3. Commits to one plan for the visit, not a menu of local attractions.

## Success criteria
- Commits to one plan for the visit, not a menu of local attractions.
- Gives each day an order and times, built around what is open when.
- Names the first thing to do right now, usually the grocery run or the spare
  bedding, and what can wait until the morning they arrive.
- Says what to buy for the house, with a rough total.
- Accounts for the constraint that actually breaks visits: the thing that shuts
  on Mondays, the journey from the airport, and leaving people one free day.

## Failure behavior
- If a listing will not load, skip it and keep going.
- If a place is closed for their dates, say so and put something else in the
  slot.

## Never
- Never sign in to a grocery, delivery or booking account.
- Never order groceries, book a table or buy anything.
- Never invent an opening time, a price or a place.

## Redaction
Omit query strings, account details, order history, saved cards, other people's
travel details, home address, and anything shown after a page unexpectedly asks
for a login.
