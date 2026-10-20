---
name: beauty-drops
skill_id: browser-skill:beauty-drops
description: New launches worth your money, and the ones to skip
when_to_use:
  - intent_keywords: [sephora, beauty, makeup, launch, drops, ulta, new]
    require_auth: false
    mutation_boundary: read_only
steps:
  - caption: new beauty launches and restocks this week from
    capability_target: web_search
    mutation_boundary: read_only
  - caption: which new launches people say are actually worth it from
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
  - name: brands
    current_value: the big beauty brands
    fill_rule: say which brands you follow
adapter_preferences:
  preferred: browserbase
  fallback: owned_browser
  declined: []
schema_version: 1
metadata:
  luke:
    tags: [beauty, makeup, sephora, launches, discovery]
    related_skills: []
platforms: [macos]
---
# Beauty drops

## Purpose
Thursday, what just landed and whether it's worth it. Your money goes on the good stuff.

## Reads
- Search results for new beauty launches and restocks this week from the big beauty brands.
- Search results for which new launches people say are actually worth it from the big beauty brands.

## Lands in
- Leads with the one launch actually worth it. Short enough to act on straight away.

## Steps
1. Look up new beauty launches and restocks this week from the big beauty brands.
2. Look up which new launches people say are actually worth it from the big beauty brands.
3. Leads with the one launch actually worth it.

## Success criteria
- Leads with the one launch actually worth it.
- Says who it suits, in a few words.
- Calls out the overhyped one, kindly.

## Failure behavior
- If a source will not load, skip it and keep going.
- If there is genuinely nothing, say so in one line and move on.

## Never
- Never sign in, buy, book, reserve or join a waitlist.
- Never invent a price, a date, a venue or a review.
- Never pass an ad off as a recommendation.

## Redaction
Omit query strings, account details, order history, saved cards, home address,
and anything shown after a page unexpectedly asks for a login.
