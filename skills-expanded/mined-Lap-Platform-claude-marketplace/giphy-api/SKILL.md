---
name: giphy-api
description: "Giphy API skill. Use when working with Giphy for gifs, stickers. Covers 10 endpoints."
version: 1.0.0
generator: lapsh
---

# Giphy API
API version: 1.0

## Auth
ApiKey api_key in query

## Base URL
https://api.giphy.com/v1

## Setup
1. Set your API key in the appropriate header
2. GET /gifs/search -- verify access

## Endpoints

10 endpoints across 2 groups. See references/api-spec.lap for full details.

### gifs
| Method | Path | Description |
|--------|------|-------------|
| GET | /gifs/search | Search GIFs |
| GET | /gifs/trending | Trending GIFs |
| GET | /gifs/translate | Translate phrase to GIF |
| GET | /gifs/random | Random GIF |
| GET | /gifs/{gifId} | Get GIF by Id |
| GET | /gifs | Get GIFs by ID |

### stickers
| Method | Path | Description |
|--------|------|-------------|
| GET | /stickers/search | Search Stickers |
| GET | /stickers/trending | Trending Stickers |
| GET | /stickers/translate | Translate phrase to Sticker |
| GET | /stickers/random | Random Sticker |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Search search?" -> GET /gifs/search
- "List all trending?" -> GET /gifs/trending
- "List all translate?" -> GET /gifs/translate
- "List all random?" -> GET /gifs/random
- "Get gif details?" -> GET /gifs/{gifId}
- "List all gifs?" -> GET /gifs
- "Search search?" -> GET /stickers/search
- "List all trending?" -> GET /stickers/trending
- "List all translate?" -> GET /stickers/translate
- "List all random?" -> GET /stickers/random
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
