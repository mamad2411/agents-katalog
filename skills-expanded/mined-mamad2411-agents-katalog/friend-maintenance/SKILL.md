---
name: friend-maintenance
skill_id: browser-skill:friend-maintenance
description: Who you have not seen in too long, and a specific plan to fix it
when_to_use:
  - intent_keywords: [friends, catch up, havent seen, make a plan, hang out, reconnect, see people]
    require_auth: false
    mutation_boundary: read_only
steps:
  - caption: easy low key places to actually sit and talk in
    capability_target: web_search
    mutation_boundary: read_only
  - caption: what is on this weekend that two or three people could just turn up to in
    capability_target: web_search
    mutation_boundary: read_only
trigger:
  kind: schedule
  recurrence: weekly
  weekday: 5
  time: 17:15
  timezone: America/Los_Angeles
  follows_device: true
parameters:
  - name: your_people
    current_value: Los Angeles
    fill_rule: say your city and Luke uses it instead
adapter_preferences:
  preferred: browserbase
  fallback: owned_browser
  declined: []
schema_version: 1
metadata:
  luke:
    tags: [friends, plans, weekly, social, catch up]
    related_skills: [browser-skill:out-this-weekend]
platforms: [macos]
---
# Friend maintenance

## Purpose
Thursday evening, while the weekend is still open. One person the user has been
meaning to see, and a plan specific enough to send as a text tonight.

## Reads
- Search results for easy low key places to actually sit and talk in Los Angeles.
- Search results for what is on this weekend that two or three people could just turn up to in Los Angeles.

## Lands in
- Names one person, not a list to feel guilty about. Short enough to act on straight away.

## Steps
1. Look up easy low key places to actually sit and talk in Los Angeles.
2. Look up what is on this weekend that two or three people could just turn up to in Los Angeles.
3. Names one person, not a list to feel guilty about.

## Success criteria
- Names one person, not a list to feel guilty about.
- Gives a real place and a real time, so the text needs no follow up to be useful.
- Matches the plan to the friendship: coffee for some, a whole night for others.
- Writes the message in the user's voice, short enough to send unedited.

## Failure behavior
- If a listing will not load, skip it and keep going.
- If the weekend is packed, say so and suggest a weeknight that is actually free.

## Never
- Never send, post or schedule anything. The user hits send, not Luke.
- Never invent a place, an opening time or an event.
- Never read a private message thread or contact list to guess who to name.

## Redaction
Omit query strings, account details, phone numbers, home address, and anything
shown after a page unexpectedly asks for a login.
