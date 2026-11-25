---
name: deed-api
description: "Deed API skill. Use when working with Deed for deed. Covers 2 endpoints."
version: 1.0.0
generator: lapsh
---

# Deed API
API version: 1.0.0

## Auth
No authentication required.

## Base URL
https://api.landregistry.gov.uk/v1

## Setup
1. No auth setup needed
2. GET /deed/{deed_reference} -- verify access
3. POST /deed/ -- create first deed

## Endpoints

2 endpoints across 1 groups. See references/api-spec.lap for full details.

### deed
| Method | Path | Description |
|--------|------|-------------|
| POST | /deed/ | Deed |
| GET | /deed/{deed_reference} | Deed |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a deed?" -> POST /deed/
- "Get deed details?" -> GET /deed/{deed_reference}

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
