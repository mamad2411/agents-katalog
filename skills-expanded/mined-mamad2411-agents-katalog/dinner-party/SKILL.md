---
name: dinner-party
skill_id: browser-skill:dinner-party
description: A menu that works together, prepped in order, with the shopping list done
when_to_use:
  - intent_keywords: [dinner party, cooking for friends, menu, having people over, hosting dinner, what to cook]
    require_auth: false
    mutation_boundary: read_only
steps:
  - caption: dinner party menus that can be mostly made ahead
    capability_target: web_search
    mutation_boundary: read_only
  - caption: recipes for six people with prep times and ingredients
    capability_target: web_search
    mutation_boundary: read_only
  - caption: what to prep the day before a dinner party
    capability_target: web_search
    mutation_boundary: read_only
parameters:
  - name: dinner
    current_value: dinner for six, no dietary restrictions
    fill_rule: say how many people, when, and anything anyone cannot eat
adapter_preferences:
  preferred: browserbase
  fallback: owned_browser
  declined: []
schema_version: 1
metadata:
  luke:
    tags: [cooking, dinner party, hosting, recipes, menu]
    related_skills: [browser-skill:party-plan, browser-skill:house-guests]
platforms: [macos]
---
# Dinner party

## Purpose
You are cooking for people. This picks a menu whose courses actually work
together, tells you what to make when, and hands you the shopping list.

## Reads
- Search results for dinner party menus that can be mostly made ahead dinner for six, no dietary restrictions.
- Search results for recipes for six people with prep times and ingredients dinner for six, no dietary restrictions.
- Search results for what to prep the day before a dinner party dinner for six, no dietary restrictions.

## Lands in
- Commits to one menu, not a set of dishes to choose between. Short enough to act on straight away.

## Steps
1. Look up dinner party menus that can be mostly made ahead dinner for six, no dietary restrictions.
2. Look up recipes for six people with prep times and ingredients dinner for six, no dietary restrictions.
3. Look up what to prep the day before a dinner party dinner for six, no dietary restrictions.
4. Commits to one menu, not a set of dishes to choose between.

## Success criteria
- Commits to one menu, not a set of dishes to choose between.
- Gives the cooking an order and times, working back from when people sit down.
- Names the first thing to do right now, usually the shop or the thing that
  needs marinating, and what can wait until the afternoon.
- Says what to buy in one list, with a rough total.
- Accounts for the constraint that actually breaks dinners: one oven, one
  stovetop, and wanting to be in the room when your guests arrive.

## Failure behavior
- If a recipe page will not load, use another for the same dish and say so.
- If a restriction rules out the menu, change the menu rather than the guest
  list.

## Never
- Never sign in to a grocery or delivery account.
- Never order groceries, book a delivery slot or buy anything.
- Never invent an ingredient price, a cook time or a recipe.

## Redaction
Omit query strings, account details, order history, saved cards, other people's
dietary or medical details, home address, and anything shown after a page
unexpectedly asks for a login.
