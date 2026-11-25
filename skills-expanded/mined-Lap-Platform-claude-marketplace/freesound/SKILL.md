---
name: freesound
description: "Freesound API skill. Use when working with Freesound for search, sounds. Covers 2 endpoints."
version: 1.0.0
generator: lapsh
---

# Freesound
API version: 2.0.0

## Auth
No authentication required.

## Base URL
http://www.freesound.org/apiv2

## Setup
1. No auth setup needed
2. GET /search/text -- verify access

## Endpoints

2 endpoints across 2 groups. See references/api-spec.lap for full details.

### search
| Method | Path | Description |
|--------|------|-------------|
| GET | /search/text | Search sounds |

### sounds
| Method | Path | Description |
|--------|------|-------------|
| GET | /sounds/{soundId} | Details of a sound |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Search text?" -> GET /search/text
- "Get sound details?" -> GET /sounds/{soundId}

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
