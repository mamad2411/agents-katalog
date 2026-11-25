---
name: what-should-i-learn
skill_id: browser-skill:what-should-i-learn
description: One skill worth learning right now in your field, and where to start today
when_to_use:
  - intent_keywords: [level up, learn, skill, get better, career, study, upskill]
    require_auth: false
    mutation_boundary: read_only
steps:
  - caption: skills employers are asking for right now
    capability_target: web_search
    mutation_boundary: read_only
  - caption: best free way to start learning
    capability_target: web_search
    mutation_boundary: read_only
trigger:
  kind: schedule
  recurrence: weekly
  weekday: 3
  time: 17:15
  timezone: America/Los_Angeles
  follows_device: true
parameters:
  - name: your_field
    current_value: in demand skills this year
    fill_rule: say what you do and Luke aims the search at your field
adapter_preferences:
  preferred: browserbase
  fallback: owned_browser
  declined: []
schema_version: 1
metadata:
  luke:
    tags: [learning, career, weekly, skills]
    related_skills: [browser-skill:work-on-my-side-project]
platforms: [macos]
---

# Level up

## Purpose
One skill that is actually worth your time this month, and the exact first
thing to open today. Getting sharper, without a six month course.

## Reads
- Search results for skills employers are asking for right now in demand skills this year.
- Search results for best free way to start learning in demand skills this year.

## Lands in
- One skill, not a curriculum. Short enough to act on straight away.

## Steps
1. Look up skills employers are asking for right now in demand skills this year.
2. Look up best free way to start learning in demand skills this year.
3. One skill, not a curriculum.

## Success criteria
- One skill, not a curriculum.
- The starting point is free and openable today.
- Says plainly why this skill and not the hyped one.

## Failure behavior
- If a source will not load, skip it and keep going.
- If nothing has really changed in the field, repeat last week's pick and say so.

## Never
- Never imply the user is behind or missing out.
- Never recommend something paid without saying the price up front.
- Never sign in, enroll, buy, or join a waitlist.

## Redaction
Omit query strings, account details, employer names the user has not shared,
and anything shown after a page unexpectedly asks for a login.
