---
name: birthday-plan
skill_id: browser-skill:birthday-plan
description: Their birthday, planned properly, cake and surprise logistics included
when_to_use:
  - intent_keywords: [birthday, surprise party, cake, celebrate, turning 30, birthday dinner]
    require_auth: false
    mutation_boundary: read_only
steps:
  - caption: best places for a birthday dinner or drinks for a group in
    capability_target: web_search
    mutation_boundary: read_only
  - caption: bakeries taking custom cake orders and how much notice they need
    capability_target: web_search
    mutation_boundary: read_only
  - caption: how to run a surprise party without it getting out
    capability_target: web_search
    mutation_boundary: read_only
parameters:
  - name: birthday
    current_value: birthday dinner for 12 people in Los Angeles
    fill_rule: say your city and Luke uses it instead
adapter_preferences:
  preferred: browserbase
  fallback: owned_browser
  declined: []
schema_version: 1
metadata:
  luke:
    tags: [birthday, party, cake, hosting, planning]
    related_skills: [browser-skill:party-plan, browser-skill:dinner-party]
platforms: [macos]
---
# Birthday plan

## Purpose
Someone's birthday is coming and you are the one who cares enough to sort it.
One plan: where, who, the cake, and how the surprise actually works.

## Reads
- Search results for best places for a birthday dinner or drinks for a group in birthday dinner for 12 people in Los Angeles.
- Search results for bakeries taking custom cake orders and how much notice they need birthday dinner for 12 people in Los Angeles.
- Search results for how to run a surprise party without it getting out birthday dinner for 12 people in Los Angeles.

## Lands in
- Commits to one plan with one place and one time, not a set of candidates. Short enough to act on straight away.

## Steps
1. Look up best places for a birthday dinner or drinks for a group in birthday dinner for 12 people in Los Angeles.
2. Look up bakeries taking custom cake orders and how much notice they need birthday dinner for 12 people in Los Angeles.
3. Look up how to run a surprise party without it getting out birthday dinner for 12 people in Los Angeles.
4. Commits to one plan with one place and one time, not a set of candidates.

## Success criteria
- Commits to one plan with one place and one time, not a set of candidates.
- Gives the evening an order and times, including when people arrive versus
  when the birthday person does.
- Names the first thing to do right now, usually the group booking or the cake
  order, and what can wait until the week of.
- Says what to buy or order, with rough cost, cake included.
- Accounts for the constraint that actually breaks birthdays: cake lead time,
  a restaurant that will not seat a group, or getting the person there without
  telling them why.

## Failure behavior
- If a venue page will not load, skip it and keep going.
- If nothing takes the group that night, keep the date and move it to a home
  dinner or drinks, and say why.

## Never
- Never sign in to a booking, delivery or shopping account.
- Never book, reserve, order a cake or buy anything.
- Never invent a price, a bakery, a venue or a lead time.

## Redaction
Omit query strings, account details, order history, saved cards, other people's
contact details, home address, and anything shown after a page unexpectedly
asks for a login.
