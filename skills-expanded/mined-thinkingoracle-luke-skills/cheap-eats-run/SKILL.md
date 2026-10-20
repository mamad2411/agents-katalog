---
name: cheap-eats-run
skill_id: browser-skill:cheap-eats-run
description: Genuinely great food for under twenty five dollars near you
when_to_use:
  - intent_keywords: [cheap eats, budget food, under 20, food hall, night market, good value]
    require_auth: false
    mutation_boundary: read_only
steps:
  - caption: best cheap eats and great value restaurants right now in
    capability_target: web_search
    mutation_boundary: read_only
  - caption: food hall stalls and night market dates coming up in
    capability_target: web_search
    mutation_boundary: read_only
trigger:
  kind: schedule
  recurrence: weekly
  weekday: 7
  time: 12:30
  timezone: America/Los_Angeles
  follows_device: true
parameters:
  - name: budget
    current_value: best cheap eats in Los Angeles under 25 dollars
    fill_rule: say your city and Luke uses it instead
adapter_preferences:
  preferred: browserbase
  fallback: owned_browser
  declined: []
schema_version: 1
metadata:
  luke:
    tags: [cheap eats, value, food hall, night market, lunch]
    related_skills: [browser-skill:good-food-near-you, browser-skill:happy-hour]
platforms: [macos]
---
# Cheap eats run

## Purpose
Saturday, where to eat brilliantly this week without it being a thing. Cheap
does not mean settling, and the best value food in any city is documented, it
just is not where the expensive places are listed.

## Reads
- Search results for best cheap eats and great value restaurants right now in best cheap eats in Los Angeles under 25 dollars.
- Search results for food hall stalls and night market dates coming up in best cheap eats in Los Angeles under 25 dollars.

## Lands in
- Uses the value awards, not the star lists. Short enough to act on straight away.

## Steps
1. Look up best cheap eats and great value restaurants right now in best cheap eats in Los Angeles under 25 dollars.
2. Look up food hall stalls and night market dates coming up in best cheap eats in Los Angeles under 25 dollars.
3. Uses the value awards, not the star lists. The affordable tier of the major restaurant guide is a real, inspected, published list in most big US cities and it is where the good cheap food actually is. Star lists are the wrong tool for this question.

## Success criteria
- Uses the value awards, not the star lists. The affordable tier of the major
  restaurant guide is a real, inspected, published list in most big US cities
  and it is where the good cheap food actually is. Star lists are the wrong tool
  for this question.
- Knows lunch is the loophole. The same kitchen often runs a set lunch at
  roughly half its dinner price, and at a lot of hard to book rooms lunch is the
  only version you can walk into.
- Treats food halls as the incubator they are. Stalls are where new cooks test a
  concept before they can afford a lease, rents are low, so the food punches far
  above the price. Name the stall, not the hall.
- Gives night markets an actual date and a cutoff. Most run only a handful of
  weekends a season, and the gates close well before the posted end time, so the
  last orders hour is the number that matters.
- Names a dish and a price for each pick, because "good and cheap" without a
  plate is not a recommendation.

## Failure behavior
- If a menu page will not load, use the most recent published menu and say the
  price may have moved.
- If a market has no dates announced yet, say so and give a standing option
  instead.

## Never
- Never sign in, order food, buy a ticket or pay a cover.
- Never invent a price, a dish, a stall, a market date or an award.
- Never pass a paid placement off as a value recommendation.

## Redaction
Omit query strings, account details, order history, saved cards, home address,
and anything shown after a page unexpectedly asks for a login.
