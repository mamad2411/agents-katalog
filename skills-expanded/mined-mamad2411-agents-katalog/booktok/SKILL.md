---
name: booktok
skill_id: browser-skill:booktok
description: What people are actually reading right now, and which one to start
when_to_use:
  - intent_keywords: [book, reading, booktok, what should i read, novel, book recommendation, tbr]
    require_auth: false
    mutation_boundary: read_only
steps:
  - caption: the books people are actually reading and posting about right now in
    capability_target: web_search
    mutation_boundary: read_only
  - caption: honest reader reactions, length and whether it holds up for
    capability_target: web_search
    mutation_boundary: read_only
trigger:
  kind: schedule
  recurrence: weekly
  weekday: 1
  time: 08:30
  timezone: America/Los_Angeles
  follows_device: true
parameters:
  - name: taste
    current_value: books everyone is reading right now
    fill_rule: say the last book you loved and Luke reads out from there
adapter_preferences:
  preferred: browserbase
  fallback: owned_browser
  declined: []
schema_version: 1
metadata:
  luke:
    tags: [books, reading, culture, weekly, recommendations]
    related_skills: [browser-skill:new-obsession]
platforms: [macos]
---
# BookTok

## Purpose
Sunday morning, with actual time to start something. One book people are really
reading this week, picked to match what the user already loves, with an honest
line on whether it earns the hours.

## Reads
- Search results for the books people are actually reading and posting about right now in books everyone is reading right now.
- Search results for honest reader reactions, length and whether it holds up for books everyone is reading right now.

## Lands in
- Names one book with its author, and says what it is without spoiling it. Short enough to act on straight away.

## Steps
1. Look up the books people are actually reading and posting about right now in books everyone is reading right now.
2. Look up honest reader reactions, length and whether it holds up for books everyone is reading right now.
3. Names one book with its author, and says what it is without spoiling it.

## Success criteria
- Names one book with its author, and says what it is without spoiling it.
- Gives the page count and an honest read on the pace.
- Separates a publisher push from readers actually loving it, and says which.
- Offers one shorter alternative for a week with no time in it.

## Failure behavior
- If a source will not load, skip it and keep going.
- If nothing new fits the user's taste, say so and name an older book they
  probably missed.

## Never
- Never sign in, buy, preorder or add anything to a cart.
- Never invent a title, an author, a rating or a reader quote.
- Never pass sponsored or gifted coverage off as a real reader reaction.

## Redaction
Omit query strings, account details, order history, saved cards, home address,
and anything shown after a page unexpectedly asks for a login.
