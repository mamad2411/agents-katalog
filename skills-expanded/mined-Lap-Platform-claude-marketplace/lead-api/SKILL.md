---
name: lead-api
description: "Lead API skill. Use when working with Lead for lead. Covers 5 endpoints."
version: 1.0.0
generator: lapsh
---

# Lead API
API version: 10.24.0

## Auth
ApiKey Authorization in header | ApiKey x-apideck-app-id in header | ApiKey x-apideck-consumer-id in header

## Base URL
https://unify.apideck.com

## Setup
1. Set your API key in the appropriate header
2. GET /lead/leads -- verify access
3. POST /lead/leads -- create first leads

## Endpoints

5 endpoints across 1 groups. See references/api-spec.lap for full details.

### lead
| Method | Path | Description |
|--------|------|-------------|
| GET | /lead/leads | List leads |
| POST | /lead/leads | Create lead |
| GET | /lead/leads/{id} | Get lead |
| PATCH | /lead/leads/{id} | Update lead |
| DELETE | /lead/leads/{id} | Delete lead |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all leads?" -> GET /lead/leads
- "Create a lead?" -> POST /lead/leads
- "Get lead details?" -> GET /lead/leads/{id}
- "Partially update a lead?" -> PATCH /lead/leads/{id}
- "Delete a lead?" -> DELETE /lead/leads/{id}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
