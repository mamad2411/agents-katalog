---
name: idealspot-geodata
description: "IdealSpot GeoData API skill. Use when working with IdealSpot GeoData for data, geometries, traffic. Covers 7 endpoints."
version: 1.0.0
generator: lapsh
---

# IdealSpot GeoData
API version: 1.0

## Auth
ApiKey X-RapidAPI-Key in header

## Base URL
https://idealspot-geodata.p.rapidapi.com/api/v1

## Setup
1. Set your API key in the appropriate header
2. GET /data/insights -- verify access

## Endpoints

7 endpoints across 3 groups. See references/api-spec.lap for full details.

### data
| Method | Path | Description |
|--------|------|-------------|
| GET | /data/insights | Fetch Available Insights |
| GET | /data/insights/{insight_id:} | Fetch Insight Query Parameters |
| GET | /data/insights/{insight_id:}/query | Query Insight at Location |

### geometries
| Method | Path | Description |
|--------|------|-------------|
| GET | /geometries/regions/intersecting/{latitude}/{longitude} | Fetch Administrative Regions using Lat/Lng |
| GET | /geometries/geometry | Fetch Geometries |

### traffic
| Method | Path | Description |
|--------|------|-------------|
| GET | /traffic/roads/nearest/{latitude}/{longitude} | Fetch Nearest Road Segments |
| GET | /traffic/counts/{segment_id} | Vehicle Traffic Counts for Road Segment |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all insights?" -> GET /data/insights
- "Get insight details?" -> GET /data/insights/{insight_id:}
- "List all query?" -> GET /data/insights/{insight_id:}/query
- "Get intersecting details?" -> GET /geometries/regions/intersecting/{latitude}/{longitude}
- "List all geometry?" -> GET /geometries/geometry
- "Get nearest details?" -> GET /traffic/roads/nearest/{latitude}/{longitude}
- "Get count details?" -> GET /traffic/counts/{segment_id}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
