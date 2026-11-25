---
name: proxy-api
description: "Proxy API skill. Use when working with Proxy for proxy. Covers 6 endpoints."
version: 1.0.0
generator: lapsh
---

# Proxy API
API version: 10.24.0

## Auth
ApiKey Authorization in header | ApiKey x-apideck-app-id in header

## Base URL
https://unify.apideck.com

## Setup
1. Set your API key in the appropriate header
2. GET /proxy -- verify access
3. POST /proxy -- create first proxy

## Endpoints

6 endpoints across 1 groups. See references/api-spec.lap for full details.

### proxy
| Method | Path | Description |
|--------|------|-------------|
| GET | /proxy | GET |
| OPTIONS | /proxy | OPTIONS |
| POST | /proxy | POST |
| PUT | /proxy | PUT |
| PATCH | /proxy | PATCH |
| DELETE | /proxy | DELETE |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all proxy?" -> GET /proxy
- "Create a proxy?" -> POST /proxy
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
