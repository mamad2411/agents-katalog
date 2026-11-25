---
name: aggregators-api-service
description: "Aggregators API Service API skill. Use when working with Aggregators API Service for api, stats, partners. Covers 28 endpoints."
version: 1.0.0
generator: lapsh
---

# Aggregators API Service
API version: 0.73-26f7c03

## Auth
ApiKey x-zeno-api-key in header | Bearer basic

## Base URL
https://api.zeno.fm

## Setup
1. Set Authorization header with your Bearer token
2. GET /api/v2/stations/list -- verify access
3. POST /stats/mounts/{mount}/auth-cache/reload -- create first reload

## Endpoints

28 endpoints across 3 groups. See references/api-spec.lap for full details.

### api
| Method | Path | Description |
|--------|------|-------------|
| GET | /api/v2/podcasts/{podcastKey} | Get podcast |
| PUT | /api/v2/podcasts/{podcastKey} | Update podcast |
| DELETE | /api/v2/podcasts/{podcastKey} | Delete podcast |
| GET | /api/v2/podcasts/{podcastKey}/episodes/{episodeKey} | Get podcast episode |
| PUT | /api/v2/podcasts/{podcastKey}/episodes/{episodeKey} | Update podcast episode |
| DELETE | /api/v2/podcasts/{podcastKey}/episodes/{episodeKey} | Delete podcast episode |
| POST | /api/v2/stations/search | Search stations |
| POST | /api/v2/stations/listener/location | Get top stations by listener location |
| POST | /api/v2/podcasts/{podcastKey}/episodes/create | Create podcast episode |
| POST | /api/v2/podcasts/search | Search podcasts |
| POST | /api/v2/podcasts/create | Create podcast |
| GET | /api/v2/stations/{stationKey} | Get station |
| GET | /api/v2/stations/list | List stations |
| GET | /api/v2/stations/languages | Get the list of Languages that can be used to filter stations in the search stations request |
| GET | /api/v2/stations/genres | Get the list of Genres that can be used to filter stations in the search stations request |
| GET | /api/v2/stations/countries | Get the list of Countries that can be used to filter stations in the search stations request |
| GET | /api/v2/stations/browse | Browse all stations |
| GET | /api/v2/podcasts/{podcastKey}/episodes | Get podcast episodes |
| GET | /api/v2/podcasts/languages | Get the list of Languages that can be used to filter podcasts in the search podcasts request |
| GET | /api/v2/podcasts/countries | Get the list of Countries that can be used to filter podcasts in the search podcasts request |
| GET | /api/v2/podcasts/categories | Get the list of Categories that can be used to filter podcasts in the search podcasts request |

### stats
| Method | Path | Description |
|--------|------|-------------|
| POST | /stats/mounts/{mount}/auth-cache/reload | Retrieve total numer of live stats for a specific mount |
| POST | /stats/mounts/{mount}/auth-cache/reload/all | Retrieve total numer of live stats for a specific mount |
| GET | /stats/mounts/{mount}/live/total | Retrieve total numer of live stats for a specific mount |

### partners
| Method | Path | Description |
|--------|------|-------------|
| POST | /partners/streams | Get the partner information for a list of streams. |
| GET | /partners/{partnerId}/ads/stats | Retrieve partner stats |
| GET | /partners/streams/{streamId} | Get the stream partner information. |
| GET | /partners/streams/{streamId}/tracks | Get the stream partner information. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Get podcast details?" -> GET /api/v2/podcasts/{podcastKey}
- "Update a podcast?" -> PUT /api/v2/podcasts/{podcastKey}
- "Delete a podcast?" -> DELETE /api/v2/podcasts/{podcastKey}
- "Get episode details?" -> GET /api/v2/podcasts/{podcastKey}/episodes/{episodeKey}
- "Update a episode?" -> PUT /api/v2/podcasts/{podcastKey}/episodes/{episodeKey}
- "Delete a episode?" -> DELETE /api/v2/podcasts/{podcastKey}/episodes/{episodeKey}
- "Create a reload?" -> POST /stats/mounts/{mount}/auth-cache/reload
- "Create a all?" -> POST /stats/mounts/{mount}/auth-cache/reload/all
- "Create a stream?" -> POST /partners/streams
- "Create a search?" -> POST /api/v2/stations/search
- "Create a location?" -> POST /api/v2/stations/listener/location
- "Create a create?" -> POST /api/v2/podcasts/{podcastKey}/episodes/create
- "Create a search?" -> POST /api/v2/podcasts/search
- "Create a create?" -> POST /api/v2/podcasts/create
- "List all total?" -> GET /stats/mounts/{mount}/live/total
- "List all stats?" -> GET /partners/{partnerId}/ads/stats
- "Get stream details?" -> GET /partners/streams/{streamId}
- "List all tracks?" -> GET /partners/streams/{streamId}/tracks
- "Get station details?" -> GET /api/v2/stations/{stationKey}
- "List all list?" -> GET /api/v2/stations/list
- "List all languages?" -> GET /api/v2/stations/languages
- "List all genres?" -> GET /api/v2/stations/genres
- "List all countries?" -> GET /api/v2/stations/countries
- "List all browse?" -> GET /api/v2/stations/browse
- "List all episodes?" -> GET /api/v2/podcasts/{podcastKey}/episodes
- "List all languages?" -> GET /api/v2/podcasts/languages
- "List all countries?" -> GET /api/v2/podcasts/countries
- "List all categories?" -> GET /api/v2/podcasts/categories
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
