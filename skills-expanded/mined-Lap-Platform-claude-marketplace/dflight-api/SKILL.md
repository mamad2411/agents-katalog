---
name: dflight-api
description: "DFlight API skill. Use when working with DFlight for us. Covers 24 endpoints."
version: 1.0.0
generator: lapsh
---

# DFlight API
API version: V 1.0.0

## Auth
ApiKey x-api-key in header

## Base URL
https://dflight-api.ljaero.com/

## Setup
1. Set your API key in the appropriate header
3. POST /us/v1/airspace/distance-query -- create first distance-query

## Endpoints

24 endpoints across 1 groups. See references/api-spec.lap for full details.

### us
| Method | Path | Description |
|--------|------|-------------|
| POST | /us/v1/airspace/distance-query | Retrieve all requested types of airspace located within given distance of location. |
| POST | /us/v1/airspace/route-query | Retrieve all requested types of airspace traversed by route. |
| POST | /us/v1/airspace/polygon-query | Retrieve all requested types of airspace located within given GeoJSON Polygon. |
| POST | /us/v1/wx-forecast/distance-query | Retrieve forecast values within given distance of location for all requested weather elements and time periods. |
| POST | /us/v1/wx-forecast/route-query | Retrieve forecast values along a route for all requested weather elements and time periods. |
| POST | /us/v1/wx-forecast/polygon-query | Retrieve forecast values within given GeoJSON polygon for all requested weather elements and time periods. |
| POST | /us/v1/restrictions/distance-query | Retrieve flight restrictions applicable within given distance of location. |
| POST | /us/v1/restrictions/route-query | Retrieve flight restrictions applicable along route. |
| POST | /us/v1/restrictions/polygon-query | Retrieve flight restrictions applicable within given area. |
| POST | /us/v1/ssa/distance-query | Retrieve all special security areas located within given distance of location. |
| POST | /us/v1/ssa/route-query | Retrieve all special security areas traversed by route. |
| POST | /us/v1/ssa/polygon-query | Retrieve all special security areas located within given GeoJSON Polygon. |
| POST | /us/v1/venues/distance-query | Retrieve all restricted public venues located within given distance of location. |
| POST | /us/v1/venues/route-query | Retrieve all restricted public venues traversed by route. |
| POST | /us/v1/venues/polygon-query | Retrieve all restricted public venues located within given GeoJSON Polygon. |
| POST | /us/v1/obstacles/distance-query | Retrieve obstacles within given distance of location. |
| POST | /us/v1/obstacles/route-query | Retrieve obstacles found along a route. |
| POST | /us/v1/obstacles/polygon-query | Retrieve obstacles located within given area. |
| POST | /us/v1/uoa/distance-query | Retrieve UAS Operating Areas (UOAs) found within given distance of location. |
| POST | /us/v1/uoa/route-query | Retrieve UAS Operating Areas (UOAs) found along route. |
| POST | /us/v1/uoa/polygon-query | Retrieve UAS Operating Areas (UOAs) found within given area. |
| POST | /us/v1/aerodromes/distance-query | Retrieve aerodromes within given distance of location. |
| POST | /us/v1/aerodromes/route-query | Retrieve aerodromes found along a route. |
| POST | /us/v1/aerodromes/polygon-query | Retrieve aerodromes located within given area. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a distance-query?" -> POST /us/v1/airspace/distance-query
- "Create a route-query?" -> POST /us/v1/airspace/route-query
- "Create a polygon-query?" -> POST /us/v1/airspace/polygon-query
- "Create a distance-query?" -> POST /us/v1/wx-forecast/distance-query
- "Create a route-query?" -> POST /us/v1/wx-forecast/route-query
- "Create a polygon-query?" -> POST /us/v1/wx-forecast/polygon-query
- "Create a distance-query?" -> POST /us/v1/restrictions/distance-query
- "Create a route-query?" -> POST /us/v1/restrictions/route-query
- "Create a polygon-query?" -> POST /us/v1/restrictions/polygon-query
- "Create a distance-query?" -> POST /us/v1/ssa/distance-query
- "Create a route-query?" -> POST /us/v1/ssa/route-query
- "Create a polygon-query?" -> POST /us/v1/ssa/polygon-query
- "Create a distance-query?" -> POST /us/v1/venues/distance-query
- "Create a route-query?" -> POST /us/v1/venues/route-query
- "Create a polygon-query?" -> POST /us/v1/venues/polygon-query
- "Create a distance-query?" -> POST /us/v1/obstacles/distance-query
- "Create a route-query?" -> POST /us/v1/obstacles/route-query
- "Create a polygon-query?" -> POST /us/v1/obstacles/polygon-query
- "Create a distance-query?" -> POST /us/v1/uoa/distance-query
- "Create a route-query?" -> POST /us/v1/uoa/route-query
- "Create a polygon-query?" -> POST /us/v1/uoa/polygon-query
- "Create a distance-query?" -> POST /us/v1/aerodromes/distance-query
- "Create a route-query?" -> POST /us/v1/aerodromes/route-query
- "Create a polygon-query?" -> POST /us/v1/aerodromes/polygon-query
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
