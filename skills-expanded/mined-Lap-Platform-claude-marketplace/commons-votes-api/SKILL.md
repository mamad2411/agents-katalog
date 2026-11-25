---
name: commons-votes-api
description: "Commons Votes API skill. Use when working with Commons Votes for data. Covers 5 endpoints."
version: 1.0.0
generator: lapsh
---

# Commons Votes API
API version: v1

## Auth
No authentication required.

## Base URL
http://commonsvotes-api.parliament.uk

## Setup
1. No auth setup needed
2. GET /data/divisions.{format}/groupedbyparty -- verify access

## Endpoints

5 endpoints across 1 groups. See references/api-spec.lap for full details.

### data
| Method | Path | Description |
|--------|------|-------------|
| GET | /data/division/{divisionId}.{format} | Return a Division |
| GET | /data/divisions.{format}/groupedbyparty | Return Divisions results grouped by party |
| GET | /data/divisions.{format}/membervoting | Return voting records for a Member |
| GET | /data/divisions.{format}/search | Return a list of Divisions |
| GET | /data/divisions.{format}/searchTotalResults | Return total results count |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Get division details?" -> GET /data/division/{divisionId}.{format}
- "List all groupedbyparty?" -> GET /data/divisions.{format}/groupedbyparty
- "List all membervoting?" -> GET /data/divisions.{format}/membervoting
- "List all search?" -> GET /data/divisions.{format}/search
- "List all searchTotalResults?" -> GET /data/divisions.{format}/searchTotalResults

## Response Tips
- Check response schemas in references/api-spec.lap for field details

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
