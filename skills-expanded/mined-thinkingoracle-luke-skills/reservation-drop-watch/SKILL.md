---
name: reservation-drop-watch
skill_id: browser-skill:reservation-drop-watch
description: The exact minute your hard to book place releases tables
when_to_use:
  - intent_keywords: [reservation drop, booking window, release time, hard to book, resy, opentable]
    require_auth: false
    mutation_boundary: read_only
steps:
  - caption: reservation release time and booking window for restaurants in
    capability_target: web_search
    mutation_boundary: read_only
  - caption: how far in advance these restaurants open bookings and at what hour
    capability_target: web_search
    mutation_boundary: read_only
trigger:
  kind: schedule
  recurrence: weekly
  weekday: 1
  time: 12:30
  timezone: America/Los_Angeles
  follows_device: true
parameters:
  - name: wishlist
    current_value: restaurant reservation release times and booking windows
    fill_rule: say your city and the two or three places you want to get into
adapter_preferences:
  preferred: browserbase
  fallback: owned_browser
  declined: []
schema_version: 1
metadata:
  luke:
    tags: [reservations, restaurants, booking, planning, resy]
    related_skills: [browser-skill:table-tonight, browser-skill:date-night-plan]
platforms: [macos]
---
# Reservation drop watch

## Purpose
Sunday, the drop calendar for the week. Every restaurant on your list has two
numbers: the hour it releases tables and how many days ahead. Know both and you
stop losing to people who just knew.

## Reads
- Search results for reservation release time and booking window for restaurants in restaurant reservation release times and booking windows.
- Search results for how far in advance these restaurants open bookings and at what hour restaurant reservation release times and booking windows.

## Lands in
- Gives two numbers per place, the drop hour and the days out, because one without the other is useless. Short enough to act on straight away.

## Steps
1. Look up reservation release time and booking window for restaurants in restaurant reservation release times and booking windows.
2. Look up how far in advance these restaurants open bookings and at what hour restaurant reservation release times and booking windows.
3. Gives two numbers per place, the drop hour and the days out, because one without the other is useless. A 10am drop at 30 days means tables for exactly 30 days from today appear at 10:00 sharp, all at once, not gradually.

## Success criteria
- Gives two numbers per place, the drop hour and the days out, because one
  without the other is useless. A 10am drop at 30 days means tables for exactly
  30 days from today appear at 10:00 sharp, all at once, not gradually.
- Corrects the common belief that everything drops at midnight. Most rooms drop
  between 9am and 10am local time, and windows range from about 6 days to 60,
  with 14 to 30 the usual band.
- Flags collisions. In most cities several of the biggest rooms release at the
  same 10am minute, so you can realistically chase one. Say which one.
- Notes that top tables can be claimed inside 10 to 30 seconds, so the useful
  advice is have the date, party size and account ready before the hour turns.
- Says when a place is not winnable at the drop and is only a cancellation play.

## Failure behavior
- If a policy page will not load, use what regulars report and say it is
  reported rather than confirmed.
- If a place publishes no window at all, say so and treat it as walk in or
  cancellation only.

## Never
- Never sign in, book a table, join a waitlist or pay a deposit.
- Never use or recommend a bot, a scraper or a paid reservation resale market.
- Never invent a drop time, a booking window or a policy.

## Redaction
Omit query strings, account details, order history, saved cards, home address,
and anything shown after a page unexpectedly asks for a login.
