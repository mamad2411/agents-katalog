---
name: crypto-pulse
skill_id: browser-skill:crypto-pulse
description: Where BTC and ETH are sitting, and what actually moved the market
when_to_use:
  - intent_keywords: [crypto, bitcoin, btc, ethereum, eth, price, market, coins]
    require_auth: false
    mutation_boundary: read_only
steps:
  - caption: current price and this week's move for
    capability_target: web_search
    mutation_boundary: read_only
  - caption: what actually moved the market this week for
    capability_target: web_search
    mutation_boundary: read_only
trigger:
  kind: schedule
  recurrence: daily
  time: 08:30
  timezone: America/Los_Angeles
  follows_device: true
parameters:
  - name: coins
    current_value: BTC, ETH
    fill_rule: say which coins you watch to change this list
adapter_preferences:
  preferred: browserbase
  fallback: owned_browser
  declined: []
schema_version: 1
metadata:
  luke:
    tags: [crypto, bitcoin, ethereum, markets, prices]
    related_skills: [browser-skill:whats-new-in-ai]
platforms: [macos]
---

# Crypto pulse

## Purpose
Every morning, where the user's coins are sitting and the one thing that actually
moved them, so they are current in ten seconds instead of ten tabs.

## Reads
- Search results for current price and this week's move for BTC, ETH.
- Search results for what actually moved the market this week for BTC, ETH.

## Lands in
- Leads with the price and the direction, in plain numbers. Short enough to act on straight away.

## Steps
1. Look up current price and this week's move for BTC, ETH.
2. Look up what actually moved the market this week for BTC, ETH.
3. Leads with the price and the direction, in plain numbers.

## Success criteria
- Leads with the price and the direction, in plain numbers.
- Gives one reason, attributed, not a wall of theories.
- Says plainly when it has been a flat, boring day.

## Failure behavior
- If a quote will not load, say which coin and keep going with the rest.
- If nothing moved, say so in one line. Do not manufacture a narrative.

## Never
- Never sign in, trade, transfer, buy or sell anything.
- Never tell the user what to buy, sell or hold.
- Never invent a price, and never state a cause the source does not give.

## Redaction
Omit query strings, wallet addresses, balances, holdings, exchange accounts, and
anything shown after a page unexpectedly asks for a login.
