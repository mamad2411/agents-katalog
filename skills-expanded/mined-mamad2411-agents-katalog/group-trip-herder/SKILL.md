---
name: group-trip-herder
skill_id: browser-skill:group-trip-herder
description: The trip six people will actually agree to, with the dates already picked
when_to_use:
  - intent_keywords: [group trip, everyone, friends trip, group booking, big group, agree on dates]
    require_auth: false
    mutation_boundary: read_only
steps:
  - caption: destinations that work for a group of six on different budgets
    capability_target: web_search
    mutation_boundary: read_only
  - caption: houses and apartments that sleep six and what they cost per night
    capability_target: web_search
    mutation_boundary: read_only
  - caption: how to split costs and deposits on a group trip
    capability_target: web_search
    mutation_boundary: read_only
parameters:
  - name: group
    current_value: six people, long weekend, mixed budgets
    fill_rule: say how many people, when you are free, and the tightest budget
adapter_preferences:
  preferred: browserbase
  fallback: owned_browser
  declined: []
schema_version: 1
metadata:
  luke:
    tags: [group trip, travel, friends, planning, budget]
    related_skills: [browser-skill:trip-plan, browser-skill:festival-kit]
platforms: [macos]
---
# Group trip herder

## Purpose
Six people, one chat, no decision. This picks the trip that survives everyone's
constraints, prices it per person, and gives you the message to send.

## Reads
- Search results for destinations that work for a group of six on different budgets six people, long weekend, mixed budgets.
- Search results for houses and apartments that sleep six and what they cost per night six people, long weekend, mixed budgets.
- Search results for how to split costs and deposits on a group trip six people, long weekend, mixed budgets.

## Lands in
- Commits to one destination and one set of dates. Short enough to act on straight away.

## Steps
1. Look up destinations that work for a group of six on different budgets six people, long weekend, mixed budgets.
2. Look up houses and apartments that sleep six and what they cost per night six people, long weekend, mixed budgets.
3. Look up how to split costs and deposits on a group trip six people, long weekend, mixed budgets.
4. Commits to one destination and one set of dates. The group votes yes or no, not between four options.

## Success criteria
- Commits to one destination and one set of dates. The group votes yes or no,
  not between four options.
- Gives an order and dates: hold the house first, flights after, everything
  else later.
- Names the first thing to do right now, usually one person paying a deposit,
  and what can wait.
- States a per person cost so nobody has to do the math in the chat.
- Accounts for the constraint that actually breaks group trips: the person on
  the tightest budget, or the flight that only works from one city.

## Failure behavior
- If a listing will not load, skip it and price a comparable one.
- If no date works for everyone, say who it does not work for and plan for the
  group that can go.

## Never
- Never sign in to a booking or payments account.
- Never book, reserve, hold or pay a deposit.
- Never invent a nightly rate, a property, or a fare.

## Redaction
Omit query strings, account details, booking references, saved cards, other
people's contact details, home address, and anything shown after a page
unexpectedly asks for a login.
