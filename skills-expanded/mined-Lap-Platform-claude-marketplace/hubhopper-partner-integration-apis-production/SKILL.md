---
name: hubhopper-partner-integration-apis-production
description: "Hubhopper Partner Integration API(s) - Production API skill. Use when working with Hubhopper Partner Integration API(s) - Production for categories, podcasts, util. Covers 7 endpoints."
version: 1.0.0
generator: lapsh
---

# Hubhopper Partner Integration API(s) - Production
API version: v5

## Auth
ApiKey x-api-key in header | ApiKey hhPartnerId in header

## Base URL
https://apis.hubhopper.com/partner

## Setup
1. Set your API key in the appropriate header
2. GET /categories -- verify access

## Endpoints

7 endpoints across 3 groups. See references/api-spec.lap for full details.

### categories
| Method | Path | Description |
|--------|------|-------------|
| GET | /categories | Get the list of all content categories. |
| GET | /categories/{categoryId} | Get specific content category. |
| GET | /categories/{categoryId}/podcasts | Get a list of all podcasts under a category. |

### podcasts
| Method | Path | Description |
|--------|------|-------------|
| GET | /podcasts | Get the list of all podcasts. |
| GET | /podcasts/{podcastId} | Get a single Podcast. |
| GET | /podcasts/{podcastId}/episodes | Get a list of all episodes under a podcast. |

### util
| Method | Path | Description |
|--------|------|-------------|
| GET | /util/languages |  |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all categories?" -> GET /categories
- "Get category details?" -> GET /categories/{categoryId}
- "List all podcasts?" -> GET /categories/{categoryId}/podcasts
- "List all podcasts?" -> GET /podcasts
- "Get podcast details?" -> GET /podcasts/{podcastId}
- "List all episodes?" -> GET /podcasts/{podcastId}/episodes
- "List all languages?" -> GET /util/languages
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
