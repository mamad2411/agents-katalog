---
name: party-plan
skill_id: browser-skill:party-plan
description: One party plan, start to finish, with a timeline and a shopping list
when_to_use:
  - intent_keywords: [party, throw a party, house party, hosting, celebration, get together]
    require_auth: false
    mutation_boundary: read_only
steps:
  - caption: party venues, bars with private areas and spaces to hire in
    capability_target: web_search
    mutation_boundary: read_only
  - caption: how much drink and food to buy for a party of this size
    capability_target: web_search
    mutation_boundary: read_only
  - caption: party timeline and what to do the week before
    capability_target: web_search
    mutation_boundary: read_only
parameters:
  - name: party
    current_value: house party for 25 people in Los Angeles
    fill_rule: say your city and Luke uses it instead
adapter_preferences:
  preferred: browserbase
  fallback: owned_browser
  declined: []
schema_version: 1
metadata:
  luke:
    tags: [party, hosting, planning, events, local]
    related_skills: [browser-skill:birthday-plan, browser-skill:dinner-party]
platforms: [macos]
---
# Party plan

## Purpose
You have decided to throw something. This makes the venue call, sets the
timeline, and hands you the list, so the only thing left is sending the invite.

## Reads
- Search results for party venues, bars with private areas and spaces to hire in house party for 25 people in Los Angeles.
- Search results for how much drink and food to buy for a party of this size house party for 25 people in Los Angeles.
- Search results for party timeline and what to do the week before house party for 25 people in Los Angeles.

## Lands in
- Commits to one plan, home or venue, and does not hand back a choice to make. Short enough to act on straight away.

## Steps
1. Look up party venues, bars with private areas and spaces to hire in house party for 25 people in Los Angeles.
2. Look up how much drink and food to buy for a party of this size house party for 25 people in Los Angeles.
3. Look up party timeline and what to do the week before house party for 25 people in Los Angeles.
4. Commits to one plan, home or venue, and does not hand back a choice to make.

## Success criteria
- Commits to one plan, home or venue, and does not hand back a choice to make.
- Gives the night an order and times, so it survives contact with real life.
- Names the first thing to do right now, and says what can wait until the day.
- Says what to buy, in what quantity, with a rough total.
- Accounts for the thing that actually breaks a party: not enough ice, one
  bathroom, or a venue with a hard closing time.

## Failure behavior
- If a venue page will not load, skip it and keep going.
- If nothing suitable is bookable, plan it at home and say why.

## Never
- Never sign in to a booking or ticketing account.
- Never book, hire, reserve, buy or pay a deposit.
- Never invent a price, a venue, a capacity or a hire fee.

## Redaction
Omit query strings, account details, order history, saved cards, home address,
and anything shown after a page unexpectedly asks for a login.
