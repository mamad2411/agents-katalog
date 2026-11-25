---
name: charity-api
description: "Charity API skill. Use when working with Charity for charity_org. Covers 2 endpoints."
version: 1.0.0
generator: lapsh
---

# Charity API
API version: v1.2.1

## Auth
OAuth2

## Base URL
https://api.ebay.com/commerce/charity/v1

## Setup
1. Configure auth: OAuth2
2. GET /charity_org -- verify access

## Endpoints

2 endpoints across 1 groups. See references/api-spec.lap for full details.

### charity_org
| Method | Path | Description |
|--------|------|-------------|
| GET | /charity_org/{charity_org_id} | This call is used to retrieve detailed information about supported charitable organizations. It allows users to retrieve the details for a specific charitable organization using its charity organization ID. |
| GET | /charity_org | This call is used to search for supported charitable organizations. It allows users to search for a specific charitable organization, or for multiple charitable organizations, from a particular charitable domain and/or geographical region, or by using search criteria.<br /><br />The call returns paginated search results containing the charitable organizations that match the specified criteria. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Get charity_org details?" -> GET /charity_org/{charity_org_id}
- "Search charity_org?" -> GET /charity_org
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
