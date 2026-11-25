---
name: city-of-surrey-open511-api
description: "City of Surrey Open511 API skill. Use when working with City of Surrey Open511 for events, jurisdiction, jurisdictiongeography. Covers 4 endpoints."
version: 1.0.0
generator: lapsh
---

# City of Surrey Open511 API
API version: 0.1

## Auth
No authentication required.

## Base URL
http://data.surrey.ca/open511

## Setup
1. No auth setup needed
2. GET /events -- verify access

## Endpoints

4 endpoints across 4 groups. See references/api-spec.lap for full details.

### events
| Method | Path | Description |
|--------|------|-------------|
| GET | /events | Provides real time traffic obstruction events.  The event resource provides information about road events (constructions, special events, etc.). |

### jurisdiction
| Method | Path | Description |
|--------|------|-------------|
| GET | /jurisdiction | Lists the jurisdictions publishing data through this Open511 API implementation. |

### jurisdictiongeography
| Method | Path | Description |
|--------|------|-------------|
| GET | /jurisdictiongeography | Provides the geographical boundaries for all the jurisdictions. |

### areas
| Method | Path | Description |
|--------|------|-------------|
| GET | /areas | Provides the geographical boundaries for all the jurisdictions. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all events?" -> GET /events
- "List all jurisdiction?" -> GET /jurisdiction
- "List all jurisdictiongeography?" -> GET /jurisdictiongeography
- "List all areas?" -> GET /areas

## Response Tips
- Check response schemas in references/api-spec.lap for field details

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
