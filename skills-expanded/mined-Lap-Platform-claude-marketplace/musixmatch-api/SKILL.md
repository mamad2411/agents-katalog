---
name: musixmatch-api
description: "Musixmatch API skill. Use when working with Musixmatch for album.tracks.get, album.get, artist.related.get. Covers 16 endpoints."
version: 1.0.0
generator: lapsh
---

# Musixmatch API
API version: 1.1.0

## Auth
ApiKey apikey in query

## Base URL
https://api.musixmatch.com/ws/1.1

## Setup
1. Set your API key in the appropriate header
2. GET /album.tracks.get -- verify access

## Endpoints

16 endpoints across 16 groups. See references/api-spec.lap for full details.

### album.tracks.get
| Method | Path | Description |
|--------|------|-------------|
| GET | /album.tracks.get |  |

### album.get
| Method | Path | Description |
|--------|------|-------------|
| GET | /album.get |  |

### artist.related.get
| Method | Path | Description |
|--------|------|-------------|
| GET | /artist.related.get |  |

### artist.albums.get
| Method | Path | Description |
|--------|------|-------------|
| GET | /artist.albums.get |  |

### artist.search
| Method | Path | Description |
|--------|------|-------------|
| GET | /artist.search |  |

### artist.get
| Method | Path | Description |
|--------|------|-------------|
| GET | /artist.get |  |

### matcher.subtitle.get
| Method | Path | Description |
|--------|------|-------------|
| GET | /matcher.subtitle.get |  |

### matcher.track.get
| Method | Path | Description |
|--------|------|-------------|
| GET | /matcher.track.get |  |

### matcher.lyrics.get
| Method | Path | Description |
|--------|------|-------------|
| GET | /matcher.lyrics.get |  |

### track.snippet.get
| Method | Path | Description |
|--------|------|-------------|
| GET | /track.snippet.get |  |

### track.lyrics.get
| Method | Path | Description |
|--------|------|-------------|
| GET | /track.lyrics.get |  |

### track.subtitle.get
| Method | Path | Description |
|--------|------|-------------|
| GET | /track.subtitle.get |  |

### track.get
| Method | Path | Description |
|--------|------|-------------|
| GET | /track.get |  |

### track.search
| Method | Path | Description |
|--------|------|-------------|
| GET | /track.search |  |

### chart.tracks.get
| Method | Path | Description |
|--------|------|-------------|
| GET | /chart.tracks.get |  |

### chart.artists.get
| Method | Path | Description |
|--------|------|-------------|
| GET | /chart.artists.get |  |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all album.tracks.get?" -> GET /album.tracks.get
- "List all album.get?" -> GET /album.get
- "List all artist.related.get?" -> GET /artist.related.get
- "List all artist.albums.get?" -> GET /artist.albums.get
- "List all artist.search?" -> GET /artist.search
- "List all artist.get?" -> GET /artist.get
- "List all matcher.subtitle.get?" -> GET /matcher.subtitle.get
- "List all matcher.track.get?" -> GET /matcher.track.get
- "List all matcher.lyrics.get?" -> GET /matcher.lyrics.get
- "List all track.snippet.get?" -> GET /track.snippet.get
- "List all track.lyrics.get?" -> GET /track.lyrics.get
- "List all track.subtitle.get?" -> GET /track.subtitle.get
- "List all track.get?" -> GET /track.get
- "List all track.search?" -> GET /track.search
- "List all chart.tracks.get?" -> GET /chart.tracks.get
- "List all chart.artists.get?" -> GET /chart.artists.get
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
