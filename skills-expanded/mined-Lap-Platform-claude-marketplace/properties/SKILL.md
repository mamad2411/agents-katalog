---
name: properties
description: "Properties API skill. Use when working with Properties for crm. Covers 13 endpoints."
version: 1.0.0
generator: lapsh
---

# Properties
API version: v3

## Auth
OAuth2 | ApiKey private-app-legacy in header | ApiKey private-app in header

## Base URL
https://api.hubapi.com

## Setup
1. Set your API key in the appropriate header
2. GET /crm/v3/properties/{objectType}/groups -- verify access
3. POST /crm/v3/properties/{objectType} -- create first properties

## Endpoints

13 endpoints across 1 groups. See references/api-spec.lap for full details.

### crm
| Method | Path | Description |
|--------|------|-------------|
| GET | /crm/v3/properties/{objectType} | Read all properties |
| POST | /crm/v3/properties/{objectType} | Create a property |
| POST | /crm/v3/properties/{objectType}/batch/archive | Archive a batch of properties |
| POST | /crm/v3/properties/{objectType}/batch/create | Create a batch of properties |
| POST | /crm/v3/properties/{objectType}/batch/read | Read a batch of properties |
| GET | /crm/v3/properties/{objectType}/groups | Read all property groups |
| POST | /crm/v3/properties/{objectType}/groups | Create a property group |
| GET | /crm/v3/properties/{objectType}/groups/{groupName} | Read a property group |
| DELETE | /crm/v3/properties/{objectType}/groups/{groupName} | Archive a property group |
| PATCH | /crm/v3/properties/{objectType}/groups/{groupName} | Update a property group |
| GET | /crm/v3/properties/{objectType}/{propertyName} | Read a property |
| DELETE | /crm/v3/properties/{objectType}/{propertyName} | Archive a property |
| PATCH | /crm/v3/properties/{objectType}/{propertyName} | Update a property |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Get property details?" -> GET /crm/v3/properties/{objectType}
- "Create a archive?" -> POST /crm/v3/properties/{objectType}/batch/archive
- "Create a create?" -> POST /crm/v3/properties/{objectType}/batch/create
- "Create a read?" -> POST /crm/v3/properties/{objectType}/batch/read
- "List all groups?" -> GET /crm/v3/properties/{objectType}/groups
- "Create a group?" -> POST /crm/v3/properties/{objectType}/groups
- "Get group details?" -> GET /crm/v3/properties/{objectType}/groups/{groupName}
- "Delete a group?" -> DELETE /crm/v3/properties/{objectType}/groups/{groupName}
- "Partially update a group?" -> PATCH /crm/v3/properties/{objectType}/groups/{groupName}
- "Get property details?" -> GET /crm/v3/properties/{objectType}/{propertyName}
- "Delete a property?" -> DELETE /crm/v3/properties/{objectType}/{propertyName}
- "Partially update a property?" -> PATCH /crm/v3/properties/{objectType}/{propertyName}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
