---
name: trail-today
skill_id: browser-skill:trail-today
description: A hike, ride or run near you that fits the time you actually have
when_to_use:
  - intent_keywords: [trail, hike, trailhead, run, ride, walk, outside, nearby]
    require_auth: false
    mutation_boundary: read_only
steps:
  - caption: best trails for a hike, run or ride near
    capability_target: web_search
    mutation_boundary: read_only
  - caption: recent trail conditions, parking and trailhead reports near
    capability_target: web_search
    mutation_boundary: read_only
trigger:
  kind: schedule
  recurrence: daily
  time: 08:30
  timezone: America/Los_Angeles
  follows_device: true
parameters:
  - name: trails
    current_value: trails in Los Angeles
    fill_rule: say your city and Luke uses it instead
adapter_preferences:
  preferred: browserbase
  fallback: owned_browser
  declined: []
schema_version: 1
metadata:
  luke:
    tags: [trails, hiking, running, outdoors, daily]
    related_skills: [browser-skill:golden-hour]
platforms: [macos]
---
# Trail today

## Purpose
Eight thirty, shoes still by the door. One trail close enough to do
before the day takes over, sized to the hours the user actually has.

## Reads
- Search results for best trails for a hike, run or ride near trails in Los Angeles.
- Search results for recent trail conditions, parking and trailhead reports near trails in Los Angeles.

## Lands in
- Names one trail with a real distance and a real drive time to the trailhead. Short enough to act on straight away.

## Steps
1. Look up best trails for a hike, run or ride near trails in Los Angeles.
2. Look up recent trail conditions, parking and trailhead reports near trails in Los Angeles.
3. Names one trail with a real distance and a real drive time to the trailhead.

## Success criteria
- Names one trail with a real distance and a real drive time to the trailhead.
- Says where to park and whether that lot fills up early.
- Offers one shorter backup for a tighter morning.

## Failure behavior
- If a source will not load, skip it and keep going.
- If conditions look closed or unclear, say so in one line and name the next
  trail over.

## Never
- Never sign in, buy a permit or reserve a parking slot.
- Never invent a distance, an elevation gain or a trailhead.
- Never pass a sponsored listing off as a real trail recommendation.

## Redaction
Omit query strings, account details, order history, saved cards, home address,
and anything shown after a page unexpectedly asks for a login.
