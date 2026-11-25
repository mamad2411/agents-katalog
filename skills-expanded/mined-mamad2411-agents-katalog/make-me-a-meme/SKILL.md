---
name: make-me-a-meme
skill_id: browser-skill:make-me-a-meme
description: Today's format, and your version of it ready to send
when_to_use:
  - intent_keywords: [meme, make a meme, format, caption, joke, post, funny]
    require_auth: false
    mutation_boundary: read_only
steps:
  - caption: the meme format everyone is using right now and how it works
    capability_target: web_search
    mutation_boundary: read_only
  - caption: the best examples people are posting today of
    capability_target: web_search
    mutation_boundary: read_only
trigger:
  kind: schedule
  recurrence: daily
  time: 12:30
  timezone: America/Los_Angeles
  follows_device: true
parameters:
  - name: your_world
    current_value: trending meme formats
    fill_rule: say what your jokes are usually about and Luke writes to that
adapter_preferences:
  preferred: browserbase
  fallback: owned_browser
  declined: []
schema_version: 1
metadata:
  luke:
    tags: [memes, jokes, formats, daily, culture]
    related_skills: [browser-skill:whats-everyone-posting]
platforms: [macos]
---

# Meme machine

## Purpose
Half twelve, the format everyone is using today, plus three captions
written for your life. You post yours while the format is still funny.

## Reads
- Search results for the meme format everyone is using right now and how it works trending meme formats.
- Search results for the best examples people are posting today of trending meme formats.

## Lands in
- Explains the format so it makes sense even if you missed it. Short enough to act on straight away.

## Steps
1. Look up the meme format everyone is using right now and how it works trending meme formats.
2. Look up the best examples people are posting today of trending meme formats.
3. Explains the format so it makes sense even if you missed it.

## Success criteria
- Explains the format so it makes sense even if you missed it.
- Writes three captions, specific to the user, not generic filler.
- Says how long the format has been running, so nobody posts a dead one.
- Picks funny over popular when they differ.

## Failure behavior
- If nothing is really landing today, say so and give yesterday's best.

## Never
- Never sign in, post, upload or share anything. The user sends it, not Luke.
- Never invent a format that is not actually going around.
- Never punch down, and never build a joke on someone's misfortune.

## Redaction
Omit query strings, account details, handles the user has not mentioned, and
anything shown after a page unexpectedly asks for a login.
