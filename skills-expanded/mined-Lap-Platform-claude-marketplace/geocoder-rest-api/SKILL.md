---
name: geocoder-rest-api
description: "Geocoder REST API skill. Use when working with Geocoder REST for addresses.{outputFormat}, occupants, sites. Covers 16 endpoints."
version: 1.0.0
generator: lapsh
---

# Geocoder REST API
API version: 2.0.0

## Auth
ApiKey apikey in header

## Base URL
https://geocoder.api.gov.bc.ca/

## Setup
1. Set your API key in the appropriate header
2. GET /addresses.{outputFormat} -- verify access

## Endpoints

16 endpoints across 5 groups. See references/api-spec.lap for full details.

### addresses.{outputFormat}
| Method | Path | Description |
|--------|------|-------------|
| GET | /addresses.{outputFormat} | Geocode an address |

### occupants
| Method | Path | Description |
|--------|------|-------------|
| GET | /occupants/addresses.{outputFormat} | Geocode an address and identify site occupants |
| GET | /occupants/nearest.{outputFormat} | Find occupants of the site nearest to a geographic point |
| GET | /occupants/near.{outputFormat} | Find occupants of sites near to a geographic point |
| GET | /occupants/within.{outputFormat} | Find occupants of sites in a geographic area |
| GET | /occupants/{occupantID}.{outputFormat} | Get an occupant (of a site) by its unique ID |

### sites
| Method | Path | Description |
|--------|------|-------------|
| GET | /sites/nearest.{outputFormat} | Find the site nearest to a geographic point |
| GET | /sites/near.{outputFormat} | Find sites near to a geographic point |
| GET | /sites/within.{outputFormat} | Find sites in a geographic area |
| GET | /sites/{siteID}/subsites.{outputFormat} | Represents all subsites of a given site |
| GET | /sites/{siteID}.{outputFormat} | Get a site by its unique ID |

### intersections
| Method | Path | Description |
|--------|------|-------------|
| GET | /intersections/nearest.{outputFormat} | Find nearest intersection to a geographic point |
| GET | /intersections/near.{outputFormat} | Find intersections near to a geographic point |
| GET | /intersections/within.{outputFormat} | Find intersections in a geographic area |
| GET | /intersections/{intersectionID}.{outputFormat} | Get an intersection by its unique ID |

### parcels
| Method | Path | Description |
|--------|------|-------------|
| GET | /parcels/pids/{siteID}.{outputFormat} | Get a comma-separated string of all pids for a given site |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Get addresses.{outputFormat} details?" -> GET /addresses.{outputFormat}
- "Get addresses.{outputFormat} details?" -> GET /occupants/addresses.{outputFormat}
- "Get nearest.{outputFormat} details?" -> GET /sites/nearest.{outputFormat}
- "Get nearest.{outputFormat} details?" -> GET /occupants/nearest.{outputFormat}
- "Get nearest.{outputFormat} details?" -> GET /intersections/nearest.{outputFormat}
- "Get near.{outputFormat} details?" -> GET /sites/near.{outputFormat}
- "Get near.{outputFormat} details?" -> GET /occupants/near.{outputFormat}
- "Get near.{outputFormat} details?" -> GET /intersections/near.{outputFormat}
- "Get within.{outputFormat} details?" -> GET /sites/within.{outputFormat}
- "Get within.{outputFormat} details?" -> GET /occupants/within.{outputFormat}
- "Get within.{outputFormat} details?" -> GET /intersections/within.{outputFormat}
- "Get subsites.{outputFormat} details?" -> GET /sites/{siteID}/subsites.{outputFormat}
- "Get site details?" -> GET /sites/{siteID}.{outputFormat}
- "Get occupant details?" -> GET /occupants/{occupantID}.{outputFormat}
- "Get pid details?" -> GET /parcels/pids/{siteID}.{outputFormat}
- "Get intersection details?" -> GET /intersections/{intersectionID}.{outputFormat}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
