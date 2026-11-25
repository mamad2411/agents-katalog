---
name: servicenow-table-api
description: "ServiceNow Table API skill. Use when working with ServiceNow Table for now. Covers 1 endpoint."
version: 1.0.0
generator: lapsh
---

# ServiceNow Table API
API version: 1.0.0

## Auth
ApiKey JSESSIONID in cookie | ApiKey X-UserToken in header

## Base URL
Not specified.

## Setup
1. Set your API key in the appropriate header
2. GET /now/table/{tableName} -- verify access

## Endpoints

1 endpoints across 1 groups. See references/api-spec.lap for full details.

### now
| Method | Path | Description |
|--------|------|-------------|
| GET | /now/table/{tableName} | Retrieves multiple records for the specified table. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Get table details?" -> GET /now/table/{tableName}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
