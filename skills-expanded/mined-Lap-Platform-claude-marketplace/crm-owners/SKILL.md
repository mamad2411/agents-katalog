---
name: crm-owners
description: "Crm Owners API skill. Use when working with Crm Owners for crm. Covers 2 endpoints."
version: 1.0.0
generator: lapsh
---

# Crm Owners
API version: v3

## Auth
OAuth2 | ApiKey private-app-legacy in header | ApiKey private-app in header

## Base URL
https://api.hubapi.com

## Setup
1. Set your API key in the appropriate header
2. GET /crm/v3/owners/ -- verify access

## Endpoints

2 endpoints across 1 groups. See references/api-spec.lap for full details.

### crm
| Method | Path | Description |
|--------|------|-------------|
| GET | /crm/v3/owners/ | Retrieve a paginated list of owners available in the account. |
| GET | /crm/v3/owners/{ownerId} | Retrieve a specific owner by ID |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all owners?" -> GET /crm/v3/owners/
- "Get owner details?" -> GET /crm/v3/owners/{ownerId}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
