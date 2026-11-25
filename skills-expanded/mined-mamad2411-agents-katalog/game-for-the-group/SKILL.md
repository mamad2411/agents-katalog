---
name: game-for-the-group
skill_id: browser-skill:game-for-the-group
description: One game the whole chat can be playing in ten minutes
when_to_use:
  - intent_keywords: [game to play with friends, co op, friendslop, party game, what should we play, multiplayer]
    require_auth: false
    mutation_boundary: read_only
steps:
  - caption: cheap co op games everyone is playing together right now like
    capability_target: web_search
    mutation_boundary: read_only
  - caption: player count, price and how long it takes to learn
    capability_target: web_search
    mutation_boundary: read_only
trigger:
  kind: schedule
  recurrence: weekly
  weekday: 6
  time: 17:15
  timezone: America/Los_Angeles
  follows_device: true
parameters:
  - name: your_crew
    current_value: best friendslop games to play with friends
    fill_rule: say how many of you there are and what you already own
adapter_preferences:
  preferred: browserbase
  fallback: owned_browser
  declined: []
schema_version: 1
metadata:
  luke:
    tags: [games, co op, friends, weekly, culture]
    related_skills: []
platforms: [macos]
---

# Game for the group

## Purpose
Friday afternoon, while everyone is still deciding. One game the group can all
be in tonight, chosen the way the group actually chooses: cheap, learnable in
one round, and funny when it goes wrong.

## Reads
- Search results for cheap co op games everyone is playing together right now like best friendslop games to play with friends.
- Search results for player count, price and how long it takes to learn best friendslop games to play with friends.

## Lands in
- Picks for the group, not for the player. Short enough to act on straight away.

## Steps
1. Look up cheap co op games everyone is playing together right now like best friendslop games to play with friends.
2. Look up player count, price and how long it takes to learn best friendslop games to play with friends.
3. Picks for the group, not for the player. A game everyone can learn in one round beats a better game where two people spend an hour in the tutorial.

## Success criteria
- Picks for the group, not for the player. A game everyone can learn in one
  round beats a better game where two people spend an hour in the tutorial.
- Leads with price and player cap. A cheap game all six people own beats a
  great game three people own, every single time, and this is the whole trick.
- Says whether it is a hang or a challenge. Half of what is popular right now
  is barely a game and works as somewhere to talk, which is fine but is a
  different night than a hard co op run.
- Names one thing that will go wrong and be funny. That is what gets clipped
  and that is why anyone plays these.
- Says if the servers are quiet, because a dead lobby ends the night.

## Failure behavior
- If nothing new fits the group, say so and name the one already installed.
- If a store page will not load, skip it and keep going.

## Never
- Never sign in, buy, gift, wishlist or post anything. The user does that part.
- Never invent a price, a player count, a review or a release date.
- Never punch down, and never recommend on a lobby known for abusing people.

## Redaction
Omit query strings, account details, order history, saved cards, and anything
shown after a page unexpectedly asks for a login.
