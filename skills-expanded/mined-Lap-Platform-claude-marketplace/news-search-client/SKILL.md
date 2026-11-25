---
name: news-search-client
description: "News Search Client API skill. Use when working with News Search Client for news. Covers 3 endpoints."
version: 1.0.0
generator: lapsh
---

# News Search Client
API version: 1.0

## Auth
ApiKey Ocp-Apim-Subscription-Key in header

## Base URL
https://api.cognitive.microsoft.com/bing/v7.0

## Setup
1. Set your API key in the appropriate header
2. GET /news/search -- verify access

## Endpoints

3 endpoints across 1 groups. See references/api-spec.lap for full details.

### news
| Method | Path | Description |
|--------|------|-------------|
| GET | /news/search | The News Search API lets you send a search query to Bing and get back a list of news that are relevant to the search query. This section provides technical details about the query parameters and headers that you use to request news and the JSON response objects that contain them.  For examples that show how to make requests, see [Searching the web for news](https://docs.microsoft.com/en-us/azure/cognitive-services/bing-news-search/search-the-web). |
| GET | /news | The News Category API lets you search on Bing and get back a list of top news articles by category. This section provides technical details about the query parameters and headers that you use to request news and the JSON response objects that contain them.  For examples that show how to make requests, see [Searching the web for news](https://docs.microsoft.com/en-us/azure/cognitive-services/bing-news-search/search-the-web). |
| GET | /news/trendingtopics | The News Trending Topics API lets you search on Bing and get back a list of trending news topics that are currently trending on Bing. This section provides technical details about the query parameters and headers that you use to request news and the JSON response objects that contain them.  For examples that show how to make requests, see [Searching the web for news](https://docs.microsoft.com/en-us/azure/cognitive-services/bing-news-search/search-the-web). |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Search search?" -> GET /news/search
- "List all news?" -> GET /news
- "List all trendingtopics?" -> GET /news/trendingtopics
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
