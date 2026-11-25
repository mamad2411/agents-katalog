---
name: utilities-management
description: "Utilities Management API skill. Use when working with Utilities Management for utilities. Covers 4 endpoints."
version: 1.0.0
generator: lapsh
---

# Utilities Management

## Auth
ApiKey WM_SEC.ACCESS_TOKEN in header

## Base URL
https://marketplace.walmartapis.com

## Setup
1. Set your API key in the appropriate header
2. GET /v3/utilities/taxonomy -- verify access

## Endpoints

4 endpoints across 1 groups. See references/api-spec.lap for full details.

### utilities
| Method | Path | Description |
|--------|------|-------------|
| GET | /v3/utilities/taxonomy | Taxonomy by spec |
| GET | /v3/utilities/taxonomy/departments | All Departments |
| GET | /v3/utilities/taxonomy/departments/{departmentId} | All Categories |
| GET | /v3/utilities/apiStatus | API Platform Status |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all taxonomy?" -> GET /v3/utilities/taxonomy
- "List all departments?" -> GET /v3/utilities/taxonomy/departments
- "Get department details?" -> GET /v3/utilities/taxonomy/departments/{departmentId}
- "List all apiStatus?" -> GET /v3/utilities/apiStatus
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
