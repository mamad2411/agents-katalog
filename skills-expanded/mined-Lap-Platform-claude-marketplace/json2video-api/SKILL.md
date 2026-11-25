---
name: json2video-api
description: "JSON2Video API skill. Use when working with JSON2Video for movies. Covers 2 endpoints."
version: 1.0.0
generator: lapsh
---

# JSON2Video API
API version: 2.0.0

## Auth
No authentication required.

## Base URL
https://api.json2video.com/v2

## Setup
1. No auth setup needed
2. GET /movies -- verify access
3. POST /movies -- create first movies

## Endpoints

2 endpoints across 1 groups. See references/api-spec.lap for full details.

### movies
| Method | Path | Description |
|--------|------|-------------|
| GET | /movies | Get the status of your movies |
| POST | /movies | Create a new movie |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all movies?" -> GET /movies
- "Create a movy?" -> POST /movies

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
