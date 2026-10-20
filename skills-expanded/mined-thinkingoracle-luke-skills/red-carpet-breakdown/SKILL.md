---
name: red-carpet-breakdown
skill_id: browser-skill:red-carpet-breakdown
description: Who wore what, who styled it, and what it cost
when_to_use:
  - intent_keywords: [red carpet, outfit, met gala, awards, styling, look, dress]
    require_auth: false
    mutation_boundary: read_only
steps:
  - caption: best and most talked about looks, designers and stylists at
    capability_target: web_search
    mutation_boundary: read_only
  - caption: what fashion critics said about the standout looks at
    capability_target: web_search
    mutation_boundary: read_only
trigger:
  kind: schedule
  recurrence: weekly
  weekday: 2
  time: 12:30
  timezone: America/Los_Angeles
  follows_device: true
parameters:
  - name: event
    current_value: the Met Gala and awards season
    fill_rule: say which events you want covered
adapter_preferences:
  preferred: browserbase
  fallback: owned_browser
  declined: []
schema_version: 1
metadata:
  luke:
    tags: [fashion, red carpet, styling, culture]
    related_skills: []
platforms: [macos]
---
# Red carpet breakdown

## Purpose
Who wore what, who put it together, and why it worked. The whole conversation, sourced, without scrolling twenty carousels.

## Reads
- Search results for best and most talked about looks, designers and stylists at the Met Gala and awards season.
- Search results for what fashion critics said about the standout looks at the Met Gala and awards season.

## Lands in
- Names the designer and the stylist, not just the celebrity. Short enough to act on straight away.

## Steps
1. Look up best and most talked about looks, designers and stylists at the Met Gala and awards season.
2. Look up what fashion critics said about the standout looks at the Met Gala and awards season.
3. Names the designer and the stylist, not just the celebrity.

## Success criteria
- Names the designer and the stylist, not just the celebrity.
- Says what made a look land or fail, in specific terms.
- Includes the one nobody is talking about that deserved more.
- Never comments on anyone's body.

## Failure behavior
- If a source will not load, skip it and keep going.
- If there is genuinely nothing, say so in one line and move on.

## Never
- Never sign in, buy, post or share on the user's behalf.
- Never invent a quote, a name, a designer or a price.
- Never say anything cruel about a person's body or private life.

## Redaction
Omit query strings, account details, order history, saved cards, home address,
and anything shown after a page unexpectedly asks for a login.
