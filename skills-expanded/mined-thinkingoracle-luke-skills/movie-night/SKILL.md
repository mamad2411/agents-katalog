---
name: movie-night
skill_id: browser-skill:movie-night
description: What to actually put on, decided in one line
when_to_use:
  - intent_keywords: [movie, film, watch, tonight, netflix, cinema, movie night]
    require_auth: false
    mutation_boundary: read_only
steps:
  - caption: best films to watch tonight for
    capability_target: web_search
    mutation_boundary: read_only
  - caption: what people are saying is worth watching right now in
    capability_target: web_search
    mutation_boundary: read_only
parameters:
  - name: mood
    current_value: best films streaming right now
    fill_rule: say the mood and who is watching
adapter_preferences:
  preferred: browserbase
  fallback: owned_browser
  declined: []
schema_version: 1
metadata:
  luke:
    tags: [movies, films, streaming, evenings]
    related_skills: []
platforms: [macos]
---
# Movie night

## Purpose
One film, the service it is on, and why that one tonight. The decision made, so the evening starts instead of stalling.

## Reads
- Search results for best films to watch tonight for best films streaming right now.
- Search results for what people are saying is worth watching right now in best films streaming right now.

## Lands in
- One pick. Short enough to act on straight away.

## Steps
1. Look up best films to watch tonight for best films streaming right now.
2. Look up what people are saying is worth watching right now in best films streaming right now.
3. One pick. Says where it is streaming tonight.

## Success criteria
- One pick. Says where it is streaming tonight.
- One line on why it suits the mood asked for.
- Gives the runtime, so nobody starts something too long.
- One backup, no more.

## Failure behavior
- If a source will not load, skip it and keep going.
- If nothing is on, say so in one line and give the best fallback.

## Never
- Never sign in, book, buy tickets or reserve anything.
- Never invent a venue, a time, a price or a lineup.
- Never pass a promoted listing off as what people rate.

## Redaction
Omit query strings, account details, order history, saved cards, home address,
and anything shown after a page unexpectedly asks for a login.
