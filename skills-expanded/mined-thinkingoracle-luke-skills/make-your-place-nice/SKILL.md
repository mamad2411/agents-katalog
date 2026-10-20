---
name: make-your-place-nice
skill_id: browser-skill:make-your-place-nice
description: One small thing to change about your place this week
when_to_use:
  - intent_keywords: [home, apartment, my place, room, decorate, interiors, make it nicer]
    require_auth: false
    mutation_boundary: read_only
steps:
  - caption: small changes that make a rented place feel better for
    capability_target: web_search
    mutation_boundary: read_only
  - caption: what it costs and how long it actually takes to
    capability_target: web_search
    mutation_boundary: read_only
trigger:
  kind: schedule
  recurrence: weekly
  weekday: 7
  time: 08:30
  timezone: America/Los_Angeles
  follows_device: true
parameters:
  - name: your_place
    current_value: small apartment upgrades under 50 dollars
    fill_rule: describe your place and the one corner that bugs you
adapter_preferences:
  preferred: browserbase
  fallback: owned_browser
  declined: []
schema_version: 1
metadata:
  luke:
    tags: [home, apartment, weekly, small projects, interiors]
    related_skills: []
platforms: [macos]
---
# Make your place nice

## Purpose
Saturday morning, with a couple of free hours. One small change to the user's
place that is doable today, reversible if they rent, and noticeable every time
they walk in.

## Reads
- Search results for small changes that make a rented place feel better for small apartment upgrades under 50 dollars.
- Search results for what it costs and how long it actually takes to small apartment upgrades under 50 dollars.

## Lands in
- One change, sized to a free afternoon, not a renovation. Short enough to act on straight away.

## Steps
1. Look up small changes that make a rented place feel better for small apartment upgrades under 50 dollars.
2. Look up what it costs and how long it actually takes to small apartment upgrades under 50 dollars.
3. One change, sized to a free afternoon, not a renovation.

## Success criteria
- One change, sized to a free afternoon, not a renovation.
- Says the honest cost and the honest time, including the boring part.
- Stays reversible for renters, or flags plainly when it is not.
- Says what the change actually does for the room, in a line.

## Failure behavior
- If a source will not load, skip it and keep going.
- If nothing fits this week's budget or time, say so and give the free version.

## Never
- Never sign in, buy, order or add anything to a cart.
- Never invent a price, a product or a store's stock.
- Never suggest anything that needs a landlord's permission without saying so.

## Redaction
Omit query strings, account details, order history, saved cards, home address,
and anything shown after a page unexpectedly asks for a login.
