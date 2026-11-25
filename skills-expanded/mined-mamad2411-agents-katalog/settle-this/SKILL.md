---
name: settle-this
skill_id: browser-skill:settle-this
description: Who is right, with the sources named
when_to_use:
  - intent_keywords: [settle this, who is right, is it true, fact check, actually, prove it, argument]
    require_auth: false
    mutation_boundary: read_only
steps:
  - caption: the primary source, original data or official record on
    capability_target: web_search
    mutation_boundary: read_only
  - caption: where the common belief came from and whether it was ever corrected about
    capability_target: web_search
    mutation_boundary: read_only
parameters:
  - name: the_claim
    current_value: does cracking your knuckles cause arthritis
    fill_rule: type the claim exactly as it was said and Luke goes and checks it
adapter_preferences:
  preferred: browserbase
  fallback: owned_browser
  declined: []
schema_version: 1
metadata:
  luke:
    tags: [facts, sources, research, arguments, on-demand]
    related_skills: [browser-skill:explain-like-im-in]
platforms: [macos]
---
# Settle this

## Purpose
An argument is running and everyone is confident. This goes to the primary
source and comes back with the answer plus where it came from, so it ends.

## Reads
- Search results for the primary source, original data or official record on does cracking your knuckles cause arthritis.
- Search results for where the common belief came from and whether it was ever corrected about does cracking your knuckles cause arthritis.

## Lands in
- Answers the actual question asked, in the first line. Short enough to act on straight away.

## Steps
1. Look up the primary source, original data or official record on does cracking your knuckles cause arthritis.
2. Look up where the common belief came from and whether it was ever corrected about does cracking your knuckles cause arthritis.
3. Answers the actual question asked, in the first line.

## Success criteria
- Answers the actual question asked, in the first line.
- Names the source by name and date, not just "studies show".
- Says plainly when the real answer is that nobody knows, and why.
- Flags when both sides are arguing about different definitions of the word.

## Failure behavior
- If the primary source is paywalled, say so and use the best public summary,
  labeled as a summary.
- If the evidence genuinely splits, say it splits and give the strongest case
  on each side.

## Never
- Never sign in, subscribe, pay for access or join anything.
- Never invent a study, a statistic, a quote or a citation.
- Never present a blog restating a source as the source.

## Redaction
Omit query strings, account details, saved cards, home address, and anything
shown after a page unexpectedly asks for a login.
