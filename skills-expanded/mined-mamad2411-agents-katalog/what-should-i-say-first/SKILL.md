---
name: what-should-i-say-first
skill_id: browser-skill:what-should-i-say-first
description: Something actually good to say, tuned to who you are talking to
when_to_use:
  - intent_keywords: [opener, pickup line, first message, dating app, what do i say, text back]
    require_auth: false
    mutation_boundary: read_only
steps:
  - caption: what actually works as an opener right now according to people who date in
    capability_target: web_search
    mutation_boundary: read_only
  - caption: what people say makes them reply, and what makes them not, in
    capability_target: web_search
    mutation_boundary: read_only
trigger:
  kind: schedule
  recurrence: weekly
  weekday: 6
  time: 20:00
  timezone: America/Los_Angeles
  follows_device: true
parameters:
  - name: vibe
    current_value: funny and low key confident
    fill_rule: say your vibe and Luke writes to it
adapter_preferences:
  preferred: browserbase
  fallback: owned_browser
  declined: []
schema_version: 1
metadata:
  luke:
    tags: [dating, openers, confidence, social]
    related_skills: [browser-skill:make-me-a-meme]
platforms: [macos]
---

# Opening line

## Purpose
Friday evening, three openers that sound like a person and not a script, tuned to how you actually talk.

## Reads
- Search results for what actually works as an opener right now according to people who date in funny and low key confident.
- Search results for what people say makes them reply, and what makes them not, in funny and low key confident.

## Lands in
- Writes three, each a different angle: funny, curious, direct. Short enough to act on straight away.

## Steps
1. Look up what actually works as an opener right now according to people who date in funny and low key confident.
2. Look up what people say makes them reply, and what makes them not, in funny and low key confident.
3. Writes three, each a different angle: funny, curious, direct.

## Success criteria
- Writes three, each a different angle: funny, curious, direct.
- Sounds like something the user would actually say out loud.
- Gives one line on why each works.
- Specific beats clever. Never a rhyming couplet.

## Failure behavior
- If it is a quiet day, say so and give the best evergreen instead.

## Never
- Never sign in, message anyone, or open a dating app.
- Never write anything that negs, pressures or manipulates.
- Never invent a fact about the person being messaged.

## Redaction
Omit query strings, account details, handles and names the user has not
mentioned, message history, and anything shown after a page unexpectedly asks
for a login.
