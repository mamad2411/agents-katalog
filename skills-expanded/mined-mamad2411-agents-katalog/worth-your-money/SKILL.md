---
name: worth-your-money
skill_id: browser-skill:worth-your-money
description: The thing you keep almost buying, judged by people six months in
when_to_use:
  - intent_keywords: [worth it, should i buy, still good, long term review, six months later, holds up, keeps breaking]
    require_auth: false
    mutation_boundary: read_only
steps:
  - caption: what owners say six months and a year later about
    capability_target: web_search
    mutation_boundary: read_only
  - caption: what people bought instead and whether they were happier than with
    capability_target: web_search
    mutation_boundary: read_only
parameters:
  - name: the_thing
    current_value: Sony WH-1000XM5 headphones
    fill_rule: name the thing you are thinking of buying
adapter_preferences:
  preferred: browserbase
  fallback: owned_browser
  declined: []
schema_version: 1
metadata:
  luke:
    tags: [decisions, reviews, money, research, on-demand]
    related_skills: [browser-skill:worth-the-money]
platforms: [macos]
---
# Worth your money

## Purpose
The thing has been open in a tab for two weeks. Every review is from week one.
This finds the people who have lived with it since spring and says whether they
still reach for it.

## Reads
- Search results for what owners say six months and a year later about Sony WH-1000XM5 headphones.
- Search results for what people bought instead and whether they were happier than with Sony WH-1000XM5 headphones.

## Lands in
- Leads with a verdict, not a balanced summary of both sides. Short enough to act on straight away.

## Steps
1. Look up what owners say six months and a year later about Sony WH-1000XM5 headphones.
2. Look up what people bought instead and whether they were happier than with Sony WH-1000XM5 headphones.
3. Leads with a verdict, not a balanced summary of both sides.

## Success criteria
- Leads with a verdict, not a balanced summary of both sides.
- Names the specific thing that annoys owners later, and how often it comes up.
- Says whether it holds resale value, which makes a yes easier.
- Gives the price it actually sells for, and whether waiting gets a better one.

## Failure behavior
- If it is too new for long term reviews, say so and use the previous version.
- If a source will not load, skip it and keep going.

## Never
- Never sign in, buy, order or add anything to a cart.
- Never invent a price, a review, a rating or an owner quote.
- Never pass an affiliate roundup off as real owner experience.

## Redaction
Omit query strings, account details, order history, saved cards, home address,
and anything shown after a page unexpectedly asks for a login.
