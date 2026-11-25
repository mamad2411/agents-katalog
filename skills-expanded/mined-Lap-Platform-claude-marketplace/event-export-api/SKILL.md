---
name: event-export-api
description: "Event Export API skill. Use when working with Event Export for export. Covers 1 endpoint."
version: 1.0.0
generator: lapsh
---

# Event Export API
API version: 1.0.0

## Auth
No authentication required.

## Base URL
Not specified.

## Setup
1. No auth setup needed
2. GET /export -- verify access

## Endpoints

1 endpoints across 1 groups. See references/api-spec.lap for full details.

### export
| Method | Path | Description |
|--------|------|-------------|
| GET | /export | Download Data |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all export?" -> GET /export

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
