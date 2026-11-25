---
name: onsched-api-utility
description: "OnSched API Utility API skill. Use when working with OnSched API Utility for utility. Covers 2 endpoints."
version: 1.0.0
generator: lapsh
---

# OnSched API Utility
API version: v1

## Auth
OAuth2

## Base URL
https://sandbox-api.onsched.com/

## Setup
1. Configure auth: OAuth2
2. GET /utility/v1/health/heartbeat -- verify access

## Endpoints

2 endpoints across 1 groups. See references/api-spec.lap for full details.

### utility
| Method | Path | Description |
|--------|------|-------------|
| GET | /utility/v1/health/heartbeat |  |
| GET | /utility/v1/health/threadinfo |  |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all heartbeat?" -> GET /utility/v1/health/heartbeat
- "List all threadinfo?" -> GET /utility/v1/health/threadinfo
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
