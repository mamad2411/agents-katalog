---
name: on-demand-flight-status
description: "On-Demand Flight Status API skill. Use when working with On-Demand Flight Status for schedule. Covers 1 endpoint."
version: 1.0.0
generator: lapsh
---

# On-Demand Flight Status
API version: 2.0.2

## Auth
No authentication required.

## Base URL
https://test.api.amadeus.com/v2

## Setup
1. No auth setup needed
2. GET /schedule/flights -- verify access

## Endpoints

1 endpoints across 1 groups. See references/api-spec.lap for full details.

### schedule
| Method | Path | Description |
|--------|------|-------------|
| GET | /schedule/flights | Retrieves a unique flight by search criteria. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all flights?" -> GET /schedule/flights

## Response Tips
- Check response schemas in references/api-spec.lap for field details

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
