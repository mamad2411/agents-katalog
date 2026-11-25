---
name: domains-index-api
description: "Domains-Index API skill. Use when working with Domains-Index for domains, info. Covers 14 endpoints."
version: 1.0.0
generator: lapsh
---

# Domains-Index API
API version: 1.0

## Auth
ApiKey api_key in query

## Base URL
Not specified.

## Setup
1. Set your API key in the appropriate header
2. GET /domains/search -- verify access

## Endpoints

14 endpoints across 2 groups. See references/api-spec.lap for full details.

### domains
| Method | Path | Description |
|--------|------|-------------|
| GET | /domains/search | Domains Database Search |
| GET | /domains/tld/{zone_id} | Get TLD records |
| GET | /domains/tld/{zone_id}/download | Download Whole Dataset for TLD |
| GET | /domains/tld/{zone_id}/search | Domains Search for TLD |
| GET | /domains/updates/added | Get added domains, latest if date not specified |
| GET | /domains/updates/added/download | Download added domains, latest if date not specified |
| GET | /domains/updates/deleted | Get deleted domains, latest if date not specified |
| GET | /domains/updates/deleted/download | Download deleted domains, latest if date not specified |
| GET | /domains/updates/list | List of updates |

### info
| Method | Path | Description |
|--------|------|-------------|
| GET | /info/api |  |
| GET | /info/stat/ | Returns overall stagtistics |
| GET | /info/stat/{zone} | Returns statistics for specific zone |
| GET | /info/tld/ | Returns overall Tld info |
| GET | /info/tld/{zone} | Returns statistics for specific zone |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all search?" -> GET /domains/search
- "Get tld details?" -> GET /domains/tld/{zone_id}
- "List all download?" -> GET /domains/tld/{zone_id}/download
- "List all search?" -> GET /domains/tld/{zone_id}/search
- "List all added?" -> GET /domains/updates/added
- "List all download?" -> GET /domains/updates/added/download
- "List all deleted?" -> GET /domains/updates/deleted
- "List all download?" -> GET /domains/updates/deleted/download
- "List all list?" -> GET /domains/updates/list
- "List all api?" -> GET /info/api
- "List all stat?" -> GET /info/stat/
- "Get stat details?" -> GET /info/stat/{zone}
- "List all tld?" -> GET /info/tld/
- "Get tld details?" -> GET /info/tld/{zone}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
