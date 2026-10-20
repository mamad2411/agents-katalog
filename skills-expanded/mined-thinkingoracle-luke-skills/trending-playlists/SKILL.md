---
name: trending-playlists
skill_id: browser-skill:trending-playlists
description: What is climbing the charts and which playlists everyone is on right now
when_to_use:
  - host: open.spotify.com
    path_prefix: /
    intent_keywords: [spotify, playlist, trending, charts, top songs, viral, whats hot]
    require_auth: true
    mutation_boundary: read_only
  - host: open.spotify.com
    path_prefix: /
    intent_keywords: [trending music, whats charting, viral songs, top 50]
    require_auth: true
    mutation_boundary: read_only
steps:
  - caption: read visible Spotify charts and trending playlists for
    capability_target: delegate_web_action
    host: open.spotify.com
    mutation_boundary: read_only
trigger:
  kind: schedule
  recurrence: weekly
  weekday: 2
  time: 17:15
  timezone: America/Los_Angeles
  follows_device: true
parameters:
  - name: scene
    current_value: pop, hip hop and dance
    fill_rule: say which genres or scenes you want tracked
adapter_preferences:
  preferred: owned_browser
  declined: [browserbase, frontmost_local, yutori]
schema_version: 1
metadata:
  luke:
    tags: [spotify, playlists, charts, trending, music, discovery]
    related_skills: [browser-skill:new-this-week]
platforms: [macos]
---

# Trending playlists

## Purpose
Monday morning, the song that's taking off and the playlist worth opening. You get to be the one who plays it first.

## Reads
- Visible Spotify chart and playlist text from Luke's isolated owned-browser profile.
- The user's signed-in Spotify session only when they have set it up locally and approved navigation.

## Lands in
- Names the track and the artist, and says whether it is rising or peaking. Short enough to act on straight away.

## Steps
1. Open Spotify in Luke's isolated owned-browser profile after the user approves navigation.
2. Read visible charts and trending playlists for pop, hip hop and dance without clicking, typing, following, saving, or submitting.
3. Name the track and the artist, and say whether it is rising or peaking.

## Success criteria
- Names the track and the artist, and says whether it is rising or peaking.
- Gives one playlist worth opening, not a wall of links.
- Sticks to the scenes the user asked for.
- A quiet week is one line, not a padded chart dump.

## Failure behavior
- If a chart will not load, skip it and keep going. Do not report the plumbing.
- If nothing is really moving, say so and name the one thing worth a listen.

## Never
- Never ask for, capture, type, export, or transmit credentials. The user signs in directly inside Luke's owned-browser profile.
- Never use Browserbase, the user's everyday browser, a hosted fetch service, or another remote browser for signed-in page content.
- Never follow, save, or add anything to a library or playlist.
- Never invent a chart position, a stream count or a release date.
- Never pass a paid placement off as organic movement.

## Redaction
Omit query strings, account details, listening history, saved libraries, and
all other account-specific content. Persist only the redacted result needed to
name the public track, artist, chart movement, and playlist.
