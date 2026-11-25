---
name: table-tonight
skill_id: browser-skill:table-tonight
description: A table tonight at a place that says it is fully booked
when_to_use:
  - intent_keywords: [table tonight, fully booked, cancellation, last minute reservation, get in tonight, walk in]
    require_auth: false
    mutation_boundary: read_only
steps:
  - caption: same day cancellations and last minute tables tonight in
    capability_target: web_search
    mutation_boundary: read_only
  - caption: which restaurants keep bar seats and counter seats for walk ins in
    capability_target: web_search
    mutation_boundary: read_only
parameters:
  - name: tonight
    current_value: Los Angeles
    fill_rule: say your city
adapter_preferences:
  preferred: browserbase
  fallback: owned_browser
  declined: []
schema_version: 1
metadata:
  luke:
    tags: [restaurants, reservations, walk in, last minute, dinner]
    related_skills: [browser-skill:good-food-near-you, browser-skill:date-night-plan]
platforms: [macos]
---
# Table tonight

## Purpose
"Fully booked" is almost never true at 5pm. Cancellations come in waves and
most good rooms hold seats that the app has never listed. This finds you a
table for tonight anyway.

## Reads
- Search results for same day cancellations and last minute tables tonight in Los Angeles.
- Search results for which restaurants keep bar seats and counter seats for walk ins in Los Angeles.

## Lands in
- Knows cancellations cluster, not trickle. Short enough to act on straight away.

## Steps
1. Look up same day cancellations and last minute tables tonight in Los Angeles.
2. Look up which restaurants keep bar seats and counter seats for walk ins in Los Angeles.
3. Knows cancellations cluster, not trickle. The big same day wave is roughly 2pm to 6pm as people finalize their evening, and a second one lands 24 to 48 hours out when free cancellation windows and deposit deadlines expire.

## Success criteria
- Knows cancellations cluster, not trickle. The big same day wave is roughly
  2pm to 6pm as people finalize their evening, and a second one lands 24 to 48
  hours out when free cancellation windows and deposit deadlines expire.
- Knows the bar counter is usually first come first served and often never
  appears on the reservation app at all, even at rooms that look sold out. That
  is the way in, and at many places it is the same full menu.
- Says the arrival time, not just the place. Doors opening, usually 5 to 5:30,
  is the single best walk in moment. The late second wave after 9 is the other.
- Flags the 15 to 20 minute hold: a table booked for 7 goes back to walk ins by
  about 7:20 if nobody shows.
- Names one backup within walking distance, because the whole plan is timing.

## Failure behavior
- If a listing will not load, skip it and use the next one.
- If nothing is genuinely open, say so in one line and give the walk in play
  with a time instead of a booking.

## Never
- Never sign in, book a table, join a waitlist or pay a deposit.
- Never buy, bid on, or recommend a resold reservation from a resale market.
- Never invent an opening, a wait time, a policy or a price.

## Redaction
Omit query strings, account details, order history, saved cards, home address,
and anything shown after a page unexpectedly asks for a login.
