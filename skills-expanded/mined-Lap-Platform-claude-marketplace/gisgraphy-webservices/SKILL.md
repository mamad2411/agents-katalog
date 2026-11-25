---
name: gisgraphy-webservices
description: "Gisgraphy webservices API skill. Use when working with Gisgraphy webservices for geocoding, reversegeocoding, street. Covers 6 endpoints."
version: 1.0.0
generator: lapsh
---

# Gisgraphy webservices
API version: 4.0.0

## Auth
ApiKey api_key in query

## Base URL
http://free.gisgraphy.com/

## Setup
1. Set your API key in the appropriate header
2. GET /geocoding/geocode -- verify access

## Endpoints

6 endpoints across 6 groups. See references/api-spec.lap for full details.

### geocoding
| Method | Path | Description |
|--------|------|-------------|
| GET | /geocoding/geocode | Geocode an address |

### reversegeocoding
| Method | Path | Description |
|--------|------|-------------|
| GET | /reversegeocoding/reversegeocode | Reverse geocode an address |

### street
| Method | Path | Description |
|--------|------|-------------|
| GET | /street/find | Geocode an address |

### geoloc
| Method | Path | Description |
|--------|------|-------------|
| GET | /geoloc/search | Geocode an address |

### fulltext
| Method | Path | Description |
|--------|------|-------------|
| GET | /fulltext/search | search for places by text around a GPS point |

### addressparser
| Method | Path | Description |
|--------|------|-------------|
| GET | /addressparser/parse | split a raw address into several parts |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all geocode?" -> GET /geocoding/geocode
- "List all reversegeocode?" -> GET /reversegeocoding/reversegeocode
- "List all find?" -> GET /street/find
- "List all search?" -> GET /geoloc/search
- "Search search?" -> GET /fulltext/search
- "List all parse?" -> GET /addressparser/parse
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
