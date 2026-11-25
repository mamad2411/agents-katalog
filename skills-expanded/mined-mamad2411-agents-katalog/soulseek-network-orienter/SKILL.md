---
name: soulseek-network-orienter
description: Teaches Soulseek culture, etiquette, and search strategies; logs discoveries to Obsidian.
category: media
tags: [media, soulseek, music, acquisition, etiquette]
agents: [opencode, freebuff, antigravity, codex]
---

# soulseek-network-orienter

## Purpose

Orients the agent to Soulseek's culture, etiquette, and search patterns for respectful, intentional music discovery and acquisition.

## Invocation

**OpenCode / Codex:** `Invoke soulseek-network-orienter`
**Freebuff:** `/skill soulseek-network-orienter`

Invoke this before any Soulseek-related MCP tools or slskd API calls.

## Soulseek Culture

Soulseek is a community of music enthusiasts, not just a data source:
- Maintain a good share ratio — share diverse, well-tagged music.
- Be patient with queues; avoid spam queries.
- Respect other users' bandwidth limits and sharing preferences.
- Do not attempt mass-scraping or abusive query patterns.

## Search Strategies

- Search by artist, release, label, year, genre, or scene keywords.
- Prefer targeted searches over broad ones.
- Bookmark interesting users for future discovery.
- Prioritize high-quality files (FLAC, high-bitrate MP3) when available.

## Workflow

1. Clarify what the user is looking for (release, scene, mood, label).
2. Suggest targeted search terms.
3. After finding targets, coordinate with `slskd-media-acquisition` or `slsk-mcp-client` for download.
4. Log discoveries in Obsidian via `obsidian-music-journal`.

## Inputs

- User search intent: release, artist, label, scene, mood, or era
- Optional: existing Soulseek username bookmarks or preferred user lists

## Outputs

- Targeted search term suggestions
- Recommended download targets for user approval
- Discovery log entry in `obsidian-music-journal`

## Safety & Ethics

- Never automate mass downloads without explicit user intent per session.
- Do not log other users' personal info beyond username and general collection metadata.
- Respect community norms; when in doubt, ask the user to decide manually.

## Failure Modes

- No results for search terms — suggest alternate spellings, label names, or scene handles.
- Vault write unavailable — queue discovery log and retry on next Obsidian sync.

## References

- slskd: https://github.com/slskd/slskd
- Soulseek Qt: https://www.slsknet.org/

## Companion Skills

- `slskd-media-acquisition` — execute downloads via slskd
- `slsk-mcp-client` — MCP-based Soulseek access
- `obsidian-music-journal` — log discoveries
- `music-library-organizer` — organize after download
