---
name: budget-airline-math
skill_id: browser-skill:budget-airline-math
description: What the cheap fare really costs once the bag, the gate and the bus are in
when_to_use:
  - intent_keywords: [ryanair, wizz air, easyjet, budget airline, cheap flight, hand luggage, baggage fees]
    require_auth: false
    mutation_boundary: read_only
steps:
  - caption: current baggage, seat and check in fees charged by
    capability_target: web_search
    mutation_boundary: read_only
  - caption: how long and how much the transfer takes from the airport used by
    capability_target: web_search
    mutation_boundary: read_only
parameters:
  - name: flight
    current_value: Ryanair cabin bag fees and Beauvais airport bus to Paris
    fill_rule: name the airline and the airport it actually lands at
adapter_preferences:
  preferred: browserbase
  fallback: owned_browser
  declined: []
schema_version: 1
metadata:
  luke:
    tags: [travel, flights, budget, fees, airports]
    related_skills: [browser-skill:trip-plan]
platforms: [macos]
---
# Budget airline math

## Purpose
The 19 euro fare against the real number. Bag, seat, gate, and the hour and a
half of bus from an airport that is not in the city it is named after.

## Reads
- Search results for current baggage, seat and check in fees charged by Ryanair cabin bag fees and Beauvais airport bus to Paris.
- Search results for how long and how much the transfer takes from the airport used by Ryanair cabin bag fees and Beauvais airport bus to Paris.

## Lands in
- Adds the bag before comparing anything, because the headline fare assumes you travel with nothing. Short enough to act on straight away.

## Steps
1. Look up current baggage, seat and check in fees charged by Ryanair cabin bag fees and Beauvais airport bus to Paris.
2. Look up how long and how much the transfer takes from the airport used by Ryanair cabin bag fees and Beauvais airport bus to Paris.
3. Adds the bag before comparing anything, because the headline fare assumes you travel with nothing. Which? checked over 600 Ryanair flights and found the advertised 12 pound cabin bag price available exactly twice.

## Success criteria
- Adds the bag before comparing anything, because the headline fare assumes you
  travel with nothing. Which? checked over 600 Ryanair flights and found the
  advertised 12 pound cabin bag price available exactly twice.
- Prices the ground leg as part of the ticket. Beauvais is sold as Paris and is
  about 80 minutes and roughly 12 to 18 euros each way from Porte Maillot. Hahn
  is close to two hours from Frankfurt.
- Warns about the gate specifically. Ryanair gate staff earn 2.50 euros for each
  oversized bag they catch, gate penalties run up to 75 euros, and checking in at
  the airport rather than online costs 55 euros.
- Notes that the boarding pass went app only in November 2025, and a reissue is
  20 euros or 20 pounds, so a dead phone is a real line item.
- Says whether booking direct matters here. A ticket bought through a third
  party sits with the agent, so the airline desk often cannot touch it when
  something goes wrong, and the 24 hour cancellation rule may not apply.
- Ends with one number against one number and a verdict, not a fee table.

## Failure behavior
- If a fee page will not load, use the last published figure and say it is
  indicative.
- If the airport transfer has no public timetable, say the journey time and that
  the fare needs checking locally.

## Never
- Never sign in to an airline, agent or transfer account.
- Never book, hold, check in for or buy anything.
- Never invent a fee, a fare or a shuttle that does not run.

## Redaction
Omit query strings, account details, booking references, boarding passes,
frequent flyer numbers, saved cards, home address, and anything shown after a
page unexpectedly asks for a login.
