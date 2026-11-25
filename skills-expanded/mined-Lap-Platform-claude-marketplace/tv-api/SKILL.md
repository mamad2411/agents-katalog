---
name: tv-api
description: "TV API skill. Use when working with TV for platform, channel, asset. Covers 18 endpoints."
version: 1.0.0
generator: lapsh
---

# TV API
API version: 2.0

## Auth
ApiKey apikey in header

## Base URL
https://tv.api.pressassociation.io/v2

## Setup
1. Set your API key in the appropriate header
2. GET /platform -- verify access

## Endpoints

18 endpoints across 8 groups. See references/api-spec.lap for full details.

### platform
| Method | Path | Description |
|--------|------|-------------|
| GET | /platform | Platform Collection |
| GET | /platform/{platformId} | Platform Detail |
| GET | /platform/{platformId}/region | Platform Region Collection |

### channel
| Method | Path | Description |
|--------|------|-------------|
| GET | /channel | Channel Collection |
| GET | /channel/{channelId} | Channel Detail |

### asset
| Method | Path | Description |
|--------|------|-------------|
| GET | /asset | Asset Collection |
| GET | /asset/{assetId} | Asset Detail |
| GET | /asset/{assetId}/contributor | Asset Contributors |

### contributor
| Method | Path | Description |
|--------|------|-------------|
| GET | /contributor | Contributor Collection |
| GET | /contributor/{contributorId} | Contributor Detail |

### schedule
| Method | Path | Description |
|--------|------|-------------|
| GET | /schedule | Schedule Collection |

### feature-type
| Method | Path | Description |
|--------|------|-------------|
| GET | /feature-type | Feature Type Collection |

### feature
| Method | Path | Description |
|--------|------|-------------|
| GET | /feature | Feature Collection |
| GET | /feature/{featureId} | Feature Detail |

### catalogue
| Method | Path | Description |
|--------|------|-------------|
| GET | /catalogue | Catalogue Collection |
| GET | /catalogue/{catalogueId} | Catalogue Detail |
| GET | /catalogue/{catalogueId}/asset | Catalogue Asset Collection |
| GET | /catalogue/{catalogueId}/asset/{assetId} | Catalogue Asset Detail |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all platform?" -> GET /platform
- "Get platform details?" -> GET /platform/{platformId}
- "List all region?" -> GET /platform/{platformId}/region
- "List all channel?" -> GET /channel
- "Get channel details?" -> GET /channel/{channelId}
- "List all asset?" -> GET /asset
- "Get asset details?" -> GET /asset/{assetId}
- "List all contributor?" -> GET /asset/{assetId}/contributor
- "List all contributor?" -> GET /contributor
- "Get contributor details?" -> GET /contributor/{contributorId}
- "List all schedule?" -> GET /schedule
- "List all feature-type?" -> GET /feature-type
- "List all feature?" -> GET /feature
- "Get feature details?" -> GET /feature/{featureId}
- "List all catalogue?" -> GET /catalogue
- "Get catalogue details?" -> GET /catalogue/{catalogueId}
- "List all asset?" -> GET /catalogue/{catalogueId}/asset
- "Get asset details?" -> GET /catalogue/{catalogueId}/asset/{assetId}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
