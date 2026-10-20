---
name: music-listening-journal
description: Logs active listening sessions, albums, and tracks to Obsidian with ratings, notes, and context.
category: media
tags: [media, music, journal, obsidian, listening, review]
agents: [opencode, freebuff, antigravity, codex]
---

# music-listening-journal

## Purpose

Captures structured listening session notes in Obsidian. Records album/track, listening context (mood, activity, date), personal ratings, and discovery source. Bridges Subsonic playback data with Obsidian vault knowledge.

## Invocation

**OpenCode / Codex:** `Invoke music-listening-journal`
**Freebuff:** `/skill music-listening-journal`

## Workflow Steps

1. **Capture session:** Record what is playing (artist, album, track list).
2. **Context:** Note mood, activity, discovery source (Soulseek search, recommendation).
3. **Rate:** Apply 1-5 star rating and brief review note.
4. **Tag:** Add genre, decade, vibe tags.
5. **Write:** Create or append to Obsidian daily note under `Music` heading.
6. **Link:** Backlink to artist/album pages in vault.

## Inputs

- Artist, album, and track information (manual or from `subsonic-api-client` getNowPlaying)
- Mood, activity, and discovery source context
- Optional: star rating and short review note

## Outputs

- Created or appended daily note entry under the `Music` heading in Obsidian
- Backlinks to artist/album pages
- Genre, decade, and vibe tags applied

## Safety

- Writes only to Obsidian vault; never modifies Subsonic library.
- Respect rate limits if querying Subsonic `getNowPlaying` endpoint.

## Failure Modes

- Subsonic `getNowPlaying` unavailable — fall back to manual track entry.
- Vault write conflict if daily note is open in Obsidian — prompt user to close before writing.

## References

- [Obsidian Markdown](https://help.obsidian.md/)
- [OpenSubsonic getNowPlaying](https://opensubsonic.netlify.app/docs/endpoints/getnowplaying/)

## Companion Skills

- `obsidian-music-journal`, `subsonic-api-client`, `dj-mix-documentarian`
