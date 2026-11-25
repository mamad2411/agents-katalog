---
name: geomark-web-service-rest-api
description: "Geomark Web Service REST API skill. Use when working with Geomark Web Service REST for geomarks. Covers 7 endpoints."
version: 1.0.0
generator: lapsh
---

# Geomark Web Service REST API
API version: 4.1.2

## Auth
No authentication required.

## Base URL
https://apps.gov.bc.ca/pub/geomark

## Setup
1. No auth setup needed
2. GET /geomarks/{geomarkId}/boundingBox.{fileFormatExtension} -- verify access
3. POST /geomarks/new -- create first new

## Endpoints

7 endpoints across 1 groups. See references/api-spec.lap for full details.

### geomarks
| Method | Path | Description |
|--------|------|-------------|
| POST | /geomarks/new | Create a new geomark |
| POST | /geomarks/copy | Create a new geomark by copying the geometries from one or more existing geomarks from the current server. |
| GET | /geomarks/{geomarkId}/boundingBox.{fileFormatExtension} | Gets the bounding box of the geomark |
| GET | /geomarks/{geomarkId}/feature.{fileFormatExtension} | Get the feature and attribution of the geomark |
| GET | /geomarks/{geomarkId}.{fileFormatExtension} | Get information about a particular geomark |
| GET | /geomarks/{geomarkId}/parts.{fileFormatExtension} | Get the individual geometries within a multi-part geometry |
| GET | /geomarks/{geomarkId}/point.{fileFormatExtension} | Gets a single spatial point representative of the geomark. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a new?" -> POST /geomarks/new
- "Create a copy?" -> POST /geomarks/copy
- "Get boundingBox.{fileFormatExtension} details?" -> GET /geomarks/{geomarkId}/boundingBox.{fileFormatExtension}
- "Get feature.{fileFormatExtension} details?" -> GET /geomarks/{geomarkId}/feature.{fileFormatExtension}
- "Get geomark details?" -> GET /geomarks/{geomarkId}.{fileFormatExtension}
- "Get parts.{fileFormatExtension} details?" -> GET /geomarks/{geomarkId}/parts.{fileFormatExtension}
- "Get point.{fileFormatExtension} details?" -> GET /geomarks/{geomarkId}/point.{fileFormatExtension}

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
