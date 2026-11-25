---
name: worth-watching
skill_id: browser-skill:worth-watching
description: What just landed on streaming that people are actually loving
when_to_use:
  - intent_keywords: [watch, movies, shows, streaming, film, series, tv]
    require_auth: false
    mutation_boundary: read_only
steps:
  - caption: new releases this week on streaming in
    capability_target: web_search
    mutation_boundary: read_only
  - caption: what audiences and critics are saying about the new
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
  - name: taste
    current_value: new films and series
    fill_rule: say what you are into and Luke tunes the picks
adapter_preferences:
  preferred: browserbase
  fallback: owned_browser
  declined: []
schema_version: 1
metadata:
  luke:
    tags: [movies, shows, streaming, discovery]
    related_skills: []
platforms: [macos]
---
# Worth watching

## Purpose
Thursday evening, the one thing worth putting on this weekend. Pick something in a minute, not twenty.

## Reads
- Search results for new releases this week on streaming in new films and series.
- Search results for what audiences and critics are saying about the new new films and series.

## Lands in
- Gives a clear pick, not a list of options. Short enough to act on straight away.

## Steps
1. Look up new releases this week on streaming in new films and series.
2. Look up what audiences and critics are saying about the new new films and series.
3. Gives a clear pick, not a list of options.

## Success criteria
- Gives a clear pick, not a list of options.
- Says why in one line, in plain language.
- Separates what critics said from what audiences said.

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
