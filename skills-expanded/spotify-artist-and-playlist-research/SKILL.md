---
name: spotify-artist-and-playlist-research
description: Research Spotify artists, albums, tracks and public playlists with the Scrape Everything API. Profiles an artist's top tracks and releases, audits playlists (track list, artists, explicit share, total duration, where a given artist appears and at what position), compares playlists for overlap, and optionally checks the artist's YouTube channel and TikTok sound usage for cross-platform traction. Use when the user asks about a Spotify artist's catalogue or top songs, wants to analyse or compare Spotify playlists, check whether a track is on a playlist, plan playlist pitching, or research an artist's reach across Spotify, YouTube and TikTok.
---

# Spotify artist and playlist research

Artist snapshots, playlist audits and playlist-pitching research from public Spotify data, with optional YouTube/TikTok traction.

## Inputs

- **Artist**: Spotify artist link, URI or ID (`spotify:artist:...`).
- **Playlists** (optional): public Spotify playlist links/URIs/IDs to audit or check for the artist.
- **Albums / tracks** (optional): links, URIs or IDs.
- **Cross-platform** (optional): the artist's YouTube handle and a TikTok sound URL of their track.

Short links (spoti.fi, spotify.link) are not supported: ask for the open.spotify.com link (Share > Copy link).

## What Spotify data is (and is not) available

- `spotify.artist`: `name`, `image_url`, `top_tracks[]` (~10: `title`, `artists_text`, `duration_ms`, `is_explicit`, `preview_url`). Monthly listeners, followers and genres are **not** public and are not returned; do not estimate them.
- `spotify.album`: `title`, `artists_text`, `release_date`, `track_count`, `tracks[]`.
- `spotify.track`: `title`, `artists[]`, `release_date`, `duration_ms`, `is_explicit`, `is_playable`.
- `spotify.playlist`: `title`, `owner`, `total_duration_ms`, up to ~50 `tracks[]` (in playlist order).

## Credit estimate

| Task | Calls | Credits |
| --- | --- | ---: |
| Artist snapshot | `spotify.artist` + `spotify.album` on 1-3 releases | 2-4 |
| Playlist audit | `spotify.playlist` per playlist | 1 each |
| Cross-platform | `youtube.profile` + `youtube.videos` + `tiktok.music` | 1 + 1 + 2 |

Artist + 10 playlists + cross-platform: about **18 credits**. Use `"cache_days": 7`.

## How to call the API

Use the `scrapeeverything-api` skill if installed (MCP tools `spotify_artist`, `spotify_playlist`, the `scrapeeverything` CLI, or `node <skills-dir>/scrapeeverything-api/scripts/se.mjs spotify.playlist url=<link>`). Otherwise:

```bash
curl -sS https://api.scrapeeverything.com/v1/spotify/artist -H "Authorization: Bearer $SCRAPEEVERYTHING_API_KEY" \
  -H "Content-Type: application/json" -d '{"url":"https://open.spotify.com/artist/06HL4z0CvFAxyc27GXpf02","cache_days":7}'
```

## Method

**A. Artist snapshot**
1. `spotify.artist`: list top tracks with duration and explicit flag; note features (other names in `artists_text`).
2. Identify the releases behind the top tracks and fetch 1-3 with `spotify.album` for `release_date`, track count, and how many top tracks come from the latest release (recency of their hits).
3. Release cadence from album dates; average track length; explicit share.

**B. Playlist audit** (per playlist)
1. `spotify.playlist`: owner (Spotify editorial vs user/curator), `track_count` returned, `total_duration_ms`.
2. Compute: unique artists, most repeated artists, explicit share, median track length, and the artist of interest's tracks with their **position** (1-based).
3. Note the limit: only ~50 tracks are returned, so absence from a longer playlist is "not in the first 50", not "not on the playlist".

**C. Compare playlists / pitching shortlist**
1. Overlap matrix: shared tracks and shared artists between playlists (Jaccard on artists).
2. Rank playlists for pitching: artist overlap with the user's artist's sound (similar artists present), curator type, playlist length, explicit policy fit.

**D. Cross-platform traction** (optional)
1. YouTube: `youtube.profile` (`subscriber_count`) and `youtube.videos` (recent upload views).
2. TikTok: `tiktok.music` on the track's sound: `video_count` (how many videos use it) and top videos' play counts.

## Output template

```markdown
# Spotify research: {artist}
_Date: {YYYY-MM-DD} · Credits used: {n}_

## Artist snapshot
| # | Top track | Featuring | Length | Explicit | From release (date) |
| ---: | --- | --- | --- | --- | --- |

- Releases checked: {album, date, tracks}
- Hit recency: {n}/10 top tracks from the last 12 months
- Not available from Spotify publicly: monthly listeners, followers, genres

## Playlist audit
| Playlist | Owner | Tracks returned | Duration | Explicit % | {artist} tracks (position) |
| --- | --- | ---: | --- | ---: | --- |

## Overlap
| | P1 | P2 | P3 |
| --- | ---: | ---: | ---: |
| P1 | - | {shared artists} | ... |

## Pitching shortlist
1. {playlist}: {why it fits}

## Cross-platform traction
| Platform | Metric | Value |
| --- | --- | ---: |
| YouTube | Subscribers | ... |
| TikTok | Videos using "{sound}" | ... |

## Caveats
- Playlists return up to ~50 tracks.
```

## Guardrails

- Public catalogue and public playlists only; do not try to access private or collaborative playlists that are not public.
- Do not estimate or present private metrics (streams, listeners, follower counts) as if they came from Spotify.
- Playlist owners can be individuals: report owner display names as given, do not research them further.
- Preview URLs are for reference; do not download or redistribute audio.
