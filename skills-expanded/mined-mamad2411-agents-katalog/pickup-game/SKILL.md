---
name: pickup-game
skill_id: browser-skill:pickup-game
description: A game, class or run club you can just turn up to this week
when_to_use:
  - intent_keywords: [pickup, run club, class, league, drop in, basketball, soccer, join]
    require_auth: false
    mutation_boundary: read_only
steps:
  - caption: pickup games, drop in classes and run clubs open to newcomers in
    capability_target: web_search
    mutation_boundary: read_only
  - caption: meeting times, courts and starting points for weekly drop in sport in
    capability_target: web_search
    mutation_boundary: read_only
trigger:
  kind: schedule
  recurrence: weekly
  weekday: 2
  time: 08:30
  timezone: America/Los_Angeles
  follows_device: true
parameters:
  - name: game
    current_value: Los Angeles
    fill_rule: say your city and your sport
adapter_preferences:
  preferred: browserbase
  fallback: owned_browser
  declined: []
schema_version: 1
metadata:
  luke:
    tags: [pickup, run club, sport, drop in, weekly]
    related_skills: [browser-skill:trail-today]
platforms: [macos]
---
# Pickup game

## Purpose
Monday morning, when the week is still empty enough to put something in it. One
game, class or run you can walk up to, no team and no sign up.

## Reads
- Search results for pickup games, drop in classes and run clubs open to newcomers in Los Angeles.
- Search results for meeting times, courts and starting points for weekly drop in sport in Los Angeles.

## Lands in
- Names one session with a real day, start time and meeting point. Short enough to act on straight away.

## Steps
1. Look up pickup games, drop in classes and run clubs open to newcomers in Los Angeles.
2. Look up meeting times, courts and starting points for weekly drop in sport in Los Angeles.
3. Names one session with a real day, start time and meeting point.

## Success criteria
- Names one session with a real day, start time and meeting point.
- Says plainly whether it is free, cash at the door, or needs a spot held.
- Says what the level is, so turning up alone is not a coin flip.

## Failure behavior
- If a group page will not load, skip it and keep going.
- If nothing is running this week, say so in one line and name the closest
  regular session.

## Never
- Never sign in, join a group, register or pay a drop in fee.
- Never invent a meeting time, a location or a skill level.
- Never pass a paid promotion off as an open community session.

## Redaction
Omit query strings, account details, order history, saved cards, home address,
and anything shown after a page unexpectedly asks for a login.
