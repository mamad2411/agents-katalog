---
name: new-artist-radar
skill_id: browser-skill:new-artist-radar
description: One artist you have not heard yet who fits what you already play
when_to_use:
  - intent_keywords: [new artist, new music, discover, who should i listen to, emerging, recommend an artist]
    require_auth: false
    mutation_boundary: read_only
steps:
  - caption: emerging artists people are getting into right now in
    capability_target: web_search
    mutation_boundary: read_only
  - caption: which track to start with and who they sound like for
    capability_target: web_search
    mutation_boundary: read_only
trigger:
  kind: schedule
  recurrence: weekly
  weekday: 7
  time: 08:30
  timezone: America/Los_Angeles
  follows_device: true
parameters:
  - name: taste
    current_value: hip hop, alternative and electronic
    fill_rule: say what you already listen to and Luke finds the next one
adapter_preferences:
  preferred: browserbase
  fallback: owned_browser
  declined: []
schema_version: 1
metadata:
  luke:
    tags: [music, artists, discovery, new-releases, weekly]
    related_skills: [browser-skill:new-this-week]
platforms: [macos]
---
# New artist radar

## Purpose
Saturday morning, one artist you have not heard, picked to sit next to what you
already play. One name, one track to start on, and why it lands for you.

## Reads
- Search results for emerging artists people are getting into right now in hip hop, alternative and electronic.
- Search results for which track to start with and who they sound like for hip hop, alternative and electronic.

## Lands in
- Names one artist and one specific track, not a genre roundup. Short enough to act on straight away.

## Steps
1. Look up emerging artists people are getting into right now in hip hop, alternative and electronic.
2. Look up which track to start with and who they sound like for hip hop, alternative and electronic.
3. Names one artist and one specific track, not a genre roundup.

## Success criteria
- Names one artist and one specific track, not a genre roundup.
- Says who they sound like, using artists the user already plays.
- Says where they are at, first release or third record, so the context is clear.
- A thin week is one name, or an honest line saying there is nothing new.

## Failure behavior
- If an artist page will not load, skip it and use coverage and reactions.
- If nothing new fits, say so and name an older artist the user likely missed.

## Never
- Never sign in, follow, save or download anything.
- Never invent an artist, a track title or a release date.
- Never pass a label push off as organic discovery.

## Redaction
Omit query strings, account details, listening history, saved libraries, and
anything shown after a page unexpectedly asks for a login.
