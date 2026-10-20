---
name: good-news-only
skill_id: browser-skill:good-news-only
description: The things that actually went right in the world this week
when_to_use:
  - intent_keywords: [good news, positive news, uplifting, something good, wins, hopeful]
    require_auth: false
    mutation_boundary: read_only
steps:
  - caption: good news stories and real wins reported this week in
    capability_target: web_search
    mutation_boundary: read_only
  - caption: breakthroughs and progress announced this week in
    capability_target: web_search
    mutation_boundary: read_only
trigger:
  kind: schedule
  recurrence: weekly
  weekday: 6
  time: 17:15
  timezone: America/Los_Angeles
  follows_device: true
parameters:
  - name: beats
    current_value: science, medicine, conservation and community projects
    fill_rule: say which corners of the world you want good news from
adapter_preferences:
  preferred: browserbase
  fallback: owned_browser
  declined: []
schema_version: 1
metadata:
  luke:
    tags: [good news, positive, weekly, science, community]
    related_skills: []
platforms: [macos]
---
# Good news only

## Purpose
Friday afternoon, the three things that actually went right this week. You end the week knowing something good, and you have it ready when someone needs it.

## Reads
- Search results for good news stories and real wins reported this week in science, medicine, conservation and community projects.
- Search results for breakthroughs and progress announced this week in science, medicine, conservation and community projects.

## Lands in
- Three things, each a real outcome with a real source. Short enough to act on straight away.

## Steps
1. Look up good news stories and real wins reported this week in science, medicine, conservation and community projects.
2. Look up breakthroughs and progress announced this week in science, medicine, conservation and community projects.
3. Three things, each a real outcome with a real source.

## Success criteria
- Three things, each a real outcome with a real source.
- Says what changed and who it helps, in plain words.
- Stays on the good side. Progress and recovery, never the disaster behind it.
- A thin week is two good things, not a stretched one.

## Failure behavior
- If a source will not load, skip it and keep going.
- If a beat has nothing this week, drop it and fill from the others.

## Never
- Never sign in, subscribe, donate or join a waitlist.
- Never invent a number, a study, a date or a name.
- Nothing cruel. No tragedy told as uplift, no charity bait.

## Redaction
Omit query strings, account details, order history, saved cards, home address,
and anything shown after a page unexpectedly asks for a login.
