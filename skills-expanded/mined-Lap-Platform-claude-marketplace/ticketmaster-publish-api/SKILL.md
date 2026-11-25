---
name: ticketmaster-publish-api
description: "ticketmaster publish API skill. Use when working with ticketmaster publish for publish. Covers 10 endpoints."
version: 1.0.0
generator: lapsh
---

# ticketmaster publish api
API version: v2

## Auth
No authentication required.

## Base URL
https://www.ticketmaster.com/publish/v2

## Setup
1. No auth setup needed
3. POST /publish/v2/attractions -- create first attractions

## Endpoints

10 endpoints across 1 groups. See references/api-spec.lap for full details.

### publish
| Method | Path | Description |
|--------|------|-------------|
| POST | /publish/v2/attractions | Publish an attractions |
| PATCH | /publish/v2/attractions/{id} | Publish a patch on an attraction |
| POST | /publish/v2/attractions/{id}/videos | Publish a video on an attraction |
| POST | /publish/v2/entitlements | Publish entitlements on an entity |
| POST | /publish/v2/events | Publish an event |
| PATCH | /publish/v2/events/{id} | Publish a patch on an event |
| POST | /publish/v2/events/{id}/videos | Publish a video on an event |
| POST | /publish/v2/extensions | Publish extension on an entity |
| POST | /publish/v2/venues | Publish a venue |
| PATCH | /publish/v2/venues/{id} | Publish a patch on a venue |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a attraction?" -> POST /publish/v2/attractions
- "Partially update a attraction?" -> PATCH /publish/v2/attractions/{id}
- "Create a video?" -> POST /publish/v2/attractions/{id}/videos
- "Create a entitlement?" -> POST /publish/v2/entitlements
- "Create a event?" -> POST /publish/v2/events
- "Partially update a event?" -> PATCH /publish/v2/events/{id}
- "Create a video?" -> POST /publish/v2/events/{id}/videos
- "Create a extension?" -> POST /publish/v2/extensions
- "Create a venue?" -> POST /publish/v2/venues
- "Partially update a venue?" -> PATCH /publish/v2/venues/{id}

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
