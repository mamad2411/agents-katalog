---
name: scim-provisioning-overview
description: "SCIM Provisioning Overview API skill. Use when working with SCIM Provisioning Overview for resources. Covers 5 endpoints."
version: 1.0.0
generator: lapsh
---

# SCIM Provisioning Overview

## Auth
Bearer bearer

## Base URL
https://api.frontegg.com/directory

## Setup
1. Set Authorization header with your Bearer token
2. GET /resources/v1/configurations/scim2 -- verify access
3. POST /resources/v1/configurations/scim2 -- create first scim2

## Endpoints

5 endpoints across 1 groups. See references/api-spec.lap for full details.

### resources
| Method | Path | Description |
|--------|------|-------------|
| GET | /resources/v1/configurations/scim2 | Get all SCIM configurations |
| POST | /resources/v1/configurations/scim2 | Create a SCIM configuration |
| GET | /resources/v1/configurations/scim2/{id} | Get a SCIM configuration by ID |
| PATCH | /resources/v1/configurations/scim2/{id} | Update a SCIM configuration |
| DELETE | /resources/v1/configurations/scim2/{id} | Delete a SCIM configuration |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all scim2?" -> GET /resources/v1/configurations/scim2
- "Create a scim2?" -> POST /resources/v1/configurations/scim2
- "Get scim2 details?" -> GET /resources/v1/configurations/scim2/{id}
- "Partially update a scim2?" -> PATCH /resources/v1/configurations/scim2/{id}
- "Delete a scim2?" -> DELETE /resources/v1/configurations/scim2/{id}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
