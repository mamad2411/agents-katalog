---
name: hhs-media-services-api
description: "HHS Media Services API skill. Use when working with HHS Media Services for resources.json, resources. Covers 31 endpoints."
version: 1.0.0
generator: lapsh
---

# HHS Media Services API
API version: 2

## Auth
No authentication required.

## Base URL
Not specified.

## Setup
1. No auth setup needed
2. GET /resources.json -- verify access

## Endpoints

31 endpoints across 2 groups. See references/api-spec.lap for full details.

### resources.json
| Method | Path | Description |
|--------|------|-------------|
| GET | /resources.json | Get Resources by search query |

### resources
| Method | Path | Description |
|--------|------|-------------|
| GET | /resources/campaigns.json | Get Campaigns |
| GET | /resources/campaigns/{id}.json | Get Campaign by ID |
| GET | /resources/campaigns/{id}/media.json | Get MediaItems by Campaign ID |
| GET | /resources/campaigns/{id}/syndicate.{format} | Get MediaItems for Campaign |
| GET | /resources/languages.json | Get Languages |
| GET | /resources/languages/{id}.json | Get Language by ID |
| GET | /resources/media.json | Get MediaItems |
| GET | /resources/media/featured.json | Get the list of featured content in the syndication system |
| GET | /resources/media/mostPopularMedia.{format} | Get MediaItems by popularity |
| GET | /resources/media/searchResults.json | Get MediaItems by search query |
| GET | /resources/media/{id}.json | Get MediaItem by ID |
| GET | /resources/media/{id}/content | Get content for MediaItem |
| GET | /resources/media/{id}/embed.json | Get embed code for MediaItem |
| GET | /resources/media/{id}/preview.jpg | Get Tag by ID |
| GET | /resources/media/{id}/relatedMedia.{format} | Get related MediaItems by ID |
| GET | /resources/media/{id}/syndicate.{format} | Get syndicated content for MediaItem |
| GET | /resources/media/{id}/thumbnail.jpg | Get JPG thumbnail for MediaItem |
| GET | /resources/media/{id}/youtubeMetaData.json | Get Youtube metadata for MediaItem |
| GET | /resources/mediaTypes.{format} | Get MediaTypes |
| GET | /resources/sources.json | Get Sources |
| GET | /resources/sources/{id}.json | Get Source by ID |
| GET | /resources/sources/{id}/syndicate.{format} | Get MediaItems for Source |
| GET | /resources/tags.{format} | Get Tags |
| GET | /resources/tags/tagLanguages.{format} | Get TagLanguages |
| GET | /resources/tags/tagTypes.{format} | Get MediaItems for Tag |
| GET | /resources/tags/{id}.{format} | Get Tag by ID |
| GET | /resources/tags/{id}/media.{format} | Get MediaItems for Tag |
| GET | /resources/tags/{id}/related.{format} | Get related Tags by ID |
| GET | /resources/tags/{id}/syndicate.{format} | Get MediaItems for Tag |
| GET | /resources/userMediaLists/{id}.json | Get UserMediaList by ID |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Search resources.json?" -> GET /resources.json
- "List all campaigns.json?" -> GET /resources/campaigns.json
- "Get campaign details?" -> GET /resources/campaigns/{id}.json
- "List all media.json?" -> GET /resources/campaigns/{id}/media.json
- "Get syndicate.{format} details?" -> GET /resources/campaigns/{id}/syndicate.{format}
- "List all languages.json?" -> GET /resources/languages.json
- "Get language details?" -> GET /resources/languages/{id}.json
- "List all media.json?" -> GET /resources/media.json
- "List all featured.json?" -> GET /resources/media/featured.json
- "Get mostPopularMedia.{format} details?" -> GET /resources/media/mostPopularMedia.{format}
- "Search searchResults.json?" -> GET /resources/media/searchResults.json
- "Get media details?" -> GET /resources/media/{id}.json
- "List all content?" -> GET /resources/media/{id}/content
- "List all embed.json?" -> GET /resources/media/{id}/embed.json
- "List all preview.jpg?" -> GET /resources/media/{id}/preview.jpg
- "Get relatedMedia.{format} details?" -> GET /resources/media/{id}/relatedMedia.{format}
- "Get syndicate.{format} details?" -> GET /resources/media/{id}/syndicate.{format}
- "List all thumbnail.jpg?" -> GET /resources/media/{id}/thumbnail.jpg
- "List all youtubeMetaData.json?" -> GET /resources/media/{id}/youtubeMetaData.json
- "Get mediaTypes.{format} details?" -> GET /resources/mediaTypes.{format}
- "List all sources.json?" -> GET /resources/sources.json
- "Get source details?" -> GET /resources/sources/{id}.json
- "Get syndicate.{format} details?" -> GET /resources/sources/{id}/syndicate.{format}
- "Get tags.{format} details?" -> GET /resources/tags.{format}
- "Get tagLanguages.{format} details?" -> GET /resources/tags/tagLanguages.{format}
- "Get tagTypes.{format} details?" -> GET /resources/tags/tagTypes.{format}
- "Get tag details?" -> GET /resources/tags/{id}.{format}
- "Get media.{format} details?" -> GET /resources/tags/{id}/media.{format}
- "Get related.{format} details?" -> GET /resources/tags/{id}/related.{format}
- "Get syndicate.{format} details?" -> GET /resources/tags/{id}/syndicate.{format}
- "Get userMediaList details?" -> GET /resources/userMediaLists/{id}.json

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
