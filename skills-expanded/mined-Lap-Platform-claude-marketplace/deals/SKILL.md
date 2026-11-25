---
name: deals
description: "Deals API skill. Use when working with Deals for crm. Covers 12 endpoints."
version: 1.0.0
generator: lapsh
---

# Deals
API version: v3

## Auth
OAuth2 | ApiKey private-app-legacy in header | ApiKey private-app in header

## Base URL
https://api.hubapi.com

## Setup
1. Set your API key in the appropriate header
2. GET /crm/v3/objects/0-3 -- verify access
3. POST /crm/v3/objects/0-3 -- create first 0-3

## Endpoints

12 endpoints across 1 groups. See references/api-spec.lap for full details.

### crm
| Method | Path | Description |
|--------|------|-------------|
| GET | /crm/v3/objects/0-3 | List |
| POST | /crm/v3/objects/0-3 | Create |
| POST | /crm/v3/objects/0-3/batch/archive | Archive a batch of deals by ID |
| POST | /crm/v3/objects/0-3/batch/create | Create a batch of deals |
| POST | /crm/v3/objects/0-3/batch/read | Read a batch of deals by internal ID, or unique property values |
| POST | /crm/v3/objects/0-3/batch/update | Update a batch of deals by internal ID, or unique property values |
| POST | /crm/v3/objects/0-3/batch/upsert | Create or update a batch of deals by unique property values |
| POST | /crm/v3/objects/0-3/merge | Merge two deals with same type |
| POST | /crm/v3/objects/0-3/search | Search for deals using various filters and criteria to retrieve specific records. |
| GET | /crm/v3/objects/0-3/{dealId} | Read |
| DELETE | /crm/v3/objects/0-3/{dealId} | Archive |
| PATCH | /crm/v3/objects/0-3/{dealId} | Update |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all 0-3?" -> GET /crm/v3/objects/0-3
- "Create a 0-3?" -> POST /crm/v3/objects/0-3
- "Create a archive?" -> POST /crm/v3/objects/0-3/batch/archive
- "Create a create?" -> POST /crm/v3/objects/0-3/batch/create
- "Create a read?" -> POST /crm/v3/objects/0-3/batch/read
- "Create a update?" -> POST /crm/v3/objects/0-3/batch/update
- "Create a upsert?" -> POST /crm/v3/objects/0-3/batch/upsert
- "Create a merge?" -> POST /crm/v3/objects/0-3/merge
- "Create a search?" -> POST /crm/v3/objects/0-3/search
- "Get 0-3 details?" -> GET /crm/v3/objects/0-3/{dealId}
- "Delete a 0-3?" -> DELETE /crm/v3/objects/0-3/{dealId}
- "Partially update a 0-3?" -> PATCH /crm/v3/objects/0-3/{dealId}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
