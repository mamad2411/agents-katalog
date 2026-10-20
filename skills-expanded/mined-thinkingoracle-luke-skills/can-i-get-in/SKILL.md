---
name: can-i-get-in
skill_id: browser-skill:can-i-get-in
description: The entry rules that stop people at the gate, checked before you book
when_to_use:
  - intent_keywords: [visa, entry requirements, passport, ETIAS, ESTA, do I need a visa, border]
    require_auth: false
    mutation_boundary: read_only
steps:
  - caption: current entry requirements and passport rules for visitors to
    capability_target: web_search
    mutation_boundary: read_only
  - caption: recent changes to travel authorization and border systems for
    capability_target: web_search
    mutation_boundary: read_only
parameters:
  - name: destination
    current_value: entry requirements for Americans visiting Europe
    fill_rule: say where you are going and which passport you hold
adapter_preferences:
  preferred: browserbase
  fallback: owned_browser
  declined: []
schema_version: 1
metadata:
  luke:
    tags: [travel, visas, passport, entry, borders]
    related_skills: [browser-skill:trip-plan]
platforms: [macos]
---
# Can I get in

## Purpose
The boring check that saves the trip. What this passport needs for this country,
what it costs, how long it takes, and what has changed since last time.

## Reads
- Search results for current entry requirements and passport rules for visitors to entry requirements for Americans visiting Europe.
- Search results for recent changes to travel authorization and border systems for entry requirements for Americans visiting Europe.

## Lands in
- Splits the two passport rules people mix up. Short enough to act on straight away.

## Steps
1. Look up current entry requirements and passport rules for visitors to entry requirements for Americans visiting Europe.
2. Look up recent changes to travel authorization and border systems for entry requirements for Americans visiting Europe.
3. Splits the two passport rules people mix up. For the Schengen area the passport must have been issued within the past ten years and stay valid three months past the day you leave, and both have to be true at once.

## Success criteria
- Splits the two passport rules people mix up. For the Schengen area the
  passport must have been issued within the past ten years and stay valid three
  months past the day you leave, and both have to be true at once.
- Says why the gate is strict about it: the airline pays for the deportation
  flight, so a passport one day short gets refused boarding, not waved through.
- Names the systems separately instead of blurring them. The EU Entry and Exit
  System replaced passport stamps at every Schengen border on April 10, 2026,
  and takes fingerprints and a face scan on the first crossing. ETIAS is a
  different thing, a paid online authorization valid three years, and is not
  fully enforced until about a year after it opens.
- Flags the UK, which caught a lot of people. Since February 25, 2026 an
  Electronic Travel Authorisation applies to Americans, Canadians, Australians
  and all 27 EU nationalities, every traveler needs their own including babies,
  and Eurostar and the ferries check it as well as the airlines.
- Puts the slowest item first, so the thing with a real processing time gets
  started today and the ten minute one waits.
- Says plainly when nothing is needed, in one line, and stops.

## Failure behavior
- If an official page will not load, say what the requirement was at last check
  and that it needs confirming on the government site.
- If the rule depends on nationality and none was given, ask for the passport
  instead of guessing.

## Never
- Never sign in to a government, visa or airline account.
- Never apply for, pay for, submit or buy any authorization.
- Never invent a fee, a processing time or a rule that is not published.

## Redaction
Omit query strings, account details, passport and application numbers, dates of
birth, saved cards, home address, and anything shown after a page unexpectedly
asks for a login.
