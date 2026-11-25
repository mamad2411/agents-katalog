---
name: archive-api
description: "Archive API skill. Use when working with Archive for {year}. Covers 1 endpoint."
version: 1.0.0
generator: lapsh
---

# Archive API
API version: 1.0.0

## Auth
ApiKey api-key in query

## Base URL
http://api.nytimes.com/svc/archive/v1

## Setup
1. Set your API key in the appropriate header
2. GET /{year}/{month}.json -- verify access

## Endpoints

1 endpoints across 1 groups. See references/api-spec.lap for full details.

### {year}
| Method | Path | Description |
|--------|------|-------------|
| GET | /{year}/{month}.json | Archive API |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
