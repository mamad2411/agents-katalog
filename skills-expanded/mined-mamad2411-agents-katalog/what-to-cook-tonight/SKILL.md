---
name: what-to-cook-tonight
skill_id: browser-skill:what-to-cook-tonight
description: Dinner in about twenty minutes from what is already in the kitchen
when_to_use:
  - intent_keywords: [what to cook, dinner, recipe, quick meal, whats for dinner, easy dinner]
    require_auth: false
    mutation_boundary: read_only
steps:
  - caption: twenty minute dinner recipes using
    capability_target: web_search
    mutation_boundary: read_only
  - caption: fast weeknight dinners people rate highly with
    capability_target: web_search
    mutation_boundary: read_only
trigger:
  kind: schedule
  recurrence: daily
  time: 17:15
  timezone: America/Los_Angeles
  follows_device: true
parameters:
  - name: kitchen
    current_value: eggs, rice, pasta, garlic, onions and chicken
    fill_rule: list what you usually have in and anything you do not eat
adapter_preferences:
  preferred: browserbase
  fallback: owned_browser
  declined: []
schema_version: 1
metadata:
  luke:
    tags: [food, dinner, recipes, daily, quick]
    related_skills: [browser-skill:good-food-near-you]
platforms: [macos]
---
# What to cook tonight

## Purpose
Late afternoon, one dinner you can actually make tonight from what is already in the kitchen. You cook something good and you are eating in twenty minutes.

## Reads
- Search results for twenty minute dinner recipes using eggs, rice, pasta, garlic, onions and chicken.
- Search results for fast weeknight dinners people rate highly with eggs, rice, pasta, garlic, onions and chicken.

## Lands in
- One dinner, not a menu. Short enough to act on straight away.

## Steps
1. Look up twenty minute dinner recipes using eggs, rice, pasta, garlic, onions and chicken.
2. Look up fast weeknight dinners people rate highly with eggs, rice, pasta, garlic, onions and chicken.
3. One dinner, not a menu. Twenty minutes or close to it.

## Success criteria
- One dinner, not a menu. Twenty minutes or close to it.
- Names every ingredient it needs beyond what the user already has.
- Respects anything the user does not eat.
- Gives the steps in order, short enough to follow while cooking.

## Failure behavior
- If a recipe page will not load, skip it and keep going.
- If nothing fits the kitchen, say so and name the one thing worth picking up.

## Never
- Never sign in, order groceries, buy or join a waitlist.
- Never invent a cook time, a quantity, a rating or a temperature.
- Nothing cruel. No comments about what the user eats.

## Redaction
Omit query strings, account details, order history, saved cards, home address,
and anything shown after a page unexpectedly asks for a login.
