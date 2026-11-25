---
name: residency-radar
skill_id: browser-skill:residency-radar
description: The weekly nights that never get announced because they are always on
when_to_use:
  - intent_keywords: [weekly, residency, regular night, weeknight, club night, recurring, every week]
    require_auth: false
    mutation_boundary: read_only
steps:
  - caption: weekly club nights, residencies and long running weeknight parties in
    capability_target: web_search
    mutation_boundary: read_only
  - caption: which weeklies have been running for years and who actually goes in
    capability_target: web_search
    mutation_boundary: read_only
trigger:
  kind: schedule
  recurrence: weekly
  weekday: 2
  time: 12:30
  timezone: America/Los_Angeles
  follows_device: true
parameters:
  - name: scene
    current_value: Los Angeles
    fill_rule: say your city and your scene
adapter_preferences:
  preferred: browserbase
  fallback: owned_browser
  declined: []
schema_version: 1
metadata:
  luke:
    tags: [weekly, residency, weeknights, club nights, nightlife]
    related_skills: [browser-skill:which-night-is-which]
platforms: [macos]
---
# Residency radar

## Purpose
Monday late morning, with the whole week still open. Weekly nights never show up in an events feed because there is nothing to announce, so this is the pass that finds the ones running quietly on the same night for years.

## Reads
- Search results for weekly club nights, residencies and long running weeknight parties in Los Angeles.
- Search results for which weeklies have been running for years and who actually goes in Los Angeles.

## Lands in
- Searches venue calendars and the night's own account rather than events feeds, because a weekly with nothing to announce never buys a listing. Short enough to act on straight away.

## Steps
1. Look up weekly club nights, residencies and long running weeknight parties in Los Angeles.
2. Look up which weeklies have been running for years and who actually goes in Los Angeles.
3. Searches venue calendars and the night's own account rather than events feeds, because a weekly with nothing to announce never buys a listing.

## Success criteria
- Searches venue calendars and the night's own account rather than events feeds, because a weekly with nothing to announce never buys a listing.
- Knows the weeknight map. Monday is goth and industrial in most cities, and the San Francisco one has run every Monday since 1993. Tuesday is Latin social dancing. Wednesday carries a second goth night. Thursday is where promoters test new bookings.
- Mentions the lesson. Latin nights put a free beginner class before the social, usually starting around 6:30pm, and that hour is the friendliest a room ever is to somebody arriving alone.
- Flags industry nights, which land Sunday and Monday because that is when the people who work the weekend are finally off.
- Includes the Sunday daytime option, since day parties and coffee sets now start in the afternoon and finish early enough to work on Monday.
- Says how long each night has run, because a weekly that survived a decade is a different proposition from one on its fourth week.

## Failure behavior
- If a venue calendar will not load, skip it and keep going.
- If the city has no real weeklies, say so in one line and name the best one-off happening this week.

## Never
- Never sign in, RSVP, buy tickets or join a list.
- Never invent a night, a venue or a start time.
- Never list a night that has stopped running as though it is still on.

## Redaction
Omit query strings, account details, ticket orders, saved cards, home address,
and anything shown after a page unexpectedly asks for a login.
