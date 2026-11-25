---
name: discovery-api
description: "Discovery API skill. Use when working with Discovery for discovery. Covers 13 endpoints."
version: 1.0.0
generator: lapsh
---

# Discovery API
API version: v2

## Auth
No authentication required.

## Base URL
https://www.ticketmaster.com/discovery/v2

## Setup
1. No auth setup needed
2. GET /discovery/v2/attractions -- verify access

## Endpoints

13 endpoints across 1 groups. See references/api-spec.lap for full details.

### discovery
| Method | Path | Description |
|--------|------|-------------|
| GET | /discovery/v2/attractions | Attraction Search |
| GET | /discovery/v2/attractions/{id} | Get Attraction Details |
| GET | /discovery/v2/classifications | Classification Search |
| GET | /discovery/v2/classifications/genres/{id} | Get Genre Details |
| GET | /discovery/v2/classifications/segments/{id} | Get Segment Details |
| GET | /discovery/v2/classifications/subgenres/{id} | Get Sub-Genre Details |
| GET | /discovery/v2/classifications/{id} | Get Classification Details |
| GET | /discovery/v2/events | Event Search |
| GET | /discovery/v2/events/{id} | Get Event Details |
| GET | /discovery/v2/events/{id}/images | Get Event Images |
| GET | /discovery/v2/suggest | Find Suggest |
| GET | /discovery/v2/venues | Venue Search |
| GET | /discovery/v2/venues/{id} | Get Venue Details |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all attractions?" -> GET /discovery/v2/attractions
- "Get attraction details?" -> GET /discovery/v2/attractions/{id}
- "List all classifications?" -> GET /discovery/v2/classifications
- "Get genre details?" -> GET /discovery/v2/classifications/genres/{id}
- "Get segment details?" -> GET /discovery/v2/classifications/segments/{id}
- "Get subgenre details?" -> GET /discovery/v2/classifications/subgenres/{id}
- "Get classification details?" -> GET /discovery/v2/classifications/{id}
- "List all events?" -> GET /discovery/v2/events
- "Get event details?" -> GET /discovery/v2/events/{id}
- "List all images?" -> GET /discovery/v2/events/{id}/images
- "List all suggest?" -> GET /discovery/v2/suggest
- "List all venues?" -> GET /discovery/v2/venues
- "Get venue details?" -> GET /discovery/v2/venues/{id}

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
