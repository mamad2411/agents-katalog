---
name: library-card-secrets
skill_id: browser-skill:library-card-secrets
description: Everything your library card gets you that is not a book
when_to_use:
  - intent_keywords: [library card, museum pass, borrow, library of things, free stuff, park pass]
    require_auth: false
    mutation_boundary: read_only
steps:
  - caption: library museum pass, park pass and library of things lending near
    capability_target: web_search
    mutation_boundary: read_only
  - caption: how to reserve a pass, loan length and how many people it admits at the library near
    capability_target: web_search
    mutation_boundary: read_only
parameters:
  - name: library
    current_value: library museum pass in Los Angeles
    fill_rule: say your city and Luke uses it instead
adapter_preferences:
  preferred: browserbase
  fallback: owned_browser
  declined: []
schema_version: 1
metadata:
  luke:
    tags: [library, free, museum pass, borrow, local]
    related_skills: [browser-skill:city-secret]
platforms: [macos]
---
# Library card secrets

## Purpose
On demand, for the moment someone realizes the card in their wallet is doing
about two percent of its job. Most US library systems lend museum passes,
state park passes and power tools, and almost nobody claims them.

## Reads
- Search results for library museum pass, park pass and library of things lending near library museum pass in Los Angeles.
- Search results for how to reserve a pass, loan length and how many people it admits at the library near library museum pass in Los Angeles.

## Lands in
- Names the user's real library system, not a generic list of what libraries do. Short enough to act on straight away.

## Steps
1. Look up library museum pass, park pass and library of things lending near library museum pass in Los Angeles.
2. Look up how to reserve a pass, loan length and how many people it admits at the library near library museum pass in Los Angeles.
3. Names the user's real library system, not a generic list of what libraries do.

## Success criteria
- Names the user's real library system, not a generic list of what libraries do.
- Says whether it runs a museum pass program, how many people one pass admits,
  which is often up to four, and how long the loan runs, which is often a week.
- Names the state park pass if the state has one, like the Empire Pass in New
  York or the Discover Pass through Check Out Washington.
- Covers the non book shelf when it exists: tools, sewing machines, telescopes,
  instruments, wifi hotspots, board games, seed libraries.
- Says which streaming the card unlocks, Kanopy or Hoopla or both, and that
  passes are first come first served so reserving early is the whole game.

## Failure behavior
- If a source will not load, skip it and keep going.
- If the local system lends none of this, say so plainly and name the nearest
  system that does, since many allow non resident cards.

## Never
- Never sign in, place a hold, reserve a pass or check anything out.
- Never invent a lending program, a loan length or a pass the system does not offer.
- Never pass a neighboring system's program off as the user's own library.

## Redaction
Omit query strings, account details, card numbers, loan history, saved cards,
home address, and anything shown after a page unexpectedly asks for a login.
