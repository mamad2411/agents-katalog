---
name: associations
description: "Associations API skill. Use when working with Associations for crm. Covers 10 endpoints."
version: 1.0.0
generator: lapsh
---

# Associations
API version: v4

## Auth
OAuth2 | OAuth2 | ApiKey private-app-legacy in header | ApiKey private-app in header

## Base URL
https://api.hubapi.com

## Setup
1. Set your API key in the appropriate header
2. GET /crm/v4/objects/{objectType}/{objectId}/associations/{toObjectType} -- verify access
3. POST /crm/v4/associations/usage/high-usage-report/{userId} -- create first high-usage-report

## Endpoints

10 endpoints across 1 groups. See references/api-spec.lap for full details.

### crm
| Method | Path | Description |
|--------|------|-------------|
| POST | /crm/v4/associations/usage/high-usage-report/{userId} | Report high usage |
| POST | /crm/v4/associations/{fromObjectType}/{toObjectType}/batch/archive | Remove associations |
| POST | /crm/v4/associations/{fromObjectType}/{toObjectType}/batch/associate/default | Associate records (default) |
| POST | /crm/v4/associations/{fromObjectType}/{toObjectType}/batch/create | Associate records (labelled) |
| POST | /crm/v4/associations/{fromObjectType}/{toObjectType}/batch/labels/archive | Delete specific labels |
| POST | /crm/v4/associations/{fromObjectType}/{toObjectType}/batch/read | Retrieve associations |
| PUT | /crm/v4/objects/{fromObjectType}/{fromObjectId}/associations/default/{toObjectType}/{toObjectId} | Associate records (default) |
| GET | /crm/v4/objects/{objectType}/{objectId}/associations/{toObjectType} | Retrieve all associations by object type |
| PUT | /crm/v4/objects/{objectType}/{objectId}/associations/{toObjectType}/{toObjectId} | Associate records (labelled) |
| DELETE | /crm/v4/objects/{objectType}/{objectId}/associations/{toObjectType}/{toObjectId} | Delete associations between two records |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a archive?" -> POST /crm/v4/associations/{fromObjectType}/{toObjectType}/batch/archive
- "Create a default?" -> POST /crm/v4/associations/{fromObjectType}/{toObjectType}/batch/associate/default
- "Create a create?" -> POST /crm/v4/associations/{fromObjectType}/{toObjectType}/batch/create
- "Create a archive?" -> POST /crm/v4/associations/{fromObjectType}/{toObjectType}/batch/labels/archive
- "Create a read?" -> POST /crm/v4/associations/{fromObjectType}/{toObjectType}/batch/read
- "Update a default?" -> PUT /crm/v4/objects/{fromObjectType}/{fromObjectId}/associations/default/{toObjectType}/{toObjectId}
- "Get association details?" -> GET /crm/v4/objects/{objectType}/{objectId}/associations/{toObjectType}
- "Update a association?" -> PUT /crm/v4/objects/{objectType}/{objectId}/associations/{toObjectType}/{toObjectId}
- "Delete a association?" -> DELETE /crm/v4/objects/{objectType}/{objectId}/associations/{toObjectType}/{toObjectId}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
