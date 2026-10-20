---
name: festival-kit
skill_id: browser-skill:festival-kit
description: What to bring, what to book, and the thing everyone forgets
when_to_use:
  - intent_keywords: [festival, camping, packing list, what to bring, glastonbury, coachella, weekender]
    require_auth: false
    mutation_boundary: read_only
steps:
  - caption: festival packing list and what people wish they had brought
    capability_target: web_search
    mutation_boundary: read_only
  - caption: festival travel, parking and campsite opening times
    capability_target: web_search
    mutation_boundary: read_only
  - caption: what is banned at festivals and what you can take in
    capability_target: web_search
    mutation_boundary: read_only
parameters:
  - name: festival
    current_value: a three day camping festival this summer
    fill_rule: say which festival, the dates, and whether you are camping
adapter_preferences:
  preferred: browserbase
  fallback: owned_browser
  declined: []
schema_version: 1
metadata:
  luke:
    tags: [festival, camping, packing, music, travel]
    related_skills: [browser-skill:group-trip-herder, browser-skill:trip-plan]
platforms: [macos]
---
# Festival kit

## Purpose
You are going. This sorts what to book now, what to buy this week, and the
things people only realize they needed once they are standing in a field.

## Reads
- Search results for festival packing list and what people wish they had brought a three day camping festival this summer.
- Search results for festival travel, parking and campsite opening times a three day camping festival this summer.
- Search results for what is banned at festivals and what you can take in a three day camping festival this summer.

## Lands in
- Commits to one list, not a set of options to weigh up. Short enough to act on straight away.

## Steps
1. Look up festival packing list and what people wish they had brought a three day camping festival this summer.
2. Look up festival travel, parking and campsite opening times a three day camping festival this summer.
3. Look up what is banned at festivals and what you can take in a three day camping festival this summer.
4. Commits to one list, not a set of options to weigh up.

## Success criteria
- Commits to one list, not a set of options to weigh up.
- Puts the list in order with times: book, buy, then pack the night before.
- Names the first thing to do right now, usually travel or parking, and what
  can wait until the week of.
- Says what to buy and roughly what it costs, including the cheap items people
  end up paying triple for on site.
- Accounts for the constraint that actually breaks festivals: campsite opening
  times, the walk from the car park, and the banned item you packed anyway.

## Failure behavior
- If the festival's own pages will not load, use published guidance and say it
  is unconfirmed.
- If the rules are not posted yet, say so and flag what usually changes.

## Never
- Never sign in to a ticket, travel or shopping account.
- Never buy tickets, book parking or order anything.
- Never invent a rule, a price, a campsite time or a travel option.

## Redaction
Omit query strings, account details, ticket orders and barcodes, saved cards,
home address, and anything shown after a page unexpectedly asks for a login.
