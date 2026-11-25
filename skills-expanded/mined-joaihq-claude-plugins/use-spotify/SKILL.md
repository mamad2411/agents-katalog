---
name: use-spotify
description: Use the Spotify JoAi app plugin when the task needs Spotify tools or workflows.
---

# Spotify

Connect Spotify to Claude, Cursor, and ChatGPT through JoAi's hosted MCP app server.

If a specific task was given, identify the relevant MCP tool and call it immediately — no preamble.

If invoked with no task, call the authenticate tool first (if present), then list the available actions concisely so the user can pick one.

Never ask "what would you like to do?" — either act on the task or show the menu.

## Example Prompts

- List the Spotify tools available in this app.
- Explain what setup or authentication Spotify needs before I run an action.
- Use Spotify to help me with the task I describe next.

## Action Inventory

- `spotify-get-album` (collect) — Get detailed information about an album on Spotify, including its tracks.
- `spotify-get-artist` (collect) — Get detailed information about an artist on Spotify.
- `spotify-get-artist-top-tracks` (collect) — Get the top tracks for an artist on Spotify.
- `spotify-get-currently-playing` (collect) — Get the track currently playing on the user's Spotify account.
- `spotify-get-playlist` (collect) — Get detailed information about a Spotify playlist, including its tracks.
- `spotify-get-track` (collect) — Get detailed information about a single track from Spotify.
- `spotify-search` (collect) — Search for tracks, artists, albums, or playlists on Spotify.

## Usage Notes

- Every listed action becomes an MCP tool when the app server is connected.
- Prefer the generated provider plugin when one is available, and fall back to the raw MCP URL otherwise.

## Auth Notes

- Some actions require provider credentials or OAuth on first use.
