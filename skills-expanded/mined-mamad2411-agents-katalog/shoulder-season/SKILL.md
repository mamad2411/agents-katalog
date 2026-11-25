---
name: shoulder-season
skill_id: browser-skill:shoulder-season
description: The weeks a place is at its best while the prices have already dropped
when_to_use:
  - intent_keywords: [best time to visit, shoulder season, when to go, off season, avoid crowds, cheapest time to travel]
    require_auth: false
    mutation_boundary: read_only
steps:
  - caption: best weeks to visit and current crowd and price levels in
    capability_target: web_search
    mutation_boundary: read_only
  - caption: sea temperature, weather and local holiday dates this season in
    capability_target: web_search
    mutation_boundary: read_only
trigger:
  kind: schedule
  recurrence: weekly
  weekday: 1
  time: 08:30
  timezone: America/Los_Angeles
  follows_device: true
parameters:
  - name: places
    current_value: best time to visit southern Italy shoulder season
    fill_rule: name the places you keep thinking about and Luke watches for the window
adapter_preferences:
  preferred: browserbase
  fallback: owned_browser
  declined: []
schema_version: 1
metadata:
  luke:
    tags: [travel, seasons, timing, weather, crowds]
    related_skills: [browser-skill:trip-ideas]
platforms: [macos]
---
# Shoulder season

## Purpose
Sunday morning, before anyone has booked anything. Which of your places is about
to hit its good weeks, and how far out you would need to move to catch it.

## Reads
- Search results for best weeks to visit and current crowd and price levels in best time to visit southern Italy shoulder season.
- Search results for sea temperature, weather and local holiday dates this season in best time to visit southern Italy shoulder season.

## Lands in
- Names weeks, not months. Short enough to act on straight away.

## Steps
1. Look up best weeks to visit and current crowd and price levels in best time to visit southern Italy shoulder season.
2. Look up sea temperature, weather and local holiday dates this season in best time to visit southern Italy shoulder season.
3. Names weeks, not months. The good part of a month and the bad part of the same month are often two different trips.

## Success criteria
- Names weeks, not months. The good part of a month and the bad part of the same
  month are often two different trips.
- Knows the southern Europe trick. The Mediterranean is at its warmest in the
  second half of September, around 25 to 27 degrees, which is after European
  schools go back and rates come down. August water at non-August prices.
- Calls out the shoulder that is a trap. Spring in the Med is cheap because the
  sea is still cold, and autumn in Southeast Asia is cheap because it is still
  raining through October.
- Knows the dates that ruin an otherwise perfect month. Japan's Golden Week runs
  April 29 to May 6 in 2026, Silver Week is September 19 to 23, and Obon fills
  mid August, all of which pack the trains and hotels with domestic travelers.
- Ties the window to the booking. Names the date by which the flight has to be
  bought for that window to still be worth going for.
- Keeps to places the user actually listed, and leads with one.

## Failure behavior
- If a source will not load, skip it and keep going. Do not report the plumbing.
- If nothing on the list is near its window, say so in one line and name the
  month to ask again.

## Never
- Never sign in to a booking, airline or hotel account.
- Never book, reserve, hold or buy anything.
- Never invent a temperature, a rate or a holiday date.

## Redaction
Omit query strings, account details, booking references, saved cards, passport
and loyalty numbers, home address, and anything shown after a page unexpectedly
asks for a login.
