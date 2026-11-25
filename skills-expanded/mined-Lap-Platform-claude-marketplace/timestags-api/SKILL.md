---
name: timestags-api
description: "TimesTags API skill. Use when working with TimesTags for timestags. Covers 1 endpoint."
version: 1.0.0
generator: lapsh
---

# TimesTags API
API version: 1.0.0

## Auth
ApiKey api-key in query

## Base URL
http://api.nytimes.com/svc/suggest/v1

## Setup
1. Set your API key in the appropriate header
2. GET /timestags -- verify access

## Endpoints

1 endpoints across 1 groups. See references/api-spec.lap for full details.

### timestags
| Method | Path | Description |
|--------|------|-------------|
| GET | /timestags |  |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Search timestags?" -> GET /timestags
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
