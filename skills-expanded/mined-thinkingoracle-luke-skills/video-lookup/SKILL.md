---
name: video-lookup
skill_id: browser-skill:video-lookup
description: The video that actually answers what you asked, not a page about it
when_to_use:
  - intent_keywords: [video, youtube, show me, find the video, tutorial, watch, how to]
    require_auth: false
    mutation_boundary: read_only
steps:
  - caption: the video that actually shows
    capability_target: web_search
    mutation_boundary: read_only
  - caption: which upload people say is the clearest on
    capability_target: web_search
    mutation_boundary: read_only
parameters:
  - name: what_you_want_to_see
    current_value: how to fix a bike puncture without tire levers
    fill_rule: say what you want to see and Luke finds the video that shows it
adapter_preferences:
  preferred: browserbase
  fallback: owned_browser
  declined: []
schema_version: 1
metadata:
  luke:
    tags: [video, youtube, search, tutorials, on-demand]
    related_skills: []
platforms: [macos]
---
# Video lookup

## Purpose
You do not want an article about it. You want the video where somebody does the
thing on camera. This finds that one and hands it over.

## Reads
- Search results for the video that actually shows how to fix a bike puncture without tire levers.
- Search results for which upload people say is the clearest on how to fix a bike puncture without tire levers.

## Lands in
- Gives one video, named, with the channel and the runtime. Short enough to act on straight away.

## Steps
1. Look up the video that actually shows how to fix a bike puncture without tire levers.
2. Look up which upload people say is the clearest on how to fix a bike puncture without tire levers.
3. Gives one video, named, with the channel and the runtime.

## Success criteria
- Gives one video, named, with the channel and the runtime.
- Says what happens in it, so it is clear before pressing play.
- Prefers the upload that shows the thing over the one that talks around it.
- Says when a two minute short covers it and the full video is not needed.

## Failure behavior
- If a source will not load, skip it and keep going.
- If no video really covers it, say so and name the closest thing.

## Never
- Never sign in, subscribe or download anything.
- Never invent a title, a channel or a timestamp.
- Never pass a sponsored upload off as the top pick.

## Redaction
Omit query strings, account details, watch history, subscriptions, saved cards,
and anything shown after a page unexpectedly asks for a login.
