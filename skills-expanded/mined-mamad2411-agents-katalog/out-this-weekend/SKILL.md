---
name: out-this-weekend
skill_id: browser-skill:out-this-weekend
description: Festivals, gigs and things actually happening near you
when_to_use:
  - intent_keywords: [weekend, festival, gig, concert, events, whats on, near me]
    require_auth: false
    mutation_boundary: read_only
steps:
  - caption: festivals, gigs and events happening this weekend
    capability_target: web_search
    mutation_boundary: read_only
  - caption: what is worth going to this weekend
    capability_target: web_search
    mutation_boundary: read_only
trigger:
  kind: schedule
  recurrence: weekly
  weekday: 5
  time: 17:15
  timezone: America/Los_Angeles
  follows_device: true
parameters:
  - name: scene
    current_value: in Los Angeles
    fill_rule: say your city and Luke uses it instead
adapter_preferences:
  preferred: browserbase
  fallback: owned_browser
  declined: []
schema_version: 1
metadata:
  luke:
    tags: [festivals, events, gigs, weekend, local]
    related_skills: []
platforms: [macos]
---
# Out this weekend

## Purpose
Thursday, tell the user what is on this weekend where they live, so plans happen instead of a group chat that goes quiet.

## Reads
- Search results for festivals, gigs and events happening this weekend in Los Angeles.
- Search results for what is worth going to this weekend in Los Angeles.

## Lands in
- Names real events with real dates and venues. Short enough to act on straight away.

## Steps
1. Look up festivals, gigs and events happening this weekend in Los Angeles.
2. Look up what is worth going to this weekend in Los Angeles.
3. Names real events with real dates and venues.

## Success criteria
- Names real events with real dates and venues.
- Leads with one thing worth clearing the calendar for.
- Says plainly when the weekend is quiet.

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
