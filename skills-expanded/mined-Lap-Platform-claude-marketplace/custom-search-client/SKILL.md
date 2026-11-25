---
name: custom-search-client
description: "Custom Search Client API skill. Use when working with Custom Search Client for search. Covers 1 endpoint."
version: 1.0.0
generator: lapsh
---

# Custom Search Client
API version: 1.0

## Auth
ApiKey Ocp-Apim-Subscription-Key in header

## Base URL
https://api.cognitive.microsoft.com/bingcustomsearch/v7.0

## Setup
1. Set your API key in the appropriate header
2. GET /search -- verify access

## Endpoints

1 endpoints across 1 groups. See references/api-spec.lap for full details.

### search
| Method | Path | Description |
|--------|------|-------------|
| GET | /search | The Custom Search API lets you send a search query to Bing and get back web pages found in your custom view of the web. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Search search?" -> GET /search
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
