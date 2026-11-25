---
name: returns-management
description: "Returns Management API skill. Use when working with Returns Management for returns, feeds. Covers 3 endpoints."
version: 1.0.0
generator: lapsh
---

# Returns Management

## Auth
ApiKey WM_SEC.ACCESS_TOKEN in header

## Base URL
https://marketplace.walmartapis.com

## Setup
1. Set your API key in the appropriate header
2. GET /v3/returns -- verify access
3. POST /v3/returns/{returnOrderId}/refund -- create first refund

## Endpoints

3 endpoints across 2 groups. See references/api-spec.lap for full details.

### returns
| Method | Path | Description |
|--------|------|-------------|
| POST | /v3/returns/{returnOrderId}/refund | Issue refund |
| GET | /v3/returns | Returns |

### feeds
| Method | Path | Description |
|--------|------|-------------|
| POST | /v3/feeds | Return Item Overrides |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a refund?" -> POST /v3/returns/{returnOrderId}/refund
- "Create a feed?" -> POST /v3/feeds
- "List all returns?" -> GET /v3/returns
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
