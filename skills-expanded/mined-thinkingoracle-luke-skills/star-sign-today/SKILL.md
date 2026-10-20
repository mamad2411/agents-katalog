---
name: star-sign-today
skill_id: browser-skill:star-sign-today
description: A light daily horoscope, read for fun with your morning coffee
when_to_use:
  - intent_keywords: [horoscope, star sign, zodiac, astrology, my sign, whats my horoscope]
    require_auth: false
    mutation_boundary: read_only
steps:
  - caption: daily horoscope for today for
    capability_target: web_search
    mutation_boundary: read_only
  - caption: what the stars say about today for
    capability_target: web_search
    mutation_boundary: read_only
trigger:
  kind: schedule
  recurrence: daily
  time: 08:30
  timezone: America/Los_Angeles
  follows_device: true
parameters:
  - name: sign
    current_value: leo
    fill_rule: say your star sign, and anyone else's you want read too
adapter_preferences:
  preferred: browserbase
  fallback: owned_browser
  declined: []
schema_version: 1
metadata:
  luke:
    tags: [horoscope, zodiac, fun, daily, culture]
    related_skills: []
platforms: [macos]
---
# Star sign today

## Purpose
With the first coffee, your horoscope for the day, delivered with a raised eyebrow. Fun to read, better to send to the person it obviously describes.

## Reads
- Search results for daily horoscope for today for leo.
- Search results for what the stars say about today for leo.

## Lands in
- Two lines, playful, with a wink in them. Short enough to act on straight away.

## Steps
1. Look up daily horoscope for today for leo.
2. Look up what the stars say about today for leo.
3. Two lines, playful, with a wink in them.

## Success criteria
- Two lines, playful, with a wink in them.
- Picks the one specific detail worth quoting, not the vague part.
- Covers every sign the user asked for.
- Reads like a friend teasing you, never like a prophecy.

## Failure behavior
- If a source will not load, skip it and keep going.
- If today's reading is not published yet, say so in one line.

## Never
- Never sign in, subscribe, pay for a reading or join a waitlist.
- Never invent a chart, a date or a prediction.
- Nothing cruel. No warnings about health, money or anyone's relationship.

## Redaction
Omit query strings, account details, order history, saved cards, home address,
and anything shown after a page unexpectedly asks for a login.
