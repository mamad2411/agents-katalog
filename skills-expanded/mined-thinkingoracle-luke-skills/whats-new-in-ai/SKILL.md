---
name: whats-new-in-ai
skill_id: browser-skill:whats-new-in-ai
description: The AI news that actually matters, without the hype
when_to_use:
  - intent_keywords: [ai, models, launch, tools, research, artificial intelligence]
    require_auth: false
    mutation_boundary: read_only
steps:
  - caption: notable AI launches, models and tools released this week in
    capability_target: web_search
    mutation_boundary: read_only
  - caption: what practitioners are actually saying about the new
    capability_target: web_search
    mutation_boundary: read_only
trigger:
  kind: schedule
  recurrence: weekly
  weekday: 3
  time: 08:30
  timezone: America/Los_Angeles
  follows_device: true
parameters:
  - name: interests
    current_value: AI models and tools
    fill_rule: say which parts of AI you follow
adapter_preferences:
  preferred: browserbase
  fallback: owned_browser
  declined: []
schema_version: 1
metadata:
  luke:
    tags: [ai, models, tools, launches]
    related_skills: []
platforms: [macos]
---
# What's new in AI

## Purpose
Tuesday morning, what genuinely shipped in AI this week and what people who use it think, so the user is current without reading forty threads.

## Reads
- Search results for notable AI launches, models and tools released this week in AI models and tools.
- Search results for what practitioners are actually saying about the new AI models and tools.

## Lands in
- Leads with what shipped, not what was announced. Short enough to act on straight away.

## Steps
1. Look up notable AI launches, models and tools released this week in AI models and tools.
2. Look up what practitioners are actually saying about the new AI models and tools.
3. Leads with what shipped, not what was announced.

## Success criteria
- Leads with what shipped, not what was announced.
- Separates a launch from a demo, and a claim from a result.
- Skips the hype cycle and says so when a week is quiet.

## Failure behavior
- If a source will not load, skip it and keep going. Do not report the plumbing.
- If there is genuinely nothing, say so in one line and move on.

## Never
- Never sign in, buy, book, pre-order or join a waitlist.
- Never invent a date, a price, a venue or a review.
- Never pass an ad off as news, or a paid placement as an opinion.

## Redaction
Omit query strings, account details, order history, saved cards, home address,
and anything shown after a page unexpectedly asks for a login.
