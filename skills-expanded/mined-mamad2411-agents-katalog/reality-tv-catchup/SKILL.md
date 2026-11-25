---
name: reality-tv-catchup
skill_id: browser-skill:reality-tv-catchup
description: What happened on the shows you watch, recapped
when_to_use:
  - intent_keywords: [reality tv, recap, bravo, love island, housewives, episode, what happened]
    require_auth: false
    mutation_boundary: read_only
steps:
  - caption: episode recap and what happened on the latest season of
    capability_target: web_search
    mutation_boundary: read_only
  - caption: what viewers are saying about the latest episodes of
    capability_target: web_search
    mutation_boundary: read_only
trigger:
  kind: schedule
  recurrence: weekly
  weekday: 3
  time: 20:00
  timezone: America/Los_Angeles
  follows_device: true
parameters:
  - name: shows
    current_value: The Traitors, Love Island, Real Housewives
    fill_rule: say which shows you watch
adapter_preferences:
  preferred: browserbase
  fallback: owned_browser
  declined: []
schema_version: 1
metadata:
  luke:
    tags: [reality tv, recaps, shows, gossip]
    related_skills: []
platforms: [macos]
---
# Reality TV catchup

## Purpose
What actually went down on the shows you watch, recapped properly, so you can skip an episode and still hold the conversation.

## Reads
- Search results for episode recap and what happened on the latest season of The Traitors, Love Island, Real Housewives.
- Search results for what viewers are saying about the latest episodes of The Traitors, Love Island, Real Housewives.

## Lands in
- Recaps what happened, not what a preview promised. Short enough to act on straight away.

## Steps
1. Look up episode recap and what happened on the latest season of The Traitors, Love Island, Real Housewives.
2. Look up what viewers are saying about the latest episodes of The Traitors, Love Island, Real Housewives.
3. Recaps what happened, not what a preview promised.

## Success criteria
- Recaps what happened, not what a preview promised.
- Names who did what, so the conversation makes sense.
- Flags the moment everyone is going to bring up.
- Never spoils further ahead than the user asked.

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
