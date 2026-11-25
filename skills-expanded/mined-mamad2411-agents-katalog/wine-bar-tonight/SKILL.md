---
name: wine-bar-tonight
skill_id: browser-skill:wine-bar-tonight
description: A wine bar with seats free, and what to order off the glass list
when_to_use:
  - intent_keywords: [wine bar, natural wine, glass of wine, low abv, non alcoholic, drinks tonight]
    require_auth: false
    mutation_boundary: read_only
steps:
  - caption: natural wine bars and by the glass lists worth going to in
    capability_target: web_search
    mutation_boundary: read_only
  - caption: which wine bars take walk ins and what is pouring this week in
    capability_target: web_search
    mutation_boundary: read_only
trigger:
  kind: schedule
  recurrence: weekly
  weekday: 6
  time: 17:15
  timezone: America/Los_Angeles
  follows_device: true
parameters:
  - name: drinks
    current_value: Los Angeles
    fill_rule: say your city and Luke uses it instead
adapter_preferences:
  preferred: browserbase
  fallback: owned_browser
  declined: []
schema_version: 1
metadata:
  luke:
    tags: [wine bar, natural wine, drinks, low abv, walk in]
    related_skills: [browser-skill:happy-hour, browser-skill:table-tonight]
platforms: [macos]
---
# Wine bar tonight

## Purpose
Friday evening, a wine bar you can actually get into and one thing to order
when you sit down. Not a list of bars. A seat, a pour and a reason.

## Reads
- Search results for natural wine bars and by the glass lists worth going to in Los Angeles.
- Search results for which wine bars take walk ins and what is pouring this week in Los Angeles.

## Lands in
- Leads with walk in access, because most good wine bars keep the counter first come first served on purpose and simply do not put those seats on any app. Short enough to act on straight away.

## Steps
1. Look up natural wine bars and by the glass lists worth going to in Los Angeles.
2. Look up which wine bars take walk ins and what is pouring this week in Los Angeles.
3. Leads with walk in access, because most good wine bars keep the counter first come first served on purpose and simply do not put those seats on any app. Arriving near open, usually around 5 or 5:30, is the difference between sitting down straight away and standing for an hour.

## Success criteria
- Leads with walk in access, because most good wine bars keep the counter first
  come first served on purpose and simply do not put those seats on any app.
  Arriving near open, usually around 5 or 5:30, is the difference between
  sitting down straight away and standing for an hour.
- Treats the by the glass list as the live thing it is. Serious lists rotate
  every week or two around whatever just landed, so the useful answer is what is
  open this week, not what the bar is famous for.
- Gives you the sentence to say. Naming a style and a price range to the person
  behind the counter gets you a better glass than reading the list ever will,
  and it is how these places prefer to work.
- Covers not drinking without making it a lesser option. Low alcohol pours and
  proper zero proof lists are standard now rather than an afterthought, so name
  the actual drink, not "they have mocktails."
- Says whether there is real food, since many of these rooms serve small plates
  only and that changes whether it is dinner or the thing before dinner.

## Failure behavior
- If a glass list is not posted, say what the bar generally pours and label it
  as general rather than tonight.
- If the first pick is likely packed, name the closest alternative and the walk
  between them.

## Never
- Never sign in, book a table, join a waitlist or buy anything.
- Never invent a wine, a producer, a price or a pour.
- Never push drinking on someone who said they are not drinking tonight.

## Redaction
Omit query strings, account details, order history, saved cards, home address,
and anything shown after a page unexpectedly asks for a login.
