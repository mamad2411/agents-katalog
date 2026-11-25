---
name: market-day
skill_id: browser-skill:market-day
description: Your farmers market, the good stalls, and the hour prices drop
when_to_use:
  - intent_keywords: [farmers market, market day, produce, local food, cheap groceries, SNAP]
    require_auth: false
    mutation_boundary: read_only
steps:
  - caption: farmers market days, hours and locations near
    capability_target: web_search
    mutation_boundary: read_only
  - caption: which vendors to hit, closing time discounts and SNAP token matching at markets near
    capability_target: web_search
    mutation_boundary: read_only
trigger:
  kind: schedule
  recurrence: weekly
  weekday: 7
  time: 08:30
  timezone: America/Los_Angeles
  follows_device: true
parameters:
  - name: market
    current_value: farmers market in Los Angeles
    fill_rule: say your city and Luke uses it instead
adapter_preferences:
  preferred: browserbase
  fallback: owned_browser
  declined: []
schema_version: 1
metadata:
  luke:
    tags: [farmers market, food, local, weekly, cheap]
    related_skills: [browser-skill:what-to-cook-tonight]
platforms: [macos]
---
# Market day

## Purpose
Saturday morning, market day in most towns. Which market is on, which stalls
are worth the walk, and the exact hour to come back if the goal is to spend
as little as possible.

## Reads
- Search results for farmers market days, hours and locations near farmers market in Los Angeles.
- Search results for which vendors to hit, closing time discounts and SNAP token matching at markets near farmers market in Los Angeles.

## Lands in
- Gives the real closing time, then names the discount hour, because vendors commonly cut 20 to 50 percent in the last 30 to 60 minutes rather than haul produce home. Short enough to act on straight away.

## Steps
1. Look up farmers market days, hours and locations near farmers market in Los Angeles.
2. Look up which vendors to hit, closing time discounts and SNAP token matching at markets near farmers market in Los Angeles.
3. Gives the real closing time, then names the discount hour, because vendors commonly cut 20 to 50 percent in the last 30 to 60 minutes rather than haul produce home.

## Success criteria
- Gives the real closing time, then names the discount hour, because vendors
  commonly cut 20 to 50 percent in the last 30 to 60 minutes rather than haul
  produce home.
- Says whether the market matches SNAP dollars at the info booth, since Double
  Up Food Bucks style programs double the spend up to a daily cap, often in the
  20 to 50 dollar range per market day.
- Explains that the match is claimed at a booth in tokens before shopping, not
  at the stalls, which is the step that trips first timers.
- Names actual stalls or products, not just the market.
- Says whether early or late is the better trade: best selection first, best
  prices last.

## Failure behavior
- If a market page will not load, skip it and keep going.
- If the market is dark this week, say so in one line and name the next one.

## Never
- Never sign in, preorder, or reserve anything from a vendor.
- Never invent market hours, a vendor, a price or a benefit program.
- Never state a benefit match amount without a source saying so for that market.

## Redaction
Omit query strings, account details, benefit balances, saved cards, home
address, and anything shown after a page unexpectedly asks for a login.
