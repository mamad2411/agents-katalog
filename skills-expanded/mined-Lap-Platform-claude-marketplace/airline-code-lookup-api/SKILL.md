---
name: airline-code-lookup-api
description: "Airline Code Lookup API skill. Use when working with Airline Code Lookup for reference-data. Covers 1 endpoint."
version: 1.0.0
generator: lapsh
---

# Airline Code Lookup API
API version: 1.2.1

## Auth
No authentication required.

## Base URL
https://test.api.amadeus.com/v1

## Setup
1. No auth setup needed
2. GET /reference-data/airlines -- verify access

## Endpoints

1 endpoints across 1 groups. See references/api-spec.lap for full details.

### reference-data
| Method | Path | Description |
|--------|------|-------------|
| GET | /reference-data/airlines | Return airlines information. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all airlines?" -> GET /reference-data/airlines

## Response Tips
- Check response schemas in references/api-spec.lap for field details

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
