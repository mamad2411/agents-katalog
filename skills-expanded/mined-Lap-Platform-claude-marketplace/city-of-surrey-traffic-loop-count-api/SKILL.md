---
name: city-of-surrey-traffic-loop-count-api
description: "City of Surrey Traffic Loop Count API. API skill. Use when working with City of Surrey Traffic Loop Count API. for TrafficLoops.fmw, TrafficLoopCounts.fmw. Covers 2 endpoints."
version: 1.0.0
generator: lapsh
---

# City of Surrey Traffic Loop Count API.
API version: 0.1

## Auth
No authentication required.

## Base URL
http://gis.surrey.ca:8080/fmedatastreaming/TrafficLoopCount

## Setup
1. No auth setup needed
2. GET /TrafficLoops.fmw -- verify access

## Endpoints

2 endpoints across 2 groups. See references/api-spec.lap for full details.

### TrafficLoops.fmw
| Method | Path | Description |
|--------|------|-------------|
| GET | /TrafficLoops.fmw | Provides all the traffic loops maintained by the City of Surrey in GeoJSON format. LANE_DIRECTION indicates the heading of the traffic (NB, SB, EB, WB). INTERSECTION_ID corresponds to the INTID field in the intersections dataset which can be found on the Surrey Open Data site. ROAD_FACILITYID indicates which road segment the loop is located on.  This corresponds to the FACILITYID in the Road Centrelines dataset on the City of Surrey Open Data site. |

### TrafficLoopCounts.fmw
| Method | Path | Description |
|--------|------|-------------|
| GET | /TrafficLoopCounts.fmw | Provides traffic loop counts for the input time interval. The LOOP_ID and DATETIME combinations are unique in the output. The output timestamp will contain the time zone offset, either -08 (PST) or -07 (PDT) depending on whether daylight savings time was observed at the output datetime. In order to work with local time you may omit the time zone offset from the input and truncate it from the output. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all TrafficLoops.fmw?" -> GET /TrafficLoops.fmw
- "List all TrafficLoopCounts.fmw?" -> GET /TrafficLoopCounts.fmw

## Response Tips
- Check response schemas in references/api-spec.lap for field details

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
