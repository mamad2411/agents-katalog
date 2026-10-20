---
name: one-more-thing
skill_id: browser-skill:one-more-thing
description: One small thing worth doing before the night ends
when_to_use:
  - intent_keywords: [one more thing, one more, before we go, still time, last stop, night cap, what else]
    require_auth: false
    mutation_boundary: read_only
steps:
  - caption: what is still open late tonight and worth the detour near
    capability_target: web_search
    mutation_boundary: read_only
  - caption: which of those late night spots people say is actually worth it in
    capability_target: web_search
    mutation_boundary: read_only
parameters:
  - name: still_out
    current_value: open late in Los Angeles
    fill_rule: say your city and Luke uses it instead
adapter_preferences:
  preferred: browserbase
  fallback: owned_browser
  declined: []
schema_version: 1
metadata:
  luke:
    tags: [late night, one more, nearby, phone, on-demand]
    related_skills: [browser-skill:get-me-home]
platforms: [macos]
---
# One more thing

## Purpose
The night is nearly done and there is one small window left. One thing worth
doing with it, close by, before everything shuts.

## Reads
- Search results for what is still open late tonight and worth the detour near open late in Los Angeles.
- Search results for which of those late night spots people say is actually worth it in open late in Los Angeles.

## Lands in
- The answer fits in a text message, two or three lines at most. Short enough to act on straight away.

## Steps
1. Look up what is still open late tonight and worth the detour near open late in Los Angeles.
2. Look up which of those late night spots people say is actually worth it in open late in Los Angeles.
3. The answer fits in a text message, two or three lines at most.

## Success criteria
- The answer fits in a text message, two or three lines at most.
- Leads with the thing to do, never with context or caveats.
- Always says how far it is and what time the window closes.
- Written for someone standing up, holding a drink, with ten seconds to read.
- Keeps it small, one stop, not a whole second night.

## Failure behavior
- If everything nearby is closing, say so in one line and name the one place
  that is not.
- If the window is already gone, say it plainly and suggest calling it a night.

## Never
- Never sign in, book, buy tickets or reserve anything.
- Never invent a place, a closing time or a walking distance.
- Never pass a promoted listing off as what people rate.

## Redaction
Omit query strings, account details, saved cards, exact home address, precise
live location, and anything shown after a page unexpectedly asks for a login.
