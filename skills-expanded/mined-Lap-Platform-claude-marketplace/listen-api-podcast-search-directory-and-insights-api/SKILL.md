---
name: listen-api-podcast-search-directory-and-insights-api
description: "Listen API: Podcast Search, Directory, and Insights API skill. Use when working with Listen API: Podcast Search, Directory, and Insights for search, typeahead, search_episode_titles. Covers 26 endpoints."
version: 1.0.0
generator: lapsh
---

# Listen API: Podcast Search, Directory, and Insights API
API version: 2.0

## Auth
ApiKey X-ListenAPI-Key in header

## Base URL
https://listen-api.listennotes.com/api/v2

## Setup
1. Set your API key in the appropriate header
2. GET /search -- verify access
3. POST /episodes -- create first episodes

## Endpoints

26 endpoints across 15 groups. See references/api-spec.lap for full details.

### search
| Method | Path | Description |
|--------|------|-------------|
| GET | /search | Full-text search |

### typeahead
| Method | Path | Description |
|--------|------|-------------|
| GET | /typeahead | Typeahead search |

### search_episode_titles
| Method | Path | Description |
|--------|------|-------------|
| GET | /search_episode_titles | Find individual episodes by searching for their titles |

### trending_searches
| Method | Path | Description |
|--------|------|-------------|
| GET | /trending_searches | Fetch trending search terms |

### related_searches
| Method | Path | Description |
|--------|------|-------------|
| GET | /related_searches | Fetch related search terms |

### spellcheck
| Method | Path | Description |
|--------|------|-------------|
| GET | /spellcheck | Spell check on a search term |

### best_podcasts
| Method | Path | Description |
|--------|------|-------------|
| GET | /best_podcasts | Fetch a list of best podcasts by genre |

### podcasts
| Method | Path | Description |
|--------|------|-------------|
| GET | /podcasts/{id} | Fetch detailed meta data and episodes for a podcast by id |
| DELETE | /podcasts/{id} | Request to delete a podcast |
| POST | /podcasts | Batch fetch basic meta data for podcasts |
| GET | /podcasts/{id}/recommendations | Fetch recommendations for a podcast |
| POST | /podcasts/submit | Submit a podcast to Listen Notes database |
| POST | /podcasts/{id}/rss | Refresh RSS feed of a podcast |
| GET | /podcasts/{id}/audience | Fetch audience demographics for a podcast |
| GET | /podcasts/domains/{domain_name} | Fetch podcasts by a publisher's domain name |

### episodes
| Method | Path | Description |
|--------|------|-------------|
| GET | /episodes/{id} | Fetch detailed meta data for an episode by id |
| POST | /episodes | Batch fetch basic meta data for episodes |
| GET | /episodes/{id}/recommendations | Fetch recommendations for an episode |

### curated_podcasts
| Method | Path | Description |
|--------|------|-------------|
| GET | /curated_podcasts/{id} | Fetch a curated list of podcasts by id |
| GET | /curated_podcasts | Fetch curated lists of podcasts |

### genres
| Method | Path | Description |
|--------|------|-------------|
| GET | /genres | Fetch a list of podcast genres |

### regions
| Method | Path | Description |
|--------|------|-------------|
| GET | /regions | Fetch a list of supported countries/regions for best podcasts |

### languages
| Method | Path | Description |
|--------|------|-------------|
| GET | /languages | Fetch a list of supported languages for podcasts |

### just_listen
| Method | Path | Description |
|--------|------|-------------|
| GET | /just_listen | Fetch a random podcast episode |

### playlists
| Method | Path | Description |
|--------|------|-------------|
| GET | /playlists/{id} | Fetch a playlist's info and items (i.e., episodes or podcasts). |
| GET | /playlists | Fetch a list of your playlists. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Search search?" -> GET /search
- "Search typeahead?" -> GET /typeahead
- "Search search_episode_titles?" -> GET /search_episode_titles
- "List all trending_searches?" -> GET /trending_searches
- "Search related_searches?" -> GET /related_searches
- "Search spellcheck?" -> GET /spellcheck
- "List all best_podcasts?" -> GET /best_podcasts
- "Get podcast details?" -> GET /podcasts/{id}
- "Delete a podcast?" -> DELETE /podcasts/{id}
- "Get episode details?" -> GET /episodes/{id}
- "Create a episode?" -> POST /episodes
- "Create a podcast?" -> POST /podcasts
- "Get curated_podcast details?" -> GET /curated_podcasts/{id}
- "List all genres?" -> GET /genres
- "List all regions?" -> GET /regions
- "List all languages?" -> GET /languages
- "List all just_listen?" -> GET /just_listen
- "List all curated_podcasts?" -> GET /curated_podcasts
- "List all recommendations?" -> GET /podcasts/{id}/recommendations
- "List all recommendations?" -> GET /episodes/{id}/recommendations
- "Create a submit?" -> POST /podcasts/submit
- "Create a rss?" -> POST /podcasts/{id}/rss
- "Get playlist details?" -> GET /playlists/{id}
- "List all playlists?" -> GET /playlists
- "List all audience?" -> GET /podcasts/{id}/audience
- "Get domain details?" -> GET /podcasts/domains/{domain_name}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
