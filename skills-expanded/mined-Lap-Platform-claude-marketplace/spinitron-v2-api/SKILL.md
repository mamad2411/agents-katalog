---
name: spinitron-v2-api
description: "Spinitron v2 API skill. Use when working with Spinitron v2 for personas, shows, playlists. Covers 9 endpoints."
version: 1.0.0
generator: lapsh
---

# Spinitron v2 API
API version: 1.0.0

## Auth
Bearer bearer | ApiKey access-token in query

## Base URL
https://spinitron.com/api

## Setup
1. Set Authorization header with your Bearer token
2. GET /personas -- verify access
3. POST /spins -- create first spins

## Endpoints

9 endpoints across 4 groups. See references/api-spec.lap for full details.

### personas
| Method | Path | Description |
|--------|------|-------------|
| GET | /personas | Get Personas |
| GET | /personas/{id} | Get Persona by id |

### shows
| Method | Path | Description |
|--------|------|-------------|
| GET | /shows | Returns scheduled shows optionally filtered by {start} and/or {end} datetimes |
| GET | /shows/{id} | Get a Show by id |

### playlists
| Method | Path | Description |
|--------|------|-------------|
| GET | /playlists | Returns playlists optionally filtered by {start} and/or {end} datetimes |
| GET | /playlists/{id} | Get a Playlist by id |

### spins
| Method | Path | Description |
|--------|------|-------------|
| GET | /spins | Returns spins optionally filtered by {start} and/or {end} datetimes |
| POST | /spins | Log a Spin |
| GET | /spins/{id} | Get a Spin by id |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all personas?" -> GET /personas
- "Get persona details?" -> GET /personas/{id}
- "List all shows?" -> GET /shows
- "Get show details?" -> GET /shows/{id}
- "List all playlists?" -> GET /playlists
- "Get playlist details?" -> GET /playlists/{id}
- "List all spins?" -> GET /spins
- "Create a spin?" -> POST /spins
- "Get spin details?" -> GET /spins/{id}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
