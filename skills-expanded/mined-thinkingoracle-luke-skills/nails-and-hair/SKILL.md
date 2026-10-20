---
name: nails-and-hair
skill_id: browser-skill:nails-and-hair
description: What's good right now, and who near you actually does it well
when_to_use:
  - intent_keywords: [nails, hair, salon, manicure, color, braids, blowout, appointment]
    require_auth: false
    mutation_boundary: read_only
steps:
  - caption: what people are getting right now and what it is called in
    capability_target: web_search
    mutation_boundary: read_only
  - caption: which salons and stylists people rate for
    capability_target: web_search
    mutation_boundary: read_only
trigger:
  kind: schedule
  recurrence: weekly
  weekday: 5
  time: 17:15
  timezone: America/Los_Angeles
  follows_device: true
parameters:
  - name: looking_for
    current_value: nail and hair trends right now
    fill_rule: say what you are after and your city
adapter_preferences:
  preferred: browserbase
  fallback: owned_browser
  declined: []
schema_version: 1
metadata:
  luke:
    tags: [nails, hair, salon, beauty, self care]
    related_skills: []
platforms: [macos]
---
# Nails and hair

## Purpose
What is actually good right now, what to ask for by name so you get it, and who near you does it properly.

## Reads
- Search results for what people are getting right now and what it is called in nail and hair trends right now.
- Search results for which salons and stylists people rate for nail and hair trends right now.

## Lands in
- Names the look the way you would ask for it in the chair. Short enough to act on straight away.

## Steps
1. Look up what people are getting right now and what it is called in nail and hair trends right now.
2. Look up which salons and stylists people rate for nail and hair trends right now.
3. Names the look the way you would ask for it in the chair.

## Success criteria
- Names the look the way you would ask for it in the chair.
- Says roughly what it costs and how long it takes.
- Names real places people rate, not the best-advertised.
- Says how long it lasts, because that is the real cost.

## Failure behavior
- If a listing will not load, skip it and keep going.
- If nothing good is on, say so in one line and name the reliable fallback.

## Never
- Never sign in, book, buy tickets or reserve anything.
- Never invent a price, an opening time, a venue or an appointment.
- Never pass a promoted listing off as what people rate.

## Redaction
Omit query strings, account details, order history, saved cards, home address,
and anything shown after a page unexpectedly asks for a login.
