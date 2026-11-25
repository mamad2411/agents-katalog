---
name: searchly-api-v1
description: "SearchLy API v1 API skill. Use when working with SearchLy API v1 for similarity, song. Covers 3 endpoints."
version: 1.0.0
generator: lapsh
---

# SearchLy API v1
API version: 1.0

## Auth
No authentication required.

## Base URL
https://searchly.asuarez.dev/api/v1

## Setup
1. No auth setup needed
2. GET /similarity/by_song -- verify access
3. POST /similarity/by_content -- create first by_content

## Endpoints

3 endpoints across 2 groups. See references/api-spec.lap for full details.

### similarity
| Method | Path | Description |
|--------|------|-------------|
| GET | /similarity/by_song | API endpoint to search similarity using a song identifier |
| POST | /similarity/by_content | API endpoint to search similarity using content |

### song
| Method | Path | Description |
|--------|------|-------------|
| GET | /song/search | API endpoint to search songs from the database given a query |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all by_song?" -> GET /similarity/by_song
- "Create a by_content?" -> POST /similarity/by_content
- "Search search?" -> GET /song/search

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
