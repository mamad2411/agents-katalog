---
name: what-should-i-wear
skill_id: browser-skill:what-should-i-wear
description: What is landing right now in style and grooming
when_to_use:
  - intent_keywords: [style, fit, outfit, grooming, fashion, look, wardrobe]
    require_auth: false
    mutation_boundary: read_only
steps:
  - caption: what is landing right now in style, fits and grooming for
    capability_target: web_search
    mutation_boundary: read_only
  - caption: what people are actually wearing and rating this season in
    capability_target: web_search
    mutation_boundary: read_only
trigger:
  kind: schedule
  recurrence: weekly
  weekday: 7
  time: 12:30
  timezone: America/Los_Angeles
  follows_device: true
parameters:
  - name: style
    current_value: everyday street style
    fill_rule: say your style and what you are going for
adapter_preferences:
  preferred: browserbase
  fallback: owned_browser
  declined: []
schema_version: 1
metadata:
  luke:
    tags: [style, fashion, grooming, discovery]
    related_skills: []
platforms: [macos]
---
# Fit check

## Purpose
Saturday late morning, what's landing right now. One thing you could actually wear this week.

## Reads
- Search results for what is landing right now in style, fits and grooming for everyday street style.
- Search results for what people are actually wearing and rating this season in everyday street style.

## Lands in
- One thing you could actually wear this week, not a trend you'd have to become a different person to pull off. Short enough to act on straight away.

## Steps
1. Look up what is landing right now in style, fits and grooming for everyday street style.
2. Look up what people are actually wearing and rating this season in everyday street style.
3. One thing you could actually wear this week, not a trend you'd have to become a different person to pull off.

## Success criteria
- One thing you could actually wear this week, not a trend you'd have to become a different person to pull off.
- Keeps it to the style the user actually said.
- Says where to find it, when that is obvious.

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
