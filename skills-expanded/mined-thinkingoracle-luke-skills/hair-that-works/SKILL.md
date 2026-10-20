---
name: hair-that-works
skill_id: browser-skill:hair-that-works
description: What people with your hair are actually using
when_to_use:
  - intent_keywords: [hair, shampoo, conditioner, curls, scalp, routine, haircare]
    require_auth: false
    mutation_boundary: read_only
steps:
  - caption: what people are getting results with this month for
    capability_target: web_search
    mutation_boundary: read_only
  - caption: which shampoos and treatments actually work for
    capability_target: web_search
    mutation_boundary: read_only
trigger:
  kind: schedule
  recurrence: weekly
  weekday: 1
  time: 17:15
  timezone: America/Los_Angeles
  follows_device: true
parameters:
  - name: hair_type
    current_value: curly, fine and color-treated hair
    fill_rule: say your hair type and what you want to fix
adapter_preferences:
  preferred: browserbase
  fallback: owned_browser
  declined: []
schema_version: 1
metadata:
  luke:
    tags: [hair, haircare, shampoo, routines]
    related_skills: []
platforms: [macos]
---
# Hair that works

## Purpose
Sunday evening, what people with your hair are actually getting results with. So the next bottle isn't another guess.

## Reads
- Search results for what people are getting results with this month for curly, fine and color-treated hair.
- Search results for which shampoos and treatments actually work for curly, fine and color-treated hair.

## Lands in
- Names real products people report results with. Short enough to act on straight away.

## Steps
1. Look up what people are getting results with this month for curly, fine and color-treated hair.
2. Look up which shampoos and treatments actually work for curly, fine and color-treated hair.
3. Names real products people report results with.

## Success criteria
- Names real products people report results with.
- Explains why it suits that hair type in one line.
- Flags what is mostly fragrance and marketing.

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
