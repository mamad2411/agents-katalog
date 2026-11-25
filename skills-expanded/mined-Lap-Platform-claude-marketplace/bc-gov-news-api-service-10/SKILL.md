---
name: bc-gov-news-api-service-10
description: "BC Gov News API Service 1.0 API skill. Use when working with BC Gov News API Service 1.0 for api. Covers 27 endpoints."
version: 1.0.0
generator: lapsh
---

# BC Gov News API Service 1.0
API version: 1.0

## Auth
Requires API key (key parameter)

## Base URL
https://news.api.gov.bc.ca/

## Setup
1. Include your API key via the key parameter
2. GET /api/FacebookPosts/ByUri -- verify access

## Endpoints

27 endpoints across 1 groups. See references/api-spec.lap for full details.

### api
| Method | Path | Description |
|--------|------|-------------|
| GET | /api/FacebookPosts/ByUri | Get a Facebook post based on a Uri |
| GET | /api/Home | Returns the top level content for the home page |
| GET | /api/Ministries | Get all ministries |
| GET | /api/Ministries/{key} | Get the Ministry associated with the ministry key |
| GET | /api/Ministries/{key}/Minister | Get the Minister associated with the ministry key |
| GET | /api/Newsletters | Get all newsletters |
| GET | /api/Newsletters/{newsletterKey} | Get a specific newsletter |
| GET | /api/Newsletters/{newsletterKey}/Editions/{editionKey} | Returns a specific edition of a newsletter |
| GET | /api/Newsletters/{newsletterKey}/Editions/{editionKey}/Articles/{articleKey} | Get an article belonging to a Newsletter edition |
| GET | /api/Newsletters/Images/{guid} | Get the image object reference by of a Newsletter Edition associated with the image guid |
| GET | /api/Posts/{key} | Get the post associated with the key |
| GET | /api/Posts | Get the posts associated with the keys in the list passed in. |
| GET | /api/Posts/Latest/{indexKind}/{indexKey} | Get the latest posts of postKind for the specified index (default or category) |
| GET | /api/Posts/Keys/{indexKind}/{indexKey} | Get all keys for the specified index (newsroom or category) |
| GET | /api/Posts/Keys/{reference} | Get the post key associated with the reference. |
| GET | /api/Posts/LatestMediaUri/{mediaType} | Gets the latest Social Media post for the social media type passed in. |
| GET | /api/ResourceLinks | Get all resource links |
| GET | /api/Sectors | Get all Sectors |
| GET | /api/Sectors/{key} | Get the sector associated with the key |
| GET | /api/Services | Get all Services |
| GET | /api/Services/{key} | Get the service associated with the passed key |
| GET | /api/Slides/{id} | Get the slide associated to the id |
| GET | /api/Slides | Get all Slides |
| GET | /api/Tags | Get all Tags |
| GET | /api/Tags/{key} | Get the Tag associated with the key |
| GET | /api/Themes | Get all Themes |
| GET | /api/Themes/{key} | Get the Theme associated with the key |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all ByUri?" -> GET /api/FacebookPosts/ByUri
- "List all Home?" -> GET /api/Home
- "List all Ministries?" -> GET /api/Ministries
- "Get Ministry details?" -> GET /api/Ministries/{key}
- "List all Minister?" -> GET /api/Ministries/{key}/Minister
- "List all Newsletters?" -> GET /api/Newsletters
- "Get Newsletter details?" -> GET /api/Newsletters/{newsletterKey}
- "Get Edition details?" -> GET /api/Newsletters/{newsletterKey}/Editions/{editionKey}
- "Get Article details?" -> GET /api/Newsletters/{newsletterKey}/Editions/{editionKey}/Articles/{articleKey}
- "Get Image details?" -> GET /api/Newsletters/Images/{guid}
- "Get Post details?" -> GET /api/Posts/{key}
- "List all Posts?" -> GET /api/Posts
- "Get Latest details?" -> GET /api/Posts/Latest/{indexKind}/{indexKey}
- "Get Key details?" -> GET /api/Posts/Keys/{indexKind}/{indexKey}
- "Get Key details?" -> GET /api/Posts/Keys/{reference}
- "Get LatestMediaUri details?" -> GET /api/Posts/LatestMediaUri/{mediaType}
- "List all ResourceLinks?" -> GET /api/ResourceLinks
- "List all Sectors?" -> GET /api/Sectors
- "Get Sector details?" -> GET /api/Sectors/{key}
- "List all Services?" -> GET /api/Services
- "Get Service details?" -> GET /api/Services/{key}
- "Get Slide details?" -> GET /api/Slides/{id}
- "List all Slides?" -> GET /api/Slides
- "List all Tags?" -> GET /api/Tags
- "Get Tag details?" -> GET /api/Tags/{key}
- "List all Themes?" -> GET /api/Themes
- "Get Theme details?" -> GET /api/Themes/{key}

## Response Tips
- Check response schemas in references/api-spec.lap for field details

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
