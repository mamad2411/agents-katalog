---
name: good-food-near-you
skill_id: browser-skill:good-food-near-you
description: New openings and places people are raving about
when_to_use:
  - intent_keywords: [food, restaurant, eat, opening, dinner, brunch, near me]
    require_auth: false
    mutation_boundary: read_only
steps:
  - caption: new restaurant openings and food spots this month in
    capability_target: web_search
    mutation_boundary: read_only
  - caption: which places people are raving about right now in
    capability_target: web_search
    mutation_boundary: read_only
trigger:
  kind: schedule
  recurrence: weekly
  weekday: 5
  time: 12:30
  timezone: America/Los_Angeles
  follows_device: true
parameters:
  - name: tastes
    current_value: new restaurant openings in Los Angeles
    fill_rule: say your city and Luke uses it instead
adapter_preferences:
  preferred: browserbase
  fallback: owned_browser
  declined: []
schema_version: 1
metadata:
  luke:
    tags: [food, restaurants, openings, local]
    related_skills: []
platforms: [macos]
---
# Good food near you

## Purpose
Thursday, the one new place worth dragging someone to this weekend. So when the group chat says "where," you're the one who answers.

## Reads
- Search results for new restaurant openings and food spots this month in new restaurant openings in Los Angeles.
- Search results for which places people are raving about right now in new restaurant openings in Los Angeles.

## Lands in
- Names real places with neighborhoods. Short enough to act on straight away.

## Steps
1. Look up new restaurant openings and food spots this month in new restaurant openings in Los Angeles.
2. Look up which places people are raving about right now in new restaurant openings in Los Angeles.
3. Names real places with neighborhoods.

## Success criteria
- Names real places with neighborhoods.
- Gives one clear recommendation, not a top ten.
- Says what the place is known for in a few words.

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
