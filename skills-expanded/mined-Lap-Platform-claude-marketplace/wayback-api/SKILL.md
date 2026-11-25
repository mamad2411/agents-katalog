---
name: wayback-api
description: "Wayback API skill. Use when working with Wayback for wayback. Covers 2 endpoints."
version: 1.0.0
generator: lapsh
---

# Wayback API
API version: 1.0.0

## Auth
No authentication required.

## Base URL
https://api.archive.org/

## Setup
1. No auth setup needed
2. GET /wayback/v1/available -- verify access
3. POST /wayback/v1/available -- create first available

## Endpoints

2 endpoints across 1 groups. See references/api-spec.lap for full details.

### wayback
| Method | Path | Description |
|--------|------|-------------|
| GET | /wayback/v1/available |  |
| POST | /wayback/v1/available |  |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all available?" -> GET /wayback/v1/available
- "Create a available?" -> POST /wayback/v1/available

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
