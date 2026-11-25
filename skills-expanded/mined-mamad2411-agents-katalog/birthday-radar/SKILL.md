---
name: birthday-radar
skill_id: browser-skill:birthday-radar
description: Whose birthday is coming up and one good gift idea for them
when_to_use:
  - intent_keywords: [birthday, gift, present, gift idea, whose birthday, anniversary]
    require_auth: false
    mutation_boundary: read_only
steps:
  - caption: birthday gift ideas people actually loved this year for
    capability_target: web_search
    mutation_boundary: read_only
  - caption: well reviewed gift guides and picks for
    capability_target: web_search
    mutation_boundary: read_only
trigger:
  kind: schedule
  recurrence: weekly
  weekday: 2
  time: 08:30
  timezone: America/Los_Angeles
  follows_device: true
parameters:
  - name: gift_taste
    current_value: coffee gear, books, small design objects
    fill_rule: say the kinds of gifts you give
adapter_preferences:
  preferred: browserbase
  fallback: owned_browser
  declined: []
schema_version: 1
metadata:
  luke:
    tags: [birthdays, gifts, people, weekly, thoughtful]
    related_skills: []
platforms: [macos]
---
# Birthday radar

## Purpose
Monday morning, whose birthday is coming and one gift that fits them. You show up with the right thing and enough time to get it there.

## Reads
- Search results for birthday gift ideas people actually loved this year for coffee gear, books, small design objects.
- Search results for well reviewed gift guides and picks for coffee gear, books, small design objects.

## Lands in
- Names the person and the date, so the lead time is obvious. Short enough to act on straight away.

## Steps
1. Look up birthday gift ideas people actually loved this year for coffee gear, books, small design objects.
2. Look up well reviewed gift guides and picks for coffee gear, books, small design objects.
3. Names the person and the date, so the lead time is obvious.

## Success criteria
- Names the person and the date, so the lead time is obvious.
- One gift each, chosen for that person, not a generic list.
- Gives a rough price and where it is sold.
- Nobody coming up means one line saying the month is clear.

## Failure behavior
- If a source will not load, skip it and keep going.
- If a price cannot be confirmed, say the price is unclear rather than guessing.

## Never
- Never sign in, buy, order or join a waitlist.
- Never invent a price, a name, a date or a stock claim.
- Nothing cruel. No jokes at the birthday person's expense.

## Redaction
Omit query strings, account details, order history, saved cards, home address,
and anything shown after a page unexpectedly asks for a login.
