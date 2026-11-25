---
name: what-to-wear
skill_id: browser-skill:what-to-wear
description: An outfit for the exact thing you have on, built from what you own
when_to_use:
  - intent_keywords: [what to wear, outfit, dress code, wedding guest, date outfit, styling, fit]
    require_auth: false
    mutation_boundary: read_only
steps:
  - caption: what people are actually wearing to
    capability_target: web_search
    mutation_boundary: read_only
  - caption: the dress code, the weather and how formal it really gets at
    capability_target: web_search
    mutation_boundary: read_only
parameters:
  - name: the_occasion
    current_value: what to wear to a winter wedding
    fill_rule: say what the event is, where it is, and what is already in your closet
adapter_preferences:
  preferred: browserbase
  fallback: owned_browser
  declined: []
schema_version: 1
metadata:
  luke:
    tags: [style, outfits, events, dressing, on-demand]
    related_skills: [browser-skill:what-should-i-wear]
platforms: [macos]
---
# What to wear

## Purpose
There is a specific thing on the calendar and the closet is open. One outfit,
built from what the user already owns, calibrated to what people actually wear
to that thing in that city at that time of year.

## Reads
- Search results for what people are actually wearing to what to wear to a winter wedding.
- Search results for the dress code, the weather and how formal it really gets at what to wear to a winter wedding.

## Lands in
- Uses what the user actually has, and only names something to borrow or buy if the outfit truly does not exist without it. Short enough to act on straight away.

## Steps
1. Look up what people are actually wearing to what to wear to a winter wedding.
2. Look up the dress code, the weather and how formal it really gets at what to wear to a winter wedding.
3. Uses what the user actually has, and only names something to borrow or buy if the outfit truly does not exist without it.

## Success criteria
- Uses what the user actually has, and only names something to borrow or buy if
  the outfit truly does not exist without it.
- Reads the real formality level, including when the invitation oversells it.
- Accounts for weather, standing, dancing and the walk between venues.
- Gives one swap, not a second full outfit.

## Failure behavior
- If the dress code is unclear, say so and dress one notch up, with the reason.
- If a source will not load, skip it and keep going.

## Never
- Never sign in, buy, order or add anything to a cart.
- Never invent a dress code, a price or a store's stock.
- Never comment on the user's body, size or how they should look.

## Redaction
Omit query strings, account details, order history, saved cards, home address,
and anything shown after a page unexpectedly asks for a login.
