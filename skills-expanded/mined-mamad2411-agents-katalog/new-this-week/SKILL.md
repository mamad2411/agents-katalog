---
name: new-this-week
skill_id: browser-skill:new-this-week
description: Friday afternoon, everything new from the artists and labels you follow
when_to_use:
  - intent_keywords: [new, drops, releases, music, singers, this week]
    require_auth: false
    mutation_boundary: read_only
steps:
  - caption: released, dropped or announced this week by
    capability_target: web_search
    mutation_boundary: read_only
  - caption: what people are saying about the new music from
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
  - name: following
    current_value: artists charting right now
    fill_rule: say who you follow and Luke keeps up with them
adapter_preferences:
  preferred: browserbase
  fallback: owned_browser
  declined: []
schema_version: 1
metadata:
  luke:
    tags: [music, drops, artists, discovery]
    related_skills: []
platforms: [macos]
---
# New this week

## Purpose
Friday afternoon, everything your artists dropped this week. New singles, features, surprise releases, all in one place.

## Reads
- Search results for released, dropped or announced this week by artists charting right now.
- Search results for what people are saying about the new music from artists charting right now.

## Lands in
- Leads with the single best thing, not the first thing found. Short enough to act on straight away.

## Steps
1. Look up released, dropped or announced this week by artists charting right now.
2. Look up what people are saying about the new music from artists charting right now.
3. Leads with the single best thing, not the first thing found.

## Success criteria
- Leads with the single best thing, not the first thing found.
- Sounds like a friend catching you up, not a newsletter.
- A quiet week is one cheerful line, not a padded list.

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
