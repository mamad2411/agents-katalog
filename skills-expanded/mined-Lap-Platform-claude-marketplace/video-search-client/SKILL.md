---
name: video-search-client
description: "Video Search Client API skill. Use when working with Video Search Client for videos. Covers 3 endpoints."
version: 1.0.0
generator: lapsh
---

# Video Search Client
API version: 1.0

## Auth
ApiKey Ocp-Apim-Subscription-Key in header

## Base URL
https://api.cognitive.microsoft.com/bing/v7.0

## Setup
1. Set your API key in the appropriate header
2. GET /videos/search -- verify access

## Endpoints

3 endpoints across 1 groups. See references/api-spec.lap for full details.

### videos
| Method | Path | Description |
|--------|------|-------------|
| GET | /videos/search | The Video Search API lets you send a search query to Bing and get back a list of videos that are relevant to the search query. This section provides technical details about the query parameters and headers that you use to request videos and the JSON response objects that contain them. For examples that show how to make requests, see [Searching the Web for Videos](https://docs.microsoft.com/azure/cognitive-services/bing-video-search/search-the-web). |
| GET | /videos/details | The Video Detail Search API lets you search on Bing and get back insights about a video, such as related videos. This section provides technical details about the query parameters and headers that you use to request insights of videos and the JSON response objects that contain them. For examples that show how to make requests, see [Searching the Web for Videos](https://docs.microsoft.com/azure/cognitive-services/bing-video-search/search-the-web). |
| GET | /videos/trending | The Video Trending Search API lets you search on Bing and get back a list of videos that are trending based on search requests made by others. The videos are broken out into different categories. For example, Top Music Videos. For a list of markets that support trending videos, see [Trending Videos](https://docs.microsoft.com/azure/cognitive-services/bing-video-search/trending-videos). |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Search search?" -> GET /videos/search
- "Search details?" -> GET /videos/details
- "List all trending?" -> GET /videos/trending
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
