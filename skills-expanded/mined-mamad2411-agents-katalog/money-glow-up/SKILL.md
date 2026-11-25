---
name: money-glow-up
skill_id: browser-skill:money-glow-up
description: One move this week that makes you better off, in plain words
when_to_use:
  - intent_keywords: [money, finance, saving, invest, budget, rates, broke]
    require_auth: false
    mutation_boundary: read_only
steps:
  - caption: one practical money move worth making this month for
    capability_target: web_search
    mutation_boundary: read_only
  - caption: what people who are good with money actually did first about
    capability_target: web_search
    mutation_boundary: read_only
trigger:
  kind: schedule
  recurrence: weekly
  weekday: 5
  time: 12:30
  timezone: America/Los_Angeles
  follows_device: true
parameters:
  - name: focus
    current_value: high yield savings and index fund basics
    fill_rule: say what you are working on with money
adapter_preferences:
  preferred: browserbase
  fallback: owned_browser
  declined: []
schema_version: 1
metadata:
  luke:
    tags: [money, saving, basics, independence]
    related_skills: []
platforms: [macos]
---
# Money glow up

## Purpose
One move this week that leaves you better off, explained like a friend who is good with money and not smug about it.

## Reads
- Search results for one practical money move worth making this month for high yield savings and index fund basics.
- Search results for what people who are good with money actually did first about high yield savings and index fund basics.

## Lands in
- One move, with the actual dollar difference it makes. Short enough to act on straight away.

## Steps
1. Look up one practical money move worth making this month for high yield savings and index fund basics.
2. Look up what people who are good with money actually did first about high yield savings and index fund basics.
3. One move, with the actual dollar difference it makes.

## Success criteria
- One move, with the actual dollar difference it makes.
- Plain words. No jargon, and nothing that assumes you already have money.
- Says how long it takes to do, so it gets done.
- Never tells you what to buy or sell.

## Failure behavior
- If a source will not load, skip it and keep going.
- If nothing is on, say so in one line and give the best fallback.

## Never
- Never sign in, book, buy tickets or reserve anything.
- Never invent a venue, a time, a price or a lineup.
- Never pass a promoted listing off as what people rate.

## Redaction
Omit query strings, account details, order history, saved cards, home address,
and anything shown after a page unexpectedly asks for a login.
