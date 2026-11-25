---
name: autosuggest-client
description: "AutoSuggest Client API skill. Use when working with AutoSuggest Client for Suggestions. Covers 1 endpoint."
version: 1.0.0
generator: lapsh
---

# AutoSuggest Client
API version: 1.0

## Auth
ApiKey Ocp-Apim-Subscription-Key in header

## Base URL
https://api.cognitive.microsoft.com/bing/v7.0

## Setup
1. Set your API key in the appropriate header
2. GET /Suggestions -- verify access

## Endpoints

1 endpoints across 1 groups. See references/api-spec.lap for full details.

### Suggestions
| Method | Path | Description |
|--------|------|-------------|
| GET | /Suggestions | The AutoSuggest API lets you send a search query to Bing and get back a list of query suggestions. This section provides technical details about the query parameters and headers that you use to request suggestions and the JSON response objects that contain them. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Search Suggestions?" -> GET /Suggestions
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
