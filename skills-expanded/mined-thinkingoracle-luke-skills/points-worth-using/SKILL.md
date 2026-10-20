---
name: points-worth-using
skill_id: browser-skill:points-worth-using
description: Whether the points you already have are worth spending on this trip
when_to_use:
  - intent_keywords: [points, miles, airline miles, award flight, credit card points, redeem, loyalty]
    require_auth: false
    mutation_boundary: read_only
steps:
  - caption: current published award rates and transfer partners for
    capability_target: web_search
    mutation_boundary: read_only
  - caption: when award seats are released and how far ahead you can book with
    capability_target: web_search
    mutation_boundary: read_only
parameters:
  - name: program
    current_value: Chase Ultimate Rewards transfer partners award value
    fill_rule: say which points you have and roughly where you want to go
adapter_preferences:
  preferred: browserbase
  fallback: owned_browser
  declined: []
schema_version: 1
metadata:
  luke:
    tags: [travel, points, miles, rewards, flights]
    related_skills: [browser-skill:trip-plan]
platforms: [macos]
---
# Points worth using

## Purpose
You have a pile of points and no idea what they are worth. One answer: spend
them on this trip, or leave them alone because cash is cheaper here.

## Reads
- Search results for current published award rates and transfer partners for Chase Ultimate Rewards transfer partners award value.
- Search results for when award seats are released and how far ahead you can book with Chase Ultimate Rewards transfer partners award value.

## Lands in
- Starts from the two numbers that settle it. Short enough to act on straight away.

## Steps
1. Look up current published award rates and transfer partners for Chase Ultimate Rewards transfer partners award value.
2. Look up when award seats are released and how far ahead you can book with Chase Ultimate Rewards transfer partners award value.
3. Starts from the two numbers that settle it. Chase points cash out at one cent each, and the same point moved to Hyatt lands around 1.8 to 2.3 cents on rooms that would cost 400 to 700 dollars, so the gap is the whole argument.

## Success criteria
- Starts from the two numbers that settle it. Chase points cash out at one cent
  each, and the same point moved to Hyatt lands around 1.8 to 2.3 cents on rooms
  that would cost 400 to 700 dollars, so the gap is the whole argument.
- Says keep the points when the redemption does not clear the cash rate. On a
  cheap short haul the fare usually beats the miles and the right move is to pay.
- Warns that a transfer is one way and cannot be reversed, so points only move
  after the specific seat or room has been found, not in hope of finding one.
- Knows when seats appear, not just what they cost. American opens partner award
  space 331 days out, and British Airways can book Japan Airlines 355 days out,
  which is 24 days of head start on the same aircraft.
- Names the single program worth putting points into for this trip, and says
  which of the others are a distraction.
- Ends with one move to make this week, and the date the seats open if that is
  what the trip is waiting on.

## Failure behavior
- If an award chart will not load, use the published rate and say it is
  indicative and dynamic pricing may differ.
- If the points balance is unknown, give the answer per ten thousand points and
  say what balance makes it work.

## Never
- Never sign in to a loyalty, bank or airline account.
- Never transfer, redeem, book or buy anything.
- Never invent a points rate, a fare or an award seat that is not shown.

## Redaction
Omit query strings, account details, loyalty and card numbers, points balances,
booking references, saved cards, home address, and anything shown after a page
unexpectedly asks for a login.
