---
name: summer-in-europe
skill_id: browser-skill:summer-in-europe
description: Where to be, when to go, and what is on while you are there
when_to_use:
  - intent_keywords: [europe, summer, travel, trip, ibiza, greece, festivals abroad]
    require_auth: false
    mutation_boundary: read_only
steps:
  - caption: best time to go and what is on this summer in
    capability_target: web_search
    mutation_boundary: read_only
  - caption: what people are recommending right now for a summer trip to
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
  - name: cities
    current_value: Europe in summer
    fill_rule: say where you fancy going
adapter_preferences:
  preferred: browserbase
  fallback: owned_browser
  declined: []
schema_version: 1
metadata:
  luke:
    tags: [travel, europe, summer, festivals, trips]
    related_skills: []
platforms: [macos]
---
# Summer in Europe

## Purpose
Saturday morning, where's good in Europe right now, what's on while you'd be there, and what it'd take to go.

## Reads
- Search results for best time to go and what is on this summer in Europe in summer.
- Search results for what people are recommending right now for a summer trip to Europe in summer.

## Lands in
- Leads with one place and says why now, not someday. Short enough to act on straight away.

## Steps
1. Look up best time to go and what is on this summer in Europe in summer.
2. Look up what people are recommending right now for a summer trip to Europe in summer.
3. Leads with one place and says why now, not someday.

## Success criteria
- Leads with one place and says why now, not someday.
- Names what is on while they would be there.
- Keeps it to places the user actually listed.

## Failure behavior
- If a source will not load, skip it and keep going.
- If there is genuinely nothing, say so in one line and move on.

## Never
- Never sign in, buy tickets, book travel or join a waitlist.
- Never invent a date, a price, a lineup or a venue.
- Never pass a promoter's announcement off as independent reaction.

## Redaction
Omit query strings, account details, ticket orders, passport and booking
references, saved cards, home address, and anything shown after a page
unexpectedly asks for a login.
