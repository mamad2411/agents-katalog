---
name: trip-ideas
skill_id: browser-skill:trip-ideas
description: Where is good right now, and what it would take to go
when_to_use:
  - intent_keywords: [travel, trip, flights, holiday, vacation, destination]
    require_auth: false
    mutation_boundary: read_only
steps:
  - caption: best time to visit and what is happening right now in
    capability_target: web_search
    mutation_boundary: read_only
  - caption: current travel conditions, seasons and events in
    capability_target: web_search
    mutation_boundary: read_only
trigger:
  kind: schedule
  recurrence: weekly
  weekday: 7
  time: 08:30
  timezone: America/Los_Angeles
  follows_device: true
parameters:
  - name: wishlist
    current_value: places good to visit right now
    fill_rule: say where you fancy and Luke watches for the moment to go
adapter_preferences:
  preferred: browserbase
  fallback: owned_browser
  declined: []
schema_version: 1
metadata:
  luke:
    tags: [travel, trips, destinations, discovery]
    related_skills: []
platforms: [macos]
---
# Trip ideas

## Purpose
Saturday morning, when you're daydreaming anyway. Where's genuinely good right now, and what it'd take to actually go.

## Reads
- Search results for best time to visit and what is happening right now in places good to visit right now.
- Search results for current travel conditions, seasons and events in places good to visit right now.

## Lands in
- Leads with the one place that is best right now, and says why now. Short enough to act on straight away.

## Steps
1. Look up best time to visit and what is happening right now in places good to visit right now.
2. Look up current travel conditions, seasons and events in places good to visit right now.
3. Leads with the one place that is best right now, and says why now.

## Success criteria
- Leads with the one place that is best right now, and says why now.
- Mentions the season or the event that makes it worth it.
- Keeps it to somewhere they actually listed.

## Failure behavior
- If a source will not load, skip it and keep going. Do not report the plumbing.
- If there is genuinely nothing, say so in one line and move on.

## Never
- Never sign in, buy, book, pre-order or join a waitlist.
- Never invent a date, a price, a venue or a review.
- Never pass an ad off as news, or a paid placement as an opinion.

## Redaction
Omit query strings, account details, order history, saved cards, home address,
and anything shown after a page unexpectedly asks for a login.
