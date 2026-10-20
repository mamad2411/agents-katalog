---
name: where-to-sleep
skill_id: browser-skill:where-to-sleep
description: Dorm, private room, cheap hotel or a sleeper berth, priced honestly
when_to_use:
  - intent_keywords: [hostel, where to stay, accommodation, cheap hotel, dorm, airbnb, place to stay]
    require_auth: false
    mutation_boundary: read_only
steps:
  - caption: current nightly rates for hostels, private rooms and budget hotels in
    capability_target: web_search
    mutation_boundary: read_only
  - caption: what recent guests actually say about the best places to stay in
    capability_target: web_search
    mutation_boundary: read_only
parameters:
  - name: city
    current_value: hostel and budget hotel prices in Lisbon
    fill_rule: say the city, the nights, and whether you want to meet people or sleep
adapter_preferences:
  preferred: browserbase
  fallback: owned_browser
  declined: []
schema_version: 1
metadata:
  luke:
    tags: [travel, hostels, hotels, budget, accommodation]
    related_skills: [browser-skill:trip-plan, browser-skill:shoulder-season]
platforms: [macos]
---
# Where to sleep

## Purpose
The bed that is actually right for this city and these nights. Sometimes the
hostel, often not, and occasionally a train that removes the question.

## Reads
- Search results for current nightly rates for hostels, private rooms and budget hotels in hostel and budget hotel prices in Lisbon.
- Search results for what recent guests actually say about the best places to stay in hostel and budget hotel prices in Lisbon.

## Lands in
- Checks whether the hostel is still the cheap option, because in some cities it stopped being one. Short enough to act on straight away.

## Steps
1. Look up current nightly rates for hostels, private rooms and budget hotels in hostel and budget hotel prices in Lisbon.
2. Look up what recent guests actually say about the best places to stay in hostel and budget hotel prices in Lisbon.
3. Checks whether the hostel is still the cheap option, because in some cities it stopped being one. Amsterdam hostel rates rose around 65 percent between 2023 and 2026, and some Paris hostels now average 180 euros a night, level with a three star hotel.

## Success criteria
- Checks whether the hostel is still the cheap option, because in some cities it
  stopped being one. Amsterdam hostel rates rose around 65 percent between 2023
  and 2026, and some Paris hostels now average 180 euros a night, level with a
  three star hotel.
- Separates the dorm from the private room, since only one of them is a big
  saving. Dorms hold the gap at roughly 15 to 30 euros against 80 to 150 for a
  budget hotel, while a private hostel room saves about 20 to 40 percent.
- Counts the city tax as part of the rate, because it is now real money.
  Barcelona's surcharge went to 5 euros a night in January 2026 on top of the
  existing tax, and Amsterdam's effective load is around 33.5 percent after the
  national VAT on accommodation rose from 9 to 21 percent.
- Counts an overnight train as a bed when the route has one. A sleeper berth
  removes a hotel night and a travel day at the same time, and Europe now runs
  more than forty night routes, with Paris to Berlin back since March 2026.
- Says which one to take and why, in terms of what the trip is for. A social
  hostel and a quiet private room are not interchangeable and the reviews say
  which one a place really is.
- Names the neighborhood, not just the property, and says what is a walk away.

## Failure behavior
- If a rate page will not load, give the published range and say it is
  approximate for those dates.
- If the city has genuinely no good budget option on those nights, say that and
  name the nearest one that works.

## Never
- Never sign in to a booking, hostel or hotel account.
- Never book, reserve, hold or buy anything.
- Never invent a rate, a tax, a property or a review.

## Redaction
Omit query strings, account details, booking references, saved cards, passport
and loyalty numbers, home address, and anything shown after a page unexpectedly
asks for a login.
