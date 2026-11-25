---
name: what-do-i-say
skill_id: browser-skill:what-do-i-say
description: You are mid conversation and stuck, here is something good to say next
when_to_use:
  - intent_keywords: [what do i say, stuck, conversation, small talk, what to ask, awkward, keep it going]
    require_auth: false
    mutation_boundary: read_only
steps:
  - caption: what is genuinely going on right now worth talking about in
    capability_target: web_search
    mutation_boundary: read_only
  - caption: good questions people actually enjoy being asked about
    capability_target: web_search
    mutation_boundary: read_only
parameters:
  - name: the_topic
    current_value: current events and culture
    fill_rule: say who you are talking to and what you already covered
adapter_preferences:
  preferred: browserbase
  fallback: owned_browser
  declined: []
schema_version: 1
metadata:
  luke:
    tags: [conversation, social, prompts, phone, on-demand]
    related_skills: [browser-skill:quick-answer]
platforms: [macos]
---
# What do I say

## Purpose
The conversation stalled and you are both looking at your drinks. One thing to
say that opens it back up.

## Reads
- Search results for what is genuinely going on right now worth talking about in current events and culture.
- Search results for good questions people actually enjoy being asked about current events and culture.

## Lands in
- The answer fits in a text message, two or three lines at most. Short enough to act on straight away.

## Steps
1. Look up what is genuinely going on right now worth talking about in current events and culture.
2. Look up good questions people actually enjoy being asked about current events and culture.
3. The answer fits in a text message, two or three lines at most.

## Success criteria
- The answer fits in a text message, two or three lines at most.
- Leads with the line to say, never with context or caveats.
- Always gives the one detail that makes the line land, a name, a number or a
  when.
- Written for someone standing up, holding a drink, with ten seconds to read.
- Sounds like the user, not like a script read aloud.

## Failure behavior
- If the subject is thin, pivot to a nearby subject and say which way it turned.
- If the situation reads as sensitive, keep it light and offer a way out of the
  topic instead of deeper into it.

## Never
- Never sign in, message anyone, post or send anything on the user's behalf.
- Never invent a fact, a quote or a story for the user to repeat.
- Never coach the user to mislead, pressure or manipulate the person they are
  talking to.

## Redaction
Omit query strings, account details, other people's names and handles the user
has not mentioned, home address, and anything shown after a page unexpectedly
asks for a login.
