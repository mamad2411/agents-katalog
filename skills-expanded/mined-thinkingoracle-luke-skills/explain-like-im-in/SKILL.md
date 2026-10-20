---
name: explain-like-im-in
skill_id: browser-skill:explain-like-im-in
description: Up to speed on a topic in time for dinner tonight
when_to_use:
  - intent_keywords: [explain, catch me up, get up to speed, what is, primer, basics, brief me]
    require_auth: false
    mutation_boundary: read_only
steps:
  - caption: the plain explanation, the key terms and the current state of
    capability_target: web_search
    mutation_boundary: read_only
  - caption: what changed recently and what people who follow it are arguing about in
    capability_target: web_search
    mutation_boundary: read_only
parameters:
  - name: topic
    current_value: tariffs
    fill_rule: name the topic you need to be able to talk about
adapter_preferences:
  preferred: browserbase
  fallback: owned_browser
  declined: []
schema_version: 1
metadata:
  luke:
    tags: [learning, primer, research, conversation, on-demand]
    related_skills: [browser-skill:settle-this]
platforms: [macos]
---
# Explain like I am in

## Purpose
There is a dinner tonight and a topic you cannot hold a conversation about.
This gets you to competent, fast: what it is, what changed, and what the people
who follow it are actually arguing about.

## Reads
- Search results for the plain explanation, the key terms and the current state of tariffs.
- Search results for what changed recently and what people who follow it are arguing about in tariffs.

## Lands in
- Explains it without jargon, then gives the jargon so you recognize it. Short enough to act on straight away.

## Steps
1. Look up the plain explanation, the key terms and the current state of tariffs.
2. Look up what changed recently and what people who follow it are arguing about in tariffs.
3. Explains it without jargon, then gives the jargon so you recognize it.

## Success criteria
- Explains it without jargon, then gives the jargon so you recognize it.
- Says what changed in the last few months, with dates.
- Gives you two or three things you could actually say that are not obvious.
- Distinguishes settled fact from live argument.

## Failure behavior
- If the topic is too broad to cover, narrow it to the part that is live now
  and say that is what you did.
- If a source will not load, skip it and keep going.

## Never
- Never sign in, subscribe or pay for access to read something.
- Never invent a fact, a date, a number or an expert.
- Never present one side's framing as the neutral account.

## Redaction
Omit query strings, account details, saved cards, home address, and anything
shown after a page unexpectedly asks for a login.
