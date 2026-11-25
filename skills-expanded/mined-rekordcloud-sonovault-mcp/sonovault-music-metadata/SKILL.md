---
name: sonovault-music-metadata
description: Look up music metadata with the SonoVault API. Use when the user needs track, artist, label, or release data. ISRC or ISWC codes, genre, BPM and musical key, release dates, or a track's IDs and links on Spotify, Apple Music, Tidal, Beatport, Discogs, MusicBrainz, or YouTube. Covers single lookups, bulk resolution of play logs and library exports, and royalty-reporting enrichment.
license: MIT
metadata:
  author: rekordcloud
---

You query the SonoVault music metadata API: 93M+ tracks with ISRC, ISWC, genre, BPM, musical key, label, release dates, and cross-platform IDs.

## Setup

- Base URL: `https://api.sonovault.now`
- Every request needs the API key header: `x-api-key: $SONOVAULT_API_KEY`
- Read the key from the `SONOVAULT_API_KEY` environment variable. If it is missing, tell the user to get a free key at https://sonovault.now (1,000 requests/month, no credit card) and export it.
- All responses are JSON, snake_case. List endpoints paginate with `next_cursor`; pass it back as `cursor`. `next_cursor` is null on the last page.

If the environment has the SonoVault MCP server available (`sonovault-mcp`), prefer its tools over raw HTTP.

## When to activate

- The user asks about a track, artist, label, or release: genre, label, release date, ISRC.
- The user has an ISRC or ISWC code, or wants one.
- The user wants a track's ID or link on another platform.
- The user has a list to enrich: a radio play log, a DJ library export, a CSV of ISRCs.

## Core recipes

### Find a track (and its ISRC)

Search requires BOTH `artist` and `title`. There is no free-text `q` parameter.

```bash
curl -s "https://api.sonovault.now/v1/tracks/search?artist=Daft+Punk&title=One+More+Time&limit=5" \
  -H "x-api-key: $SONOVAULT_API_KEY"
```

Each result carries `id`, `title`, `artists`, `isrc`, `duration`, `bpm`, `key_alphanumeric`, `key_musical`, `key_open`, `keys`, `genre`, `subgenre`, and `releases` (album title, label, release_date). The search is fuzzy: it survives `(Original Mix)` suffixes, `feat.` credits, and messy casing, so pass raw playout strings as-is.

### Tempo and key

Every track (search, ISRC lookup, by id, browse, resolve, release tracklists) carries:

- `bpm`: full tempo, up to 2 decimals (174, not 87).
- `key_alphanumeric`: 1 to 12 plus `A` (minor) or `B` (major), e.g. `10B`.
- `key_musical`: e.g. `D`, `Am`, `F#m`, `Ebm`.
- `key_open`: Open Key notation, lowercase, e.g. `3d`, `1m`.
- `keys`: every key held, one `{key_alphanumeric, key_musical, key_open, source}` per source.

Use them for harmonic mixing (same alphanumeric number, the same number with the other letter, or one number up or down mix cleanly) and for tempo questions (filtering a set by BPM range, spotting half or double time). Null values (and an empty `keys`) mean the track has not been analysed yet, not that it has no key; say so rather than guessing a value.

### Look up by ISRC

ISRC is a path parameter, not a query parameter:

```bash
curl -s "https://api.sonovault.now/v1/tracks/isrc/GBDUW0000053" -H "x-api-key: $SONOVAULT_API_KEY"
```

One canonical track can carry many ISRCs (radio edit, remaster, reissue each mint their own). Any of them resolves to the same track. Cross-source ISRC disagreement is normal, not an error.

### Cross-platform IDs and links

Pass exactly ONE identifying parameter: `id`, `isrc`, `spotify_id`, `applemusic_id`, `tidal_id`, `beatport_id`, `discogs_id`, `musicbrainz_id`, or `youtube_id`. A `discogs_id` is a Discogs track key (release ID plus track position, e.g. `2844-A`), never a bare release ID.

```bash
curl -s "https://api.sonovault.now/v1/tracks/links?isrc=GBDUW0000053" -H "x-api-key: $SONOVAULT_API_KEY"
```

Returns one entry per platform with `external_id` and a deep link `url`.

### ISWC (composition codes)

Recording to work: `GET /v1/tracks/iswc?isrc=...` (or `?id=<track id>`). Returns the ISWC(s) behind the recording; a track can have several (medleys, samples), or none.
Work to recordings: `GET /v1/tracks/iswc/T0710204399`. Dotted and dashed ISWC formats are accepted. Returns recordings by popularity with a representative ISRC each.

### Bulk resolve (up to 100 lines per call)

Use for play logs and library exports instead of looping over search. Costs one API credit per line.

```bash
curl -s -X POST "https://api.sonovault.now/v1/tracks/resolve" \
  -H "x-api-key: $SONOVAULT_API_KEY" -H "Content-Type: application/json" \
  -d '{"input_type": "track_name", "items": [{"artist": "Daft Punk", "title": "Aerodynamic"}]}'
```

`input_type` is one of `track_name`, `isrc`, `sonovault_id`, `spotify_id`, `applemusic_id`, `tidal_id`, `beatport_id`, `discogs_id`, `musicbrainz_id`. Items are strings, except `track_name` items which are `{artist, title}` objects. Each result row has `status` (`matched`, `not_found`, or `skipped_no_credits`), the `track`, and its `links`. Report not_found lines to the user rather than dropping them silently.

### Artists, labels, releases, genres

- `GET /v1/artists/search?name=...`, `GET /v1/artists/:id`, `GET /v1/artists/:id/releases` (newest first)
- `GET /v1/labels/search?name=...`, `GET /v1/labels/:id/releases`, `GET /v1/labels/:id/artists`
- `GET /v1/releases/search?title=...&artist=...`, `GET /v1/releases/:id` (includes full tracklist with ISRCs)
- `GET /v1/genres` (canonical genre hierarchy with IDs)

## Royalty-report enrichment

Radio play logs carry artist + title but royalty reports (SoundExchange, PPL, Sena, GVL, Re:Sound) match on ISRC and label. Resolve the log with bulk resolve, then output artist, title, ISRC, album, and label per line. Always tell the user to verify data before filing; SonoVault aggregates third-party data and is not affiliated with any collecting society.

## Errors and limits

- 401: bad or missing key. 403 with "paid" wording: the endpoint needs a paid tier (`/v1/tracks/browse`, audio identify). 429: rate limit (retry after the `Retry-After` header) or monthly credits exhausted (do not retry; tell the user).
- The public API does NOT expose popularity scores, energy, danceability, artwork, or lyrics. Say so instead of guessing.

## References

- Full API docs: https://sonovault.now/docs (markdown mirror: https://sonovault.now/docs/markdown)
- MCP server: https://github.com/rekordcloud/sonovault-mcp (`npx -y sonovault-mcp`)
- Client SDKs: `npm install sonovault` / `pip install sonovault`
