---
name: podcast-fetcher
skill_id: browser-skill:podcast-fetcher
description: The episode you half remember, found by guest, topic or that one line
when_to_use:
  - intent_keywords: [podcast, episode, which episode, that episode, guest, find the episode, they said]
    require_auth: false
    mutation_boundary: read_only
steps:
  - caption: which podcast episode covered
    capability_target: web_search
    mutation_boundary: read_only
  - caption: the show, episode number and release date for
    capability_target: web_search
    mutation_boundary: read_only
parameters:
  - name: what_you_remember
    current_value: the episode where a sleep scientist explained morning sunlight
    fill_rule: say the guest, the subject or the line you remember
adapter_preferences:
  preferred: browserbase
  fallback: owned_browser
  declined: []
schema_version: 1
metadata:
  luke:
    tags: [podcasts, episodes, listening, lookup, on-demand]
    related_skills: []
platforms: [macos]
---
# Podcast fetcher

## Purpose
You remember a guest, a subject, or one line somebody said. That is enough.
This comes back with the actual episode and where in it that part lands.

## Reads
- Search results for which podcast episode covered the episode where a sleep scientist explained morning sunlight.
- Search results for the show, episode number and release date for the episode where a sleep scientist explained morning sunlight.

## Lands in
- Names the show, the episode title and the guest. Short enough to act on straight away.

## Steps
1. Look up which podcast episode covered the episode where a sleep scientist explained morning sunlight.
2. Look up the show, episode number and release date for the episode where a sleep scientist explained morning sunlight.
3. Names the show, the episode title and the guest.

## Success criteria
- Names the show, the episode title and the guest.
- Says roughly where in the episode the remembered part falls.
- Gives one best match, and one runner up only when the match is genuinely close.
- Says plainly when the memory matches two different episodes.

## Failure behavior
- If a transcript is not public, work from show notes and clips and say so.
- If nothing matches, say so and name the closest episode on that subject.

## Never
- Never sign in, subscribe or download anything.
- Never invent an episode title, a guest or a timestamp.
- Never present a clip account's repost as the original episode.

## Redaction
Omit query strings, account details, listening history, subscriptions, saved
cards, and anything shown after a page unexpectedly asks for a login.
