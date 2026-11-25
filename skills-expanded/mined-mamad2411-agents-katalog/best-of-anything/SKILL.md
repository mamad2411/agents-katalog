---
name: best-of-anything
skill_id: browser-skill:best-of-anything
description: The actual best one, and why, not a list of ten with links
when_to_use:
  - intent_keywords: [best, top pick, recommend, which one, what should i get, comparison]
    require_auth: false
    mutation_boundary: read_only
steps:
  - caption: independent testing, expert picks and head to head comparisons for
    capability_target: web_search
    mutation_boundary: read_only
  - caption: what people who use it every day actually recommend for
    capability_target: web_search
    mutation_boundary: read_only
parameters:
  - name: category
    current_value: best rain jacket for commuting
    fill_rule: say the category and what you need it for
adapter_preferences:
  preferred: browserbase
  fallback: owned_browser
  declined: []
schema_version: 1
metadata:
  luke:
    tags: [recommendations, shopping, research, decisions, on-demand]
    related_skills: [browser-skill:worth-the-money]
platforms: [macos]
---
# Best of anything

## Purpose
Every search for "best anything" returns ten affiliate lists with the same ten
products. This returns one pick, the reason it wins, and the one case where you
should get something else instead.

## Reads
- Search results for independent testing, expert picks and head to head comparisons for best rain jacket for commuting.
- Search results for what people who use it every day actually recommend for best rain jacket for commuting.

## Lands in
- Commits to one pick. Short enough to act on straight away.

## Steps
1. Look up independent testing, expert picks and head to head comparisons for best rain jacket for commuting.
2. Look up what people who use it every day actually recommend for best rain jacket for commuting.
3. Commits to one pick. No "it depends" as the answer.

## Success criteria
- Commits to one pick. No "it depends" as the answer.
- Says what it beats and on what dimension.
- Names the cheap option that is almost as good, since that is often the right call.
- Says when a source is paid, sponsored or affiliate driven.

## Failure behavior
- If the category genuinely splits by use case, give one pick per use case,
  maximum three.
- If nobody has tested it independently, say so and say what you are going on.
- If the top pick is out of stock everywhere, say so and lead with the runner up.

## Never
- Never sign in, buy, order or add anything to a cart.
- Never invent a test result, a price, a rating or a reviewer.
- Never rank by affiliate payout or sponsored placement.

## Redaction
Omit query strings, account details, order history, saved cards, home address,
and anything shown after a page unexpectedly asks for a login.
