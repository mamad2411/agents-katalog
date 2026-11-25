---
name: tidal-search
description: Search for artists, albums, or tracks on Tidal. Use when the user wants to find music, look up an artist, search for a song or album. To find an album of a known artist, always use artist-albums rather than album search.
allowed-tools: Bash, Read, Grep
argument-hint: "<artist|album|track|artist-albums> <query>"
---

# Tidal Search

Search for artists, albums, or tracks on Tidal and display results as a formatted table.

## Commands

### search artist-albums (preferred to find an album of a known artist)
- **Usage**: `tidal-cli --json search artist-albums "<artist name>" [--year <YYYY>]` or `tidal-cli --json search artist-albums --artist-id <id> [--year <YYYY>]`
- **Output**: `[{id, name, artist, artist_id, type, year, release_date, num_tracks}]`, newest first
- `type` is `ALBUM`, `EP` or `SINGLE`. A single often has the same title as the album it announces: the full album is the `ALBUM` entry with more tracks.
- An artist can have several Tidal profiles (different `artist_id`); all exact-name matches are returned.
- Why: `search album` is relevance-ranked and capped at 20 results, so a recent album gets buried by homonyms and singles.

### search artist
- **Usage**: `tidal-cli --json search --type artist --query "<query>"`
- **Output**: `[{id, name}]`

### search album
- **Usage**: `tidal-cli --json search --type album --query "<query>"`
- **Output**: `[{id, name, artist, year}]`

### search track
- **Usage**: `tidal-cli --json search --type track --query "<query>"`
- **Output**: `[{id, name, artist}]`

## Instructions

1. Parse `$ARGUMENTS`:
   - First word: search type (`artist`, `album`, `track`, or `artist-albums`)
   - Remaining words: the search query
   - If no arguments or missing search type, show usage: `/tidal-search <artist|album|track|artist-albums> <query>`
   - If no query provided after the type, ask the user to provide a search term

2. Run the appropriate command based on search type. When looking for an album and the artist is known, use `artist-albums` first and pick the `ALBUM` entry (check `num_tracks` and `release_date`); fall back to `album` only when the artist is unknown:
   - **artist-albums**: `tidal-cli --json search artist-albums "<artist name>"`
   - **artist**: `tidal-cli --json search --type artist --query "<query>"`
   - **album**: `tidal-cli --json search --type album --query "<query>"`
   - **track**: `tidal-cli --json search --type track --query "<query>"`

3. Parse the JSON array output and format as a markdown table:
   - **artist-albums**: columns `ID`, `Name`, `Type`, `Date`, and `Tracks`
   - **artist**: columns `ID` and `Name`
   - **album**: columns `ID`, `Name`, `Artist`, and `Year`
   - **track**: columns `ID`, `Name`, and `Artist`

4. If the result array is empty, display: "No results found for `<type>: <query>`."

## Error Handling

- If exit code is non-zero, read stderr:
  - `"Error: Not authenticated"` → "You need to authenticate first. Run `/tidal-auth` to log in."
  - `"Error: Unable to connect to Tidal"` → "Network error: unable to reach Tidal. Check your internet connection."
  - Any other error → display the raw error message with label "Error:"
