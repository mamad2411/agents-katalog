---
name: medcorder-nearby-doctor-api
description: "Medcorder Nearby Doctor API skill. Use when working with Medcorder Nearby Doctor for doctors. Covers 1 endpoint."
version: 1.0.0
generator: lapsh
---

# Medcorder Nearby Doctor API
API version: 1.0.0

## Auth
No authentication required.

## Base URL
https://api.medcorder.com

## Setup
1. No auth setup needed
2. GET /doctors -- verify access

## Endpoints

1 endpoints across 1 groups. See references/api-spec.lap for full details.

### doctors
| Method | Path | Description |
|--------|------|-------------|
| GET | /doctors | Fetch a list of nearby medical providers |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Search doctors?" -> GET /doctors

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
