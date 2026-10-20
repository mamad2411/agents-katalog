---
name: whats-everyone-posting
skill_id: browser-skill:whats-everyone-posting
description: The thing everyone will be posting about today
when_to_use:
  - intent_keywords: [meme, funny, viral, trending, group chat, whats everyone talking about]
    require_auth: false
    mutation_boundary: read_only
steps:
  - caption: the clip, meme or moment everyone is posting today about
    capability_target: web_search
    mutation_boundary: read_only
  - caption: what people cannot stop sharing right now about
    capability_target: web_search
    mutation_boundary: read_only
trigger:
  kind: schedule
  recurrence: daily
  time: 12:30
  timezone: America/Los_Angeles
  follows_device: true
parameters:
  - name: humor
    current_value: whats going viral today
    fill_rule: say what you find funny and Luke tunes it
adapter_preferences:
  preferred: browserbase
  fallback: owned_browser
  declined: []
schema_version: 1
metadata:
  luke:
    tags: [memes, viral, funny, daily, culture]
    related_skills: []
platforms: [macos]
---
# Group chat fuel

## Purpose
Late morning, the one thing the internet is on today. So you send it first instead of getting sent it.

## Reads
- Search results for the clip, meme or moment everyone is posting today about whats going viral today.
- Search results for what people cannot stop sharing right now about whats going viral today.

## Lands in
- One thing. Short enough to act on straight away.

## Steps
1. Look up the clip, meme or moment everyone is posting today about whats going viral today.
2. Look up what people cannot stop sharing right now about whats going viral today.
3. One thing. The actual funniest or most surprising, not the biggest.

## Success criteria
- One thing. The actual funniest or most surprising, not the biggest.
- Says what it is in a line, without ruining it.
- Nothing mean, nothing tragic. This one is only for the good stuff.

## Failure behavior
- If a source will not load, skip it and keep going.
- If there is genuinely nothing, say so in one line and move on.

## Never
- Never sign in, buy, book or join a waitlist.
- Never invent a date, a price, a name or a result.
- Never pass a sponsored post off as what people are sharing.

## Redaction
Omit query strings, account details, order history, saved cards, home address,
and anything shown after a page unexpectedly asks for a login.
