---
name: restaurant-week-play
skill_id: browser-skill:restaurant-week-play
description: Which restaurant week menus are a real deal and which are not
when_to_use:
  - intent_keywords: [restaurant week, prix fixe, dine out, set menu deal, tasting deal, dining week]
    require_auth: false
    mutation_boundary: read_only
steps:
  - caption: restaurant week dates participating restaurants and menus in
    capability_target: web_search
    mutation_boundary: read_only
  - caption: which restaurant week menus are worth it and which have supplements
    capability_target: web_search
    mutation_boundary: read_only
parameters:
  - name: week
    current_value: restaurant week participating restaurants and menus
    fill_rule: say your city and roughly what you want to spend per person
adapter_preferences:
  preferred: browserbase
  fallback: owned_browser
  declined: []
schema_version: 1
metadata:
  luke:
    tags: [restaurant week, prix fixe, deals, value, dining]
    related_skills: [browser-skill:cheap-eats-run, browser-skill:reservation-drop-watch]
platforms: [macos]
---
# Restaurant week play

## Purpose
Restaurant week puts hundreds of places on one list at one price, and maybe
thirty of them are a genuine deal. This finds those, and tells you what it
really costs once the table is paid for.

## Reads
- Search results for restaurant week dates participating restaurants and menus in restaurant week participating restaurants and menus.
- Search results for which restaurant week menus are worth it and which have supplements restaurant week participating restaurants and menus.

## Lands in
- Books before the week starts. Short enough to act on straight away.

## Steps
1. Look up restaurant week dates participating restaurants and menus in restaurant week participating restaurants and menus.
2. Look up which restaurant week menus are worth it and which have supplements restaurant week participating restaurants and menus.
3. Books before the week starts. Reservations for restaurant week usually open about a week ahead of the first night, all at once, and the good rooms at the good tiers are gone within a day or two of that opening.

## Success criteria
- Books before the week starts. Reservations for restaurant week usually open
  about a week ahead of the first night, all at once, and the good rooms at the
  good tiers are gone within a day or two of that opening.
- Does the only comparison that matters: the set price against that specific
  restaurant's normal menu. A set menu is a deal only where the regular carte
  sits well above it, or where the set menu includes the dish the place is
  actually known for.
- Adds the gap out loud. The advertised price excludes tax, tip and every drink,
  so budget roughly 25 to 30 percent on top, and more if you order wine.
- Catches supplements before you book, since one upcharged course can wipe out
  the entire saving.
- Says to ask for the restaurant week menu by name at the table. Plenty of
  places hand you the regular menu by default and will not offer it otherwise.
- Points out that lunch tiers are usually the better value than dinner tiers at
  the same restaurant, and far easier to get.

## Failure behavior
- If a menu is not posted yet, say so and give the previous edition as a guide,
  clearly labeled as last time.
- If nothing on the list is a real saving, say that plainly and name one place
  worth going to at full price instead.

## Never
- Never sign in, book a table, join a waitlist or pay a deposit.
- Never invent a price, a course, a participating restaurant or a date.
- Never call something a deal without having compared it to the regular menu.

## Redaction
Omit query strings, account details, order history, saved cards, home address,
and anything shown after a page unexpectedly asks for a login.
