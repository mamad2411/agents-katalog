---
name: tidal-playlist
description: Manage Tidal playlists — list, create, rename, delete, set public/private visibility, add or remove albums and tracks, and list tracks in a playlist. Use when the user wants to work with playlists or share one.
allowed-tools: Bash, Read, Grep
argument-hint: "<list|tracks|create|rename|delete|visibility|add-album|add-track|remove-track> [options]"
---

# Tidal Playlist

Manage Tidal playlists: list, create, rename, delete, set visibility, and add or remove content.

## Commands

### playlist list
- **Usage**: `tidal-cli --json playlist list [--public|--private]`
- **Arguments**: `--public` / `--private` (optional) — restrict to public or private playlists; omit for all
- **Output**: `[{id, name, num_tracks, public}]`

### playlist tracks
- **Usage**: `tidal-cli --json playlist tracks --playlist-id <id>`
- **Arguments**: `--playlist-id` (required)
- **Output**: `[{track_number, id, title, artist, album, duration_seconds}]`
  - `track_number` : position dans la playlist (1..N), pas le numéro sur l'album

### playlist create
- **Usage**: `tidal-cli --json playlist create --name "<name>" [--desc "<description>"] [--public|--private]`
- **Arguments**: `--name` (required), `--desc` (optional), `--public` / `--private` (optional, default private)
- **Output**: `{id, name, description, public}`
  - Tidal always creates playlists private, so `--public` triggers a second call. If it fails, the
    playlist still exists: the command warns on stderr, returns `public: false` and exits 0.

### playlist rename
- **Usage**: `tidal-cli --json playlist rename --playlist-id <id> --name "<new_name>"`
- **Arguments**: `--playlist-id` (required), `--name` (required)
- **Output**: `{status, id, old_name, new_name}`

### playlist visibility
- **Usage**: `tidal-cli --json playlist visibility --playlist-id <id> --public|--private`
- **Arguments**: `--playlist-id` (required), exactly one of `--public` / `--private` (required)
- **Output**: `{status, id, name, was_public, public}`

### playlist delete
- **Usage**: `tidal-cli --json playlist delete --playlist-id <id>`
- **Arguments**: `--playlist-id` (required)
- **Output**: `{status, id, name}`

### playlist add-album
- **Usage**: `tidal-cli --json playlist add-album --playlist-id <id> --album-id <id>`
- **Arguments**: `--playlist-id` (required), `--album-id` (required)
- **Output**: `{status, tracks_added, album, playlist}`

### playlist add-track
- **Usage**: `tidal-cli --json playlist add-track --playlist-id <id> --track-id <id>`
- **Arguments**: `--playlist-id` (required), `--track-id` (required)
- **Output**: `{status, track, playlist}`

### playlist remove-track
- **Usage**: `tidal-cli --json playlist remove-track --playlist-id <id> --track-id <id>`
- **Arguments**: `--playlist-id` (required), `--track-id` (required)
- **Output**: `{status, track, playlist}`

## Instructions

1. Parse `$ARGUMENTS` to determine the operation (first word) and its parameters:
   - `list` — optionally extract `--public` or `--private`
   - `tracks` — extract `--playlist-id`
   - `create` — extract `--name` and optionally `--desc`, `--public` or `--private`
   - `rename` — extract `--playlist-id` and `--name`
   - `delete` — extract `--playlist-id`
   - `visibility` — extract `--playlist-id` and `--public` or `--private`
   - `add-album` — extract `--playlist-id` and `--album-id`
   - `add-track` — extract `--playlist-id` and `--track-id`
   - `remove-track` — extract `--playlist-id` and `--track-id`
   - If no operation given, show usage: `/tidal-playlist <list|tracks|create|rename|delete|visibility|add-album|add-track|remove-track> [options]`

2. Run the appropriate command and parse JSON output:
   - **list** → format as table with columns `ID`, `Name`, `Tracks`, `Visibility` (public/private)
   - **tracks** → format as numbered list: `#. Title — Artist [Album] MM:SS`
   - **create** → confirm: "Playlist created: **<name>** (ID: `<id>`)". If `--public` was requested
     but the output shows `public: false`, warn that it was created private and suggest
     `/tidal-playlist visibility --playlist-id <id> --public`.
   - **rename** → confirm: "Playlist renamed: **<old_name>** → **<new_name>**"
   - **visibility** → confirm: "Playlist **<name>** is now <public|private>." If `was_public` already equals the requested value, say it was already in that state.
   - **delete** → confirm: "Playlist **<name>** (ID: `<id>`) deleted."
   - **add-album** → confirm: "<tracks_added> track(s) from album **<album>** added to playlist **<playlist>**."
   - **add-track** → confirm: "Track **<track>** added to playlist **<playlist>**."
   - **remove-track** → confirm: "Track **<track>** removed from playlist **<playlist>**."

3. If required arguments are missing for an operation, show a usage hint specific to that operation.

## Error Handling

- If exit code is non-zero, read stderr:
  - `"Error: Not authenticated"` → "You need to authenticate first. Run `/tidal-auth` to log in."
  - `"Error: Playlist not found"` → "Playlist not found (ID: `<id>`). Use `/tidal-playlist list` to see your playlists."
  - `"Error: Track not found in playlist"` → "Track (ID: `<id>`) is not in this playlist."
  - `"Error: Playlist name cannot be empty"` → "Please provide a non-empty playlist name."
  - `"Error: Playlist is not owned by the current user"` → "You can only change the visibility of playlists you own."
  - `"Error: Unable to connect to Tidal"` → "Network error: unable to reach Tidal. Check your internet connection."
  - Any other error → display the raw error message with label "Error:"
