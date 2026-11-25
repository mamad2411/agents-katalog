---
name: new-obsession
skill_id: browser-skill:new-obsession
description: One hobby, skill or rabbit hole worth falling into this month
when_to_use:
  - intent_keywords: [hobby, new skill, learn something, rabbit hole, obsession, pick up]
    require_auth: false
    mutation_boundary: read_only
steps:
  - caption: fun new hobbies and skills to pick up this month
    capability_target: web_search
    mutation_boundary: read_only
  - caption: rabbit holes people fell into and loved
    capability_target: web_search
    mutation_boundary: read_only
trigger:
  kind: schedule
  recurrence: weekly
  weekday: 1
  time: 08:30
  timezone: America/Los_Angeles
  follows_device: true
parameters:
  - name: obsession
    current_value: creative hobbies for beginners
    fill_rule: say what kind of thing you want to get into
adapter_preferences:
  preferred: browserbase
  fallback: owned_browser
  declined: []
schema_version: 1
metadata:
  luke:
    tags: [hobbies, learning, curiosity, monthly, fun]
    related_skills: []
platforms: [macos]
---
# New obsession

## Purpose
Sunday morning, coffee in hand, room for something new. One hobby or rabbit
hole worth falling into, with the first hour already mapped out for you.

## Reads
- Search results for fun new hobbies and skills to pick up this month creative hobbies for beginners.
- Search results for rabbit holes people fell into and loved creative hobbies for beginners.

## Lands in
- One pick, with a first step the user can take today for little or nothing. Short enough to act on straight away.

## Steps
1. Look up fun new hobbies and skills to pick up this month creative hobbies for beginners.
2. Look up rabbit holes people fell into and loved creative hobbies for beginners.
3. One pick, with a first step the user can take today for little or nothing.

## Success criteria
- One pick, with a first step the user can take today for little or nothing.
- Says what makes it fun early, so week one carries its own reward.
- Names one place to go deeper once it takes hold.

## Failure behavior
- If a source will not load, skip it and keep going.
- If nothing fresh turns up, bring back a classic and say why it still lands.

## Never
- Never sign in, buy gear, or join a waitlist.
- Never invent a course, a price, or a community.
- Never pass a sponsored post off as a real recommendation.

## Redaction
Omit query strings, account details, order history, saved cards, home address,
and anything shown after a page unexpectedly asks for a login.
