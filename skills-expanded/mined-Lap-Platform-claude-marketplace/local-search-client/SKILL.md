---
name: local-search-client
description: "Local Search Client API skill. Use when working with Local Search Client for v7.0. Covers 1 endpoint."
version: 1.0.0
generator: lapsh
---

# Local Search Client
API version: 1.0

## Auth
ApiKey Ocp-Apim-Subscription-Key in header

## Base URL
https://api.cognitive.microsoft.com/bing

## Setup
1. Set your API key in the appropriate header
2. GET /v7.0/localbusinesses/search -- verify access

## Endpoints

1 endpoints across 1 groups. See references/api-spec.lap for full details.

### v7.0
| Method | Path | Description |
|--------|------|-------------|
| GET | /v7.0/localbusinesses/search | The Local Search API lets you send a search query to Bing and get back search results that include local businesses such as restaurants, hotels, retail stores, or other local businesses. The query can specify the name of the local business or it can ask for a list (for example, restaurants near me). |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Search search?" -> GET /v7.0/localbusinesses/search
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
