---
name: setlistfm-api
description: "setlist.fm API skill. Use when working with setlist.fm for 1.0. Covers 15 endpoints."
version: 1.0.0
generator: lapsh
---

# setlist.fm API
API version: 1.0

## Auth
ApiKey (inferred from docs)

## Base URL
Not specified.

## Setup
1. Set your API key in the appropriate header
2. GET /1.0/search/artists -- verify access

## Endpoints

15 endpoints across 1 groups. See references/api-spec.lap for full details.

### 1.0
| Method | Path | Description |
|--------|------|-------------|
| GET | /1.0/artist/{mbid} | . |
| GET | /1.0/artist/{mbid}/setlists | . |
| GET | /1.0/city/{geoId} | Get a city by its unique geoId. |
| GET | /1.0/search/artists | Search for artists. |
| GET | /1.0/search/cities | Search for a city. |
| GET | /1.0/search/countries | Get a complete list of all supported countries. |
| GET | /1.0/search/setlists | Search for setlists. |
| GET | /1.0/search/venues | Search for venues. |
| GET | /1.0/setlist/version/{versionId} | . |
| GET | /1.0/setlist/{setlistId} | . |
| GET | /1.0/user/{userId} | Get a user by userId. |
| GET | /1.0/user/{userId}/attended | . |
| GET | /1.0/user/{userId}/edited | . |
| GET | /1.0/venue/{venueId} | Get a venue by its unique id. |
| GET | /1.0/venue/{venueId}/setlists | . |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Get artist details?" -> GET /1.0/artist/{mbid}
- "List all setlists?" -> GET /1.0/artist/{mbid}/setlists
- "Get city details?" -> GET /1.0/city/{geoId}
- "List all artists?" -> GET /1.0/search/artists
- "List all cities?" -> GET /1.0/search/cities
- "List all countries?" -> GET /1.0/search/countries
- "List all setlists?" -> GET /1.0/search/setlists
- "List all venues?" -> GET /1.0/search/venues
- "Get version details?" -> GET /1.0/setlist/version/{versionId}
- "Get setlist details?" -> GET /1.0/setlist/{setlistId}
- "Get user details?" -> GET /1.0/user/{userId}
- "List all attended?" -> GET /1.0/user/{userId}/attended
- "List all edited?" -> GET /1.0/user/{userId}/edited
- "Get venue details?" -> GET /1.0/venue/{venueId}
- "List all setlists?" -> GET /1.0/venue/{venueId}/setlists
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
