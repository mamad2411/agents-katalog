---
name: community-api
description: "Community API skill. Use when working with Community for user-content. Covers 4 endpoints."
version: 1.0.0
generator: lapsh
---

# Community API
API version: 3.0.0

## Auth
ApiKey api-key in query

## Base URL
http://api.nytimes.com/svc/community/v3

## Setup
1. Set your API key in the appropriate header
2. GET /user-content/recent.json -- verify access

## Endpoints

4 endpoints across 1 groups. See references/api-spec.lap for full details.

### user-content
| Method | Path | Description |
|--------|------|-------------|
| GET | /user-content/recent.json | Recent User Comments |
| GET | /user-content/url.json | Comments by URL |
| GET | /user-content/by-date.json | Comments by Date |
| GET | /user-content/user.json | Comments by User |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all recent.json?" -> GET /user-content/recent.json
- "List all url.json?" -> GET /user-content/url.json
- "List all by-date.json?" -> GET /user-content/by-date.json
- "List all user.json?" -> GET /user-content/user.json
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
