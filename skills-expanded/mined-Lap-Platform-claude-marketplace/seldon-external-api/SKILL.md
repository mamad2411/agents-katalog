---
name: seldon-external-api
description: "Seldon External API skill. Use when working with Seldon External for seldon. Covers 2 endpoints."
version: 1.0.0
generator: lapsh
---

# Seldon External API
API version: 0.1

## Auth
Bearer bearer

## Base URL
https://localhost:80

## Setup
1. Set Authorization header with your Bearer token
3. POST /seldon/{namespace}/{deployment}/api/v1.0/predictions -- create first predictions

## Endpoints

2 endpoints across 1 groups. See references/api-spec.lap for full details.

### seldon
| Method | Path | Description |
|--------|------|-------------|
| POST | /seldon/{namespace}/{deployment}/api/v1.0/predictions |  |
| POST | /seldon/{namespace}/{deployment}/api/v1.0/feedback |  |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a prediction?" -> POST /seldon/{namespace}/{deployment}/api/v1.0/predictions
- "Create a feedback?" -> POST /seldon/{namespace}/{deployment}/api/v1.0/feedback
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
