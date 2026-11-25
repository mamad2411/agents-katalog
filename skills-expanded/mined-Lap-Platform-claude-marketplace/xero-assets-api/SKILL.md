---
name: xero-assets-api
description: "Xero Assets API skill. Use when working with Xero Assets for Assets, AssetTypes, Settings. Covers 6 endpoints."
version: 1.0.0
generator: lapsh
---

# Xero Assets API
API version: 11.1.0

## Auth
OAuth2

## Base URL
https://api.xero.com/assets.xro/1.0

## Setup
1. Configure auth: OAuth2
2. GET /Assets -- verify access
3. POST /Assets -- create first Assets

## Endpoints

6 endpoints across 3 groups. See references/api-spec.lap for full details.

### Assets
| Method | Path | Description |
|--------|------|-------------|
| GET | /Assets | searches fixed asset |
| POST | /Assets | adds a fixed asset |
| GET | /Assets/{id} | Retrieves fixed asset by id |

### AssetTypes
| Method | Path | Description |
|--------|------|-------------|
| GET | /AssetTypes | searches fixed asset types |
| POST | /AssetTypes | adds a fixed asset type |

### Settings
| Method | Path | Description |
|--------|------|-------------|
| GET | /Settings | searches fixed asset settings |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all Assets?" -> GET /Assets
- "Create a Asset?" -> POST /Assets
- "Get Asset details?" -> GET /Assets/{id}
- "List all AssetTypes?" -> GET /AssetTypes
- "Create a AssetType?" -> POST /AssetTypes
- "List all Settings?" -> GET /Settings
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
