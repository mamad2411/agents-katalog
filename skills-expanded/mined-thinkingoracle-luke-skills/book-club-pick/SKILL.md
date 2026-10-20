---
name: book-club-pick
skill_id: browser-skill:book-club-pick
description: The next book, and something smart to say about it
when_to_use:
  - intent_keywords: [book club, next book, reading, what to read, discussion]
    require_auth: false
    mutation_boundary: read_only
steps:
  - caption: most discussed and best reviewed recent books in
    capability_target: web_search
    mutation_boundary: read_only
  - caption: what book clubs are debating and disagreeing about in
    capability_target: web_search
    mutation_boundary: read_only
trigger:
  kind: schedule
  recurrence: weekly
  weekday: 1
  time: 17:15
  timezone: America/Los_Angeles
  follows_device: true
parameters:
  - name: taste
    current_value: literary fiction and memoir
    fill_rule: say what your club likes reading
adapter_preferences:
  preferred: browserbase
  fallback: owned_browser
  declined: []
schema_version: 1
metadata:
  luke:
    tags: [books, book club, reading, discussion]
    related_skills: []
platforms: [macos]
---
# Book club pick

## Purpose
The next book worth the group's time, plus the thing people actually argue about in it, so you arrive with an opinion.

## Reads
- Search results for most discussed and best reviewed recent books in literary fiction and memoir.
- Search results for what book clubs are debating and disagreeing about in literary fiction and memoir.

## Lands in
- One pick, with page count and roughly how long it takes. Short enough to act on straight away.

## Steps
1. Look up most discussed and best reviewed recent books in literary fiction and memoir.
2. Look up what book clubs are debating and disagreeing about in literary fiction and memoir.
3. One pick, with page count and roughly how long it takes.

## Success criteria
- One pick, with page count and roughly how long it takes.
- Names the argument the book starts, which is the whole point of a club.
- Says who will hate it and why, honestly.
- Never spoils past the first act.

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
