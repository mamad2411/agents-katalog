---
name: what-should-i-work-on
skill_id: browser-skill:what-should-i-work-on
description: Your first focus block, already decided: what to work on and for how long
when_to_use:
  - intent_keywords: [lock in, focus, deep work, focus block, start working, concentrate]
    require_auth: false
    mutation_boundary: read_only
steps:
  - caption: how long a deep work block should be for
    capability_target: web_search
    mutation_boundary: read_only
  - caption: best way to start the hardest task of the day
    capability_target: web_search
    mutation_boundary: read_only
trigger:
  kind: schedule
  recurrence: daily
  time: 08:30
  timezone: America/Los_Angeles
  follows_device: true
parameters:
  - name: what_youre_chasing
    current_value: deep work focus block length
    fill_rule: say what you are working toward and Luke picks the first block
adapter_preferences:
  preferred: browserbase
  fallback: owned_browser
  declined: []
schema_version: 1
metadata:
  luke:
    tags: [focus, deep work, daily, momentum]
    related_skills: [browser-skill:clear-my-admin]
platforms: [macos]
---

# Lock in

## Purpose
The block is already decided before you sit down. One thing to work on, one
length of time, no negotiating with yourself at eight thirty.

## Reads
- Search results for how long a deep work block should be for deep work focus block length.
- Search results for best way to start the hardest task of the day deep work focus block length.

## Lands in
- Names one task, never a list to choose from. Short enough to act on straight away.

## Steps
1. Look up how long a deep work block should be for deep work focus block length.
2. Look up best way to start the hardest task of the day deep work focus block length.
3. Names one task, never a list to choose from.

## Success criteria
- Names one task, never a list to choose from.
- Gives a real number of minutes, not "a while."
- The first move is small enough to start without thinking.

## Failure behavior
- If a source will not load, skip it and keep going.
- If the day is already full, shorten the block instead of skipping it.

## Never
- Never mention blocks that were skipped before. A missed day does not exist.
- Never stack a second task on top of the one named.
- Never sign in, buy, book or join a waitlist.

## Redaction
Omit query strings, account details, calendar invitee names, home address,
and anything shown after a page unexpectedly asks for a login.
