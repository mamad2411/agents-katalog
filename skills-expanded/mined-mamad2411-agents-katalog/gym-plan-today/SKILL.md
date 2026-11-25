---
name: gym-plan-today
skill_id: browser-skill:gym-plan-today
description: Today's session, already decided, based on what you did recently
when_to_use:
  - intent_keywords: [gym, workout, training, lift, session, run, exercise]
    require_auth: false
    mutation_boundary: read_only
steps:
  - caption: what to train today after an upper body session
    capability_target: web_search
    mutation_boundary: read_only
  - caption: a forty five minute workout that fits a busy day
    capability_target: web_search
    mutation_boundary: read_only
trigger:
  kind: schedule
  recurrence: daily
  time: 06:00
  timezone: America/Los_Angeles
  follows_device: true
parameters:
  - name: training_style
    current_value: forty five minute full body workout
    fill_rule: say how you train and Luke writes today's session to match
adapter_preferences:
  preferred: browserbase
  fallback: owned_browser
  declined: []
schema_version: 1
metadata:
  luke:
    tags: [gym, training, daily, health]
    related_skills: []
platforms: [macos]
---

# Gym plan today

## Purpose
Today's session is picked before you get there. What to train, how long, and
the first lift. No standing around deciding.

## Reads
- Search results for what to train today after an upper body session forty five minute full body workout.
- Search results for a forty five minute workout that fits a busy day forty five minute full body workout.

## Lands in
- Fits the stated time, including warm up. Short enough to act on straight away.

## Steps
1. Look up what to train today after an upper body session forty five minute full body workout.
2. Look up a forty five minute workout that fits a busy day forty five minute full body workout.
3. Fits the stated time, including warm up.

## Success criteria
- Fits the stated time, including warm up.
- Names real movements with sets and reps, not vibes.
- Offers a shorter version for a bad day, same session, less volume.

## Failure behavior
- If a source will not load, skip it and keep going.
- If recent sessions are unknown, give a safe full body default.

## Never
- Never mention missed sessions, streaks, or time off.
- Never give medical, injury, diet, or supplement advice.
- Never sign in, book a class, or buy anything.

## Redaction
Omit query strings, account details, gym membership details, body metrics,
home address, and anything shown after a page unexpectedly asks for a login.
