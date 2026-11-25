---
name: rawg-video-games-database-api
description: "RAWG Video Games Database API skill. Use when working with RAWG Video Games Database for creator-roles, creators, developers. Covers 30 endpoints."
version: 1.0.0
generator: lapsh
---

# RAWG Video Games Database API
API version: v1.0

## Auth
ApiKey (inferred from docs)

## Base URL
https://api.rawg.io/api

## Setup
1. Set your API key in the appropriate header
2. GET /creator-roles -- verify access

## Endpoints

30 endpoints across 9 groups. See references/api-spec.lap for full details.

### creator-roles
| Method | Path | Description |
|--------|------|-------------|
| GET | /creator-roles | Get a list of creator positions (jobs). |

### creators
| Method | Path | Description |
|--------|------|-------------|
| GET | /creators | Get a list of game creators. |
| GET | /creators/{id} | Get details of the creator. |

### developers
| Method | Path | Description |
|--------|------|-------------|
| GET | /developers | Get a list of game developers. |
| GET | /developers/{id} | Get details of the developer. |

### games
| Method | Path | Description |
|--------|------|-------------|
| GET | /games | Get a list of games. |
| GET | /games/{game_pk}/additions | Get a list of DLC's for the game, GOTY and other editions, companion apps, etc. |
| GET | /games/{game_pk}/development-team | Get a list of individual creators that were part of the development team. |
| GET | /games/{game_pk}/game-series | Get a list of games that are part of the same series. |
| GET | /games/{game_pk}/parent-games | Get a list of parent games for DLC's and editions. |
| GET | /games/{game_pk}/screenshots | Get screenshots for the game. |
| GET | /games/{game_pk}/stores | Get links to the stores that sell the game. |
| GET | /games/{id} | Get details of the game. |
| GET | /games/{id}/achievements | Get a list of game achievements. |
| GET | /games/{id}/movies | Get a list of game trailers. |
| GET | /games/{id}/reddit | Get a list of most recent posts from the game's subreddit. |
| GET | /games/{id}/suggested | Get a list of visually similar games, available only for business and enterprise API users. |
| GET | /games/{id}/twitch | Get streams on Twitch associated with the game, available only for business and enterprise API users. |
| GET | /games/{id}/youtube | Get videos from YouTube associated with the game, available only for business and enterprise API users. |

### genres
| Method | Path | Description |
|--------|------|-------------|
| GET | /genres | Get a list of video game genres. |
| GET | /genres/{id} | Get details of the genre. |

### platforms
| Method | Path | Description |
|--------|------|-------------|
| GET | /platforms | Get a list of video game platforms. |
| GET | /platforms/lists/parents | Get a list of parent platforms. |
| GET | /platforms/{id} | Get details of the platform. |

### publishers
| Method | Path | Description |
|--------|------|-------------|
| GET | /publishers | Get a list of video game publishers. |
| GET | /publishers/{id} | Get details of the publisher. |

### stores
| Method | Path | Description |
|--------|------|-------------|
| GET | /stores | Get a list of video game storefronts. |
| GET | /stores/{id} | Get details of the store. |

### tags
| Method | Path | Description |
|--------|------|-------------|
| GET | /tags | Get a list of tags. |
| GET | /tags/{id} | Get details of the tag. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all creator-roles?" -> GET /creator-roles
- "List all creators?" -> GET /creators
- "Get creator details?" -> GET /creators/{id}
- "List all developers?" -> GET /developers
- "Get developer details?" -> GET /developers/{id}
- "Search games?" -> GET /games
- "List all additions?" -> GET /games/{game_pk}/additions
- "List all development-team?" -> GET /games/{game_pk}/development-team
- "List all game-series?" -> GET /games/{game_pk}/game-series
- "List all parent-games?" -> GET /games/{game_pk}/parent-games
- "List all screenshots?" -> GET /games/{game_pk}/screenshots
- "List all stores?" -> GET /games/{game_pk}/stores
- "Get game details?" -> GET /games/{id}
- "List all achievements?" -> GET /games/{id}/achievements
- "List all movies?" -> GET /games/{id}/movies
- "List all reddit?" -> GET /games/{id}/reddit
- "List all suggested?" -> GET /games/{id}/suggested
- "List all twitch?" -> GET /games/{id}/twitch
- "List all youtube?" -> GET /games/{id}/youtube
- "List all genres?" -> GET /genres
- "Get genre details?" -> GET /genres/{id}
- "List all platforms?" -> GET /platforms
- "List all parents?" -> GET /platforms/lists/parents
- "Get platform details?" -> GET /platforms/{id}
- "List all publishers?" -> GET /publishers
- "Get publisher details?" -> GET /publishers/{id}
- "List all stores?" -> GET /stores
- "Get store details?" -> GET /stores/{id}
- "List all tags?" -> GET /tags
- "Get tag details?" -> GET /tags/{id}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
