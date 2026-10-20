---
name: skin-actually
skill_id: browser-skill:skin-actually
description: What is actually worth trying in the ingredients you are curious about
when_to_use:
  - intent_keywords: [skincare, retinol, tret, niacinamide, snail mucin, barrier, slugging, glow]
    require_auth: false
    mutation_boundary: read_only
steps:
  - caption: what people are seeing results with this month using
    capability_target: web_search
    mutation_boundary: read_only
  - caption: what actually works and what is just marketing for
    capability_target: web_search
    mutation_boundary: read_only
trigger:
  kind: schedule
  recurrence: weekly
  weekday: 1
  time: 20:00
  timezone: America/Los_Angeles
  follows_device: true
parameters:
  - name: curious_about
    current_value: retinol, niacinamide and hyaluronic acid
    fill_rule: say which ingredients you are curious about
adapter_preferences:
  preferred: browserbase
  fallback: owned_browser
  declined: []
schema_version: 1
metadata:
  luke:
    tags: [skincare, ingredients, peptides, routines, discovery]
    related_skills: [browser-skill:new-this-week]
platforms: [macos]
---

# Skin, actually

## Purpose
Sunday evening, what's actually worth trying out of everything you've been curious about, and what's just a nice bottle.

## Reads
- Search results for what people are seeing results with this month using retinol, niacinamide and hyaluronic acid.
- Search results for what actually works and what is just marketing for retinol, niacinamide and hyaluronic acid.

## Lands in
- Explains it the way a knowledgeable friend would, not a product page. Short enough to act on straight away.

## Steps
1. Look up what people are seeing results with this month using retinol, niacinamide and hyaluronic acid.
2. Look up what actually works and what is just marketing for retinol, niacinamide and hyaluronic acid.
3. Explains it the way a knowledgeable friend would, not a product page.

## Success criteria
- Explains it the way a knowledgeable friend would, not a product page.
- Separates what people report from what is established.
- Mentions what not to layer it with, and if something can burn or peel says so once, in the same breath as how to use it.
- Says plainly when something is mostly hype.

## Failure behavior
- If a source will not load, skip it and keep going.
- If there is nothing new on an ingredient, say so and move to the next.

## Never
- Never sign in, buy, or add anything to a basket.
- Never give a dose, a prescription, or a personal treatment plan.
- Never present a brand's own claim as an independent result.

## Redaction
Omit query strings, order history, account details, saved cards, and anything
shown after a page unexpectedly asks for a login.
