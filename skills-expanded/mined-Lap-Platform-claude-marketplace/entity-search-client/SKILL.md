---
name: entity-search-client
description: "Entity Search Client API skill. Use when working with Entity Search Client for entities. Covers 1 endpoint."
version: 1.0.0
generator: lapsh
---

# Entity Search Client
API version: 1.0

## Auth
ApiKey Ocp-Apim-Subscription-Key in header

## Base URL
https://api.cognitive.microsoft.com/bing/v7.0

## Setup
1. Set your API key in the appropriate header
2. GET /entities -- verify access

## Endpoints

1 endpoints across 1 groups. See references/api-spec.lap for full details.

### entities
| Method | Path | Description |
|--------|------|-------------|
| GET | /entities | The Entity Search API lets you send a search query to Bing and get back search results that include entities and places. Place results include restaurants, hotel, or other local businesses. For places, the query can specify the name of the local business or it can ask for a list (for example, restaurants near me). Entity results include persons, places, or things. Place in this context is tourist attractions, states, countries, etc. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Search entities?" -> GET /entities
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
