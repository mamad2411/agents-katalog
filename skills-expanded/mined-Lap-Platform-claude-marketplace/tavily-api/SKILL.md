---
name: tavily-api
description: "Tavily API skill. Use when working with Tavily for search. Covers 1 endpoint."
version: 1.0.0
generator: lapsh
---

# Tavily API
API version: 1.0.0

## Auth
Requires API key (api_key parameter)

## Base URL
https://api.tavily.com

## Setup
1. Include your API key via the api_key parameter
3. POST /search -- create first search

## Endpoints

1 endpoints across 1 groups. See references/api-spec.lap for full details.

### search
| Method | Path | Description |
|--------|------|-------------|
| POST | /search | Search for data based on a query. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a search?" -> POST /search

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
