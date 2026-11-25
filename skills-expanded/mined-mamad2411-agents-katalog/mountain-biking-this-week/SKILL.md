---
name: mountain-biking-this-week
skill_id: browser-skill:mountain-biking-this-week
description: Mountain biking, big lines, competitions and the clips everyone is watching
when_to_use:
  - intent_keywords: [mountain biking, mtb, redbull, downhill, skate, surf, adrenaline, sports]
    require_auth: false
    mutation_boundary: read_only
steps:
  - caption: best runs, results and clips this week in
    capability_target: web_search
    mutation_boundary: read_only
  - caption: upcoming events, qualifiers and finals coming up in
    capability_target: web_search
    mutation_boundary: read_only
trigger:
  kind: schedule
  recurrence: weekly
  weekday: 5
  time: 20:00
  timezone: America/Los_Angeles
  follows_device: true
parameters:
  - name: disciplines
    current_value: mountain biking and downhill
    fill_rule: say which sports and riders you follow
adapter_preferences:
  preferred: browserbase
  fallback: owned_browser
  declined: []
schema_version: 1
metadata:
  luke:
    tags: [mtb, adrenaline, redbull, competitions, sports]
    related_skills: []
platforms: [macos]
---
# Send it

## Purpose
Thursday evening, the runs worth rewatching, who won, and what is on this weekend, so the user catches the final live instead of the highlights on Monday.

## Reads
- Search results for best runs, results and clips this week in mountain biking and downhill.
- Search results for upcoming events, qualifiers and finals coming up in mountain biking and downhill.

## Lands in
- Leads with the run everyone is talking about. Short enough to act on straight away.

## Steps
1. Look up best runs, results and clips this week in mountain biking and downhill.
2. Look up upcoming events, qualifiers and finals coming up in mountain biking and downhill.
3. Leads with the run everyone is talking about.

## Success criteria
- Leads with the run everyone is talking about.
- Always says what is on next and when it goes live.
- Names the rider and the event, not just the trick.

## Failure behavior
- If a source will not load, skip it and keep going.
- If there is genuinely nothing, say so in one line and move on.

## Never
- Never sign in, buy tickets, book or join a waitlist.
- Never invent a result, a date, a name or a venue.
- Never pass a sponsored post off as what people are watching.

## Redaction
Omit query strings, account details, order history, saved cards, home address,
and anything shown after a page unexpectedly asks for a login.
