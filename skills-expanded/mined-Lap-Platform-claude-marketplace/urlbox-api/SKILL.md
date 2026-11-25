---
name: urlbox-api
description: "Urlbox API skill. Use when working with Urlbox for render. Covers 1 endpoint."
version: 1.0.0
generator: lapsh
---

# Urlbox API
API version: v1

## Auth
Bearer bearer

## Base URL
https://api.urlbox.io

## Setup
1. Set Authorization header with your Bearer token
3. POST /v1/render/sync -- create first sync

## Endpoints

1 endpoints across 1 groups. See references/api-spec.lap for full details.

### render
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/render/sync | Render a URL as an image or video |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a sync?" -> POST /v1/render/sync
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
