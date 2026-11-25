---
name: lords-votes-api
description: "Lords Votes API skill. Use when working with Lords Votes for data. Covers 5 endpoints."
version: 1.0.0
generator: lapsh
---

# Lords Votes API
API version: v1

## Auth
No authentication required.

## Base URL
Not specified.

## Setup
1. No auth setup needed
2. GET /data/Divisions/searchTotalResults -- verify access

## Endpoints

5 endpoints across 1 groups. See references/api-spec.lap for full details.

### data
| Method | Path | Description |
|--------|------|-------------|
| GET | /data/Divisions/{divisionId} | Return a Division |
| GET | /data/Divisions/searchTotalResults | Return total results count |
| GET | /data/Divisions/search | Return a list of Divisions |
| GET | /data/Divisions/membervoting | Return voting records for a Member |
| GET | /data/Divisions/groupedbyparty | Return Divisions results grouped by party |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Get Division details?" -> GET /data/Divisions/{divisionId}
- "List all searchTotalResults?" -> GET /data/Divisions/searchTotalResults
- "List all search?" -> GET /data/Divisions/search
- "List all membervoting?" -> GET /data/Divisions/membervoting
- "List all groupedbyparty?" -> GET /data/Divisions/groupedbyparty

## Response Tips
- Check response schemas in references/api-spec.lap for field details

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
