---
name: soundtrack-my-day
skill_id: browser-skill:soundtrack-my-day
description: A playlist or mix that fits what you are doing right now
when_to_use:
  - intent_keywords: [music, playlist, mix, put something on, background music, what should i play]
    require_auth: false
    mutation_boundary: read_only
steps:
  - caption: playlists and mixes people actually use for
    capability_target: web_search
    mutation_boundary: read_only
  - caption: which mix holds up for a full session of
    capability_target: web_search
    mutation_boundary: read_only
parameters:
  - name: what_you_are_doing
    current_value: deep work at my desk on a gray afternoon
    fill_rule: say what you are doing and Luke finds the mix that fits
adapter_preferences:
  preferred: browserbase
  fallback: owned_browser
  declined: []
schema_version: 1
metadata:
  luke:
    tags: [music, playlists, mixes, mood, on-demand]
    related_skills: [browser-skill:trending-playlists]
platforms: [macos]
---
# Soundtrack my day

## Purpose
You want something on, and you do not want to spend ten minutes choosing it.
Say what you are doing and get one mix that fits, ready to play.

## Reads
- Search results for playlists and mixes people actually use for deep work at my desk on a gray afternoon.
- Search results for which mix holds up for a full session of deep work at my desk on a gray afternoon.

## Lands in
- Gives one pick, named, with the curator or channel and the runtime. Short enough to act on straight away.

## Steps
1. Look up playlists and mixes people actually use for deep work at my desk on a gray afternoon.
2. Look up which mix holds up for a full session of deep work at my desk on a gray afternoon.
3. Gives one pick, named, with the curator or channel and the runtime.

## Success criteria
- Gives one pick, named, with the curator or channel and the runtime.
- Says what it sounds like in a line, using sound, not vibe words.
- Matches the energy of the activity, not just the genre.
- Offers a second option only when the mood could go two clear ways.

## Failure behavior
- If a playlist page will not load, skip it and keep going.
- If nothing fits well, say so and name the closest mix and what is off about it.

## Never
- Never sign in, follow, save or download anything.
- Never invent a playlist, a curator or a track list.
- Never pass a paid placement off as something people actually play.

## Redaction
Omit query strings, account details, listening history, saved libraries, and
anything shown after a page unexpectedly asks for a login.
