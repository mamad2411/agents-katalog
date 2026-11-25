---
name: visual-search-client
description: "Visual Search Client API skill. Use when working with Visual Search Client for images. Covers 1 endpoint."
version: 1.0.0
generator: lapsh
---

# Visual Search Client
API version: 1.0

## Auth
ApiKey Ocp-Apim-Subscription-Key in header

## Base URL
https://api.cognitive.microsoft.com/bing/v7.0

## Setup
1. Set your API key in the appropriate header
3. POST /images/visualsearch -- create first visualsearch

## Endpoints

1 endpoints across 1 groups. See references/api-spec.lap for full details.

### images
| Method | Path | Description |
|--------|------|-------------|
| POST | /images/visualsearch | Visual Search API lets you discover insights about an image such as visually similar images, shopping sources, and related searches. The API can also perform text recognition, identify entities (people, places, things), return other topical content for the user to explore, and more. For more information, see [Visual Search Overview](https://docs.microsoft.com/azure/cognitive-services/bing-visual-search/overview). |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a visualsearch?" -> POST /images/visualsearch
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
