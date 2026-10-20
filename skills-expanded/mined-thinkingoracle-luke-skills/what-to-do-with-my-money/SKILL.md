---
name: what-to-do-with-my-money
skill_id: browser-skill:what-to-do-with-my-money
description: One money thing worth doing this week, in plain language
when_to_use:
  - intent_keywords: [money, savings, budget, finances, money move, cash, bills]
    require_auth: false
    mutation_boundary: read_only
steps:
  - caption: best high yield savings account rates this week
    capability_target: web_search
    mutation_boundary: read_only
  - caption: how to lower a recurring monthly bill without switching providers
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
  - name: money_focus
    current_value: high yield savings account rates
    fill_rule: say what you are trying to sort out and Luke aims at that
adapter_preferences:
  preferred: browserbase
  fallback: owned_browser
  declined: []
schema_version: 1
metadata:
  luke:
    tags: [money, weekly, practical, savings]
    related_skills: []
platforms: [macos]
---

# Money moves

## Purpose
One practical money thing per week, written for people who are not rich yet.
Something you can finish over lunch, not a plan for a life you do not have.

## Reads
- Search results for best high yield savings account rates this week high yield savings account rates.
- Search results for how to lower a recurring monthly bill without switching providers high yield savings account rates.

## Lands in
- Plain words only. Short enough to act on straight away.

## Steps
1. Look up best high yield savings account rates this week high yield savings account rates.
2. Look up how to lower a recurring monthly bill without switching providers high yield savings account rates.
3. Plain words only. No jargon that needs a second search.

## Success criteria
- Plain words only. No jargon that needs a second search.
- States the actual dollar impact, or says honestly that it is small.
- Doable this week without a lawyer, an advisor, or a lump sum.

## Failure behavior
- If a source will not load, skip it and keep going.
- If nothing is genuinely worth doing this week, say so in one line.

## Never
- Never give personalized investment advice or name a security to buy.
- Never sign in, buy, book, apply, or move money.
- Never shame a spending habit or compare the user to anyone.

## Redaction
Omit query strings, account details, balances, order history, saved cards,
home address, and anything shown after a page unexpectedly asks for a login.
