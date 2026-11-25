---
name: quick-answer
skill_id: browser-skill:quick-answer
description: Settle it right now in one line, sources named, no essay
when_to_use:
  - intent_keywords: [quick answer, just tell me, one line, look it up, whats the answer, how many, when was]
    require_auth: false
    mutation_boundary: read_only
steps:
  - caption: the direct factual answer and the source that carries it for
    capability_target: web_search
    mutation_boundary: read_only
  - caption: whether that figure has changed or been corrected recently for
    capability_target: web_search
    mutation_boundary: read_only
parameters:
  - name: the_question
    current_value: how tall is the eiffel tower
    fill_rule: type the question the way you would ask a friend
adapter_preferences:
  preferred: browserbase
  fallback: owned_browser
  declined: []
schema_version: 1
metadata:
  luke:
    tags: [facts, quick, sources, phone, on-demand]
    related_skills: [browser-skill:settle-this]
platforms: [macos]
---
# Quick answer

## Purpose
The table wants the number, not the reading list. One line, the source named,
and back to the conversation.

## Reads
- Search results for the direct factual answer and the source that carries it for how tall is the eiffel tower.
- Search results for whether that figure has changed or been corrected recently for how tall is the eiffel tower.

## Lands in
- The answer fits in a text message, two or three lines at most. Short enough to act on straight away.

## Steps
1. Look up the direct factual answer and the source that carries it for how tall is the eiffel tower.
2. Look up whether that figure has changed or been corrected recently for how tall is the eiffel tower.
3. The answer fits in a text message, two or three lines at most.

## Success criteria
- The answer fits in a text message, two or three lines at most.
- Leads with the answer, never with context or caveats.
- Always names the source and how current it is, so it holds up when quoted.
- Written for someone standing up, holding a drink, with ten seconds to read.
- Says plainly when nobody actually knows, in one line, and stops there.

## Failure behavior
- If the source is paywalled, use the best public summary and label it as a
  summary.
- If the answer genuinely depends on the definition, say which definition the
  number belongs to.

## Never
- Never sign in, subscribe, pay for access or join anything.
- Never invent a number, a date, a quote or a citation.
- Never present a blog restating a source as the source.

## Redaction
Omit query strings, account details, saved cards, home address, and anything
shown after a page unexpectedly asks for a login.
