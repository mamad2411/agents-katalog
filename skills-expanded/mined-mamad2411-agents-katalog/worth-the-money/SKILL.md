---
name: worth-the-money
skill_id: browser-skill:worth-the-money
description: Whether the thing is actually good, from people who owned it six months
when_to_use:
  - intent_keywords: [worth it, should i buy, is it good, review, reviews, long term, hold up]
    require_auth: false
    mutation_boundary: read_only
steps:
  - caption: long term owner reviews and common complaints after six months of
    capability_target: web_search
    mutation_boundary: read_only
  - caption: what people say broke, wore out or annoyed them about
    capability_target: web_search
    mutation_boundary: read_only
  - caption: the cheaper and better alternatives people switched to instead of
    capability_target: web_search
    mutation_boundary: read_only
parameters:
  - name: the_thing
    current_value: best noise cancelling headphones
    fill_rule: name the exact thing you are thinking about buying
adapter_preferences:
  preferred: browserbase
  fallback: owned_browser
  declined: []
schema_version: 1
metadata:
  luke:
    tags: [shopping, reviews, research, decisions, on-demand]
    related_skills: [browser-skill:best-of-anything]
platforms: [macos]
---
# Worth the money

## Purpose
You are about to spend real money and every review you can find is from week
one. This goes and finds the people who have owned it for six months and says
what they think now.

## Reads
- Search results for long term owner reviews and common complaints after six months of best noise cancelling headphones.
- Search results for what people say broke, wore out or annoyed them about best noise cancelling headphones.
- Search results for the cheaper and better alternatives people switched to instead of best noise cancelling headphones.

## Lands in
- Leads with a verdict, not a summary of both sides. Short enough to act on straight away.

## Steps
1. Look up long term owner reviews and common complaints after six months of best noise cancelling headphones.
2. Look up what people say broke, wore out or annoyed them about best noise cancelling headphones.
3. Look up the cheaper and better alternatives people switched to instead of best noise cancelling headphones.
4. Leads with a verdict, not a summary of both sides.

## Success criteria
- Leads with a verdict, not a summary of both sides.
- Names the specific failure people report, with how common it is.
- Separates paid and affiliate coverage from real owners, and says which is which.
- Gives the price it actually sells for, not the list price.

## Failure behavior
- If the thing is too new for long term reviews, say so and give the closest
  previous model instead.
- If a source will not load, skip it and keep going.

## Never
- Never sign in, buy, order or add anything to a cart.
- Never invent a price, a review, a rating or an owner quote.
- Never pass an affiliate roundup off as owner experience.

## Redaction
Omit query strings, account details, order history, saved cards, home address,
and anything shown after a page unexpectedly asks for a login.
