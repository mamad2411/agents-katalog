---
name: first-class-free
skill_id: browser-skill:first-class-free
description: Run clubs, climbing gyms and studios you can try for nothing
when_to_use:
  - intent_keywords: [run club, climbing gym, free intro, try a class, beginner night, first class free]
    require_auth: false
    mutation_boundary: read_only
steps:
  - caption: free run clubs, group runs and free intro or beginner nights near
    capability_target: web_search
    mutation_boundary: read_only
  - caption: which night they meet, where they start and whether first timers pay anything near
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
  - name: activity
    current_value: free intro class in Los Angeles
    fill_rule: say your city and Luke uses it instead
adapter_preferences:
  preferred: browserbase
  fallback: owned_browser
  declined: []
schema_version: 1
metadata:
  luke:
    tags: [fitness, free, local, weekly, trying something new]
    related_skills: [browser-skill:pickup-game]
platforms: [macos]
---
# First class free

## Purpose
Tuesday evening, when there is still a whole week to use. The city is full of
groups that let a total stranger walk up once for free, and the only reason
people do not go is that nobody told them it was allowed.

## Reads
- Search results for free run clubs, group runs and free intro or beginner nights near free intro class in Los Angeles.
- Search results for which night they meet, where they start and whether first timers pay anything near free intro class in Los Angeles.

## Lands in
- Says plainly that most run clubs take guests with no membership and no fee, and that parkrun and November Project have no membership at all. Short enough to act on straight away.

## Steps
1. Look up free run clubs, group runs and free intro or beginner nights near free intro class in Los Angeles.
2. Look up which night they meet, where they start and whether first timers pay anything near free intro class in Los Angeles.
3. Says plainly that most run clubs take guests with no membership and no fee, and that parkrun and November Project have no membership at all.

## Success criteria
- Says plainly that most run clubs take guests with no membership and no fee,
  and that parkrun and November Project have no membership at all.
- Names the specific weeknight and the meeting spot, since these are fixed and
  weekly and showing up is the entire commitment.
- Flags climbing gym deals by name where they exist, like a free intro to
  bouldering class bundled with a day pass, half price beginner nights, and
  open houses where shoes and harness are included.
- Marks whether a club is no drop or all paces, so a slow first timer is not
  left alone on a dark street.
- Every pick states the real cost of walking in once, and free means free with
  nothing to sign at the door.

## Failure behavior
- If a club page will not load, skip it and keep going.
- If nothing meets this week, say so in one line and give next week's night.

## Never
- Never sign in, register, buy a pass or join a mailing list.
- Never invent a meeting night, a start point or a free trial.
- Never present a paid trial or a first month offer as a free drop in.

## Redaction
Omit query strings, account details, membership records, saved cards, home
address, and anything shown after a page unexpectedly asks for a login.
