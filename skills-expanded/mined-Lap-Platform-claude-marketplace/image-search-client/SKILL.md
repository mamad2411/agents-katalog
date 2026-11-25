---
name: image-search-client
description: "Image Search Client API skill. Use when working with Image Search Client for images. Covers 3 endpoints."
version: 1.0.0
generator: lapsh
---

# Image Search Client
API version: 1.0

## Auth
ApiKey Ocp-Apim-Subscription-Key in header

## Base URL
https://api.cognitive.microsoft.com/bing/v7.0

## Setup
1. Set your API key in the appropriate header
2. GET /images/search -- verify access

## Endpoints

3 endpoints across 1 groups. See references/api-spec.lap for full details.

### images
| Method | Path | Description |
|--------|------|-------------|
| GET | /images/search | The Image Search API lets you send a search query to Bing and get back a list of relevant images. This section provides technical details about the query parameters and headers that you use to request images and the JSON response objects that contain them. For examples that show how to make requests, see [Searching the Web for Images](https://docs.microsoft.com/azure/cognitive-services/bing-image-search/search-the-web). |
| GET | /images/details | The Image Detail Search API lets you search on Bing and get back insights about an image, such as webpages that include the image. This section provides technical details about the query parameters and headers that you use to request insights of images and the JSON response objects that contain them. For examples that show how to make requests, see [Searching the Web for Images](https://docs.microsoft.com/azure/cognitive-services/bing-image-search/search-the-web). |
| GET | /images/trending | The Image Trending Search API lets you search on Bing and get back a list of images that are trending based on search requests made by others. The images are broken out into different categories. For example, Popular People Searches. For a list of markets that support trending images, see [Trending Images](https://docs.microsoft.com/en-us/azure/cognitive-services/bing-image-search/trending-images). |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Search search?" -> GET /images/search
- "Search details?" -> GET /images/details
- "List all trending?" -> GET /images/trending
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
