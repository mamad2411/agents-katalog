---
name: spa-day
skill_id: browser-skill:spa-day
description: Where to go do nothing for a few hours
when_to_use:
  - intent_keywords: [spa, sauna, massage, bathhouse, treat, unwind, hot springs]
    require_auth: false
    mutation_boundary: read_only
steps:
  - caption: best spas, saunas, bathhouses and hot springs near
    capability_target: web_search
    mutation_boundary: read_only
  - caption: which ones people say are actually worth the money in
    capability_target: web_search
    mutation_boundary: read_only
parameters:
  - name: area
    current_value: spas saunas and bathhouses in Los Angeles
    fill_rule: say your city and Luke uses it instead
adapter_preferences:
  preferred: browserbase
  fallback: owned_browser
  declined: []
schema_version: 1
metadata:
  luke:
    tags: [spa, sauna, self care, unwind, treat]
    related_skills: []
platforms: [macos]
---
# Spa day

## Purpose
Somewhere to go and do absolutely nothing for a few hours. What it costs, what to book, and which one is worth it.

## Reads
- Search results for best spas, saunas, bathhouses and hot springs near spas saunas and bathhouses in Los Angeles.
- Search results for which ones people say are actually worth the money in spas saunas and bathhouses in Los Angeles.

## Lands in
- One place, with the price and whether booking is needed. Short enough to act on straight away.

## Steps
1. Look up best spas, saunas, bathhouses and hot springs near spas saunas and bathhouses in Los Angeles.
2. Look up which ones people say are actually worth the money in spas saunas and bathhouses in Los Angeles.
3. One place, with the price and whether booking is needed.

## Success criteria
- One place, with the price and whether booking is needed.
- Says what is included, because the extras are where the cost hides.
- Names a cheap option and a proper treat, and says which is which.
- Says the quiet time to go.

## Failure behavior
- If a listing will not load, skip it and keep going.
- If nothing good is on, say so in one line and name the reliable fallback.

## Never
- Never sign in, book, buy tickets or reserve anything.
- Never invent a price, an opening time, a venue or an appointment.
- Never pass a promoted listing off as what people rate.

## Redaction
Omit query strings, account details, order history, saved cards, home address,
and anything shown after a page unexpectedly asks for a login.
