---
name: bc-geographical-names-web-service-rest-api
description: "BC Geographical Names Web Service - REST API skill. Use when working with BC Geographical Names Web Service - REST for names, features, featureClasses. Covers 14 endpoints."
version: 1.0.0
generator: lapsh
---

# BC Geographical Names Web Service - REST API
API version: 3.x.x

## Auth
No authentication required.

## Base URL
https://apps.gov.bc.ca/pub/bcgnws

## Setup
1. No auth setup needed
2. GET /names/search -- verify access

## Endpoints

14 endpoints across 6 groups. See references/api-spec.lap for full details.

### names
| Method | Path | Description |
|--------|------|-------------|
| GET | /names/search | Search by name |
| GET | /names/official/search | Search by name, limit to official names only |
| GET | /names/notOfficial/search | Search by name, limit to unofficial names only |
| GET | /names/inside | Search in a geographic area |
| GET | /names/near | Search near to a geographic point |
| GET | /names/decisions/recent | Search for names affected by recent naming decision |
| GET | /names/decisions/year | Search for names affected by naming decisions in a given year |
| GET | /names/changes | Search for names with metadata changes in a given period |
| GET | /names/{nameId}.{outputFormat} | Get a name by its nameId |

### features
| Method | Path | Description |
|--------|------|-------------|
| GET | /features/{featureId} | Get a feature by its featureId |

### featureClasses
| Method | Path | Description |
|--------|------|-------------|
| GET | /featureClasses | Get all feature classes |

### featureCategories
| Method | Path | Description |
|--------|------|-------------|
| GET | /featureCategories | Get all feature categories |

### featureTypes
| Method | Path | Description |
|--------|------|-------------|
| GET | /featureTypes | Get all feature types |

### nameAuthorities
| Method | Path | Description |
|--------|------|-------------|
| GET | /nameAuthorities | Get all name authorities |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all search?" -> GET /names/search
- "List all search?" -> GET /names/official/search
- "List all search?" -> GET /names/notOfficial/search
- "List all inside?" -> GET /names/inside
- "List all near?" -> GET /names/near
- "List all recent?" -> GET /names/decisions/recent
- "List all year?" -> GET /names/decisions/year
- "List all changes?" -> GET /names/changes
- "Get name details?" -> GET /names/{nameId}.{outputFormat}
- "Get feature details?" -> GET /features/{featureId}
- "List all featureClasses?" -> GET /featureClasses
- "List all featureCategories?" -> GET /featureCategories
- "List all featureTypes?" -> GET /featureTypes
- "List all nameAuthorities?" -> GET /nameAuthorities

## Response Tips
- Check response schemas in references/api-spec.lap for field details

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
