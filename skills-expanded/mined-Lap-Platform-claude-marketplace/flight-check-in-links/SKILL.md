---
name: flight-check-in-links
description: "Flight Check-in Links API skill. Use when working with Flight Check-in Links for reference-data. Covers 1 endpoint."
version: 1.0.0
generator: lapsh
---

# Flight Check-in Links
API version: 2.1.3

## Auth
No authentication required.

## Base URL
https://test.api.amadeus.com/v2

## Setup
1. No auth setup needed
2. GET /reference-data/urls/checkin-links -- verify access

## Endpoints

1 endpoints across 1 groups. See references/api-spec.lap for full details.

### reference-data
| Method | Path | Description |
|--------|------|-------------|
| GET | /reference-data/urls/checkin-links | Lists Check-in URLs. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all checkin-links?" -> GET /reference-data/urls/checkin-links

## Response Tips
- Check response schemas in references/api-spec.lap for field details

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
