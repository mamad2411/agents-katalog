---
name: bc-route-planner-rest-api
description: "BC Route Planner REST API skill. Use when working with BC Route Planner REST for distance.{outputFormat}, distance, route.{outputFormat}. Covers 22 endpoints."
version: 1.0.0
generator: lapsh
---

# BC Route Planner REST API
API version: 2.0.0

## Auth
ApiKey apikey in header

## Base URL
https://router.api.gov.bc.ca/

## Setup
1. Set your API key in the appropriate header
2. GET /distance.{outputFormat} -- verify access
3. POST /distance.{outputFormat} -- create first distance.{outputFormat}

## Endpoints

22 endpoints across 7 groups. See references/api-spec.lap for full details.

### distance.{outputFormat}
| Method | Path | Description |
|--------|------|-------------|
| GET | /distance.{outputFormat} | Get distance and travel time between two geographic points |
| POST | /distance.{outputFormat} | Get distance and travel time between two geographic points |

### distance
| Method | Path | Description |
|--------|------|-------------|
| GET | /distance/betweenPairs.{outputFormat} | Get distance and travel time between each pair of geographic points |
| POST | /distance/betweenPairs.{outputFormat} | Get distance and travel time between each pair of geographic points |

### route.{outputFormat}
| Method | Path | Description |
|--------|------|-------------|
| GET | /route.{outputFormat} | Get the path, distance and travel time between a series of geographic points |
| POST | /route.{outputFormat} | Get the path, distance and travel time between a series of geographic points |

### directions.{outputFormat}
| Method | Path | Description |
|--------|------|-------------|
| GET | /directions.{outputFormat} | Get the directions, path, distance and travel time between a series of geographic points |
| POST | /directions.{outputFormat} | Get the directions, path, distance and travel time between a series of geographic points |

### optimalRoute.{outputFormat}
| Method | Path | Description |
|--------|------|-------------|
| GET | /optimalRoute.{outputFormat} | Get the optimal path, distance and travel time between a start point and a series of end points which are reordered to minimize total distance or time. |
| POST | /optimalRoute.{outputFormat} | Get the path, distance and travel time between a start point and a series of end points which are reordered to minimize total distance or time. |

### optimalDirections.{outputFormat}
| Method | Path | Description |
|--------|------|-------------|
| GET | /optimalDirections.{outputFormat} | Get the directions, optimal path, distance and travel time between a start point and a series of end points which are reordered to minimize total distance or time. |
| POST | /optimalDirections.{outputFormat} | Get the directions, optimal path, distance and travel time between a start point and one or more end points which are reordered to minimize total distance or time. |

### truck
| Method | Path | Description |
|--------|------|-------------|
| GET | /truck/distance.{outputFormat} | Get distance and travel time between two geographic points for a commercial vehicle |
| POST | /truck/distance.{outputFormat} | Get distance and travel time between two geographic points |
| GET | /truck/route.{outputFormat} | Get the path, distance and travel time between a series of geographic points for a commercial vehicle |
| POST | /truck/route.{outputFormat} | Get the path, distance and travel time between a series of geographic points |
| GET | /truck/directions.{outputFormat} | Get the directions, path, distance and travel time between a series of geographic points for a commercial vehicle |
| POST | /truck/directions.{outputFormat} | Get the directions, path, distance and travel time between a series of geographic points |
| GET | /truck/optimalRoute.{outputFormat} | Get the optimal path, distance and travel time between a start point and a series of end points which are reordered to minimize total distance or time for a commercial vehicle |
| POST | /truck/optimalRoute.{outputFormat} | Get the path, distance and travel time between a start point and a series of end points which are reordered to minimize total distance or time. |
| GET | /truck/optimalDirections.{outputFormat} | Get the directions, optimal path, distance and travel time between a start point and a series of end points which are reordered to minimize total distance or time for a commercial vehicle |
| POST | /truck/optimalDirections.{outputFormat} | Get the directions, optimal path, distance and travel time between a start point and one or more end points which are reordered to minimize total distance or time. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Get distance.{outputFormat} details?" -> GET /distance.{outputFormat}
- "Get betweenPairs.{outputFormat} details?" -> GET /distance/betweenPairs.{outputFormat}
- "Get route.{outputFormat} details?" -> GET /route.{outputFormat}
- "Get directions.{outputFormat} details?" -> GET /directions.{outputFormat}
- "Get optimalRoute.{outputFormat} details?" -> GET /optimalRoute.{outputFormat}
- "Get optimalDirections.{outputFormat} details?" -> GET /optimalDirections.{outputFormat}
- "Get distance.{outputFormat} details?" -> GET /truck/distance.{outputFormat}
- "Get route.{outputFormat} details?" -> GET /truck/route.{outputFormat}
- "Get directions.{outputFormat} details?" -> GET /truck/directions.{outputFormat}
- "Get optimalRoute.{outputFormat} details?" -> GET /truck/optimalRoute.{outputFormat}
- "Get optimalDirections.{outputFormat} details?" -> GET /truck/optimalDirections.{outputFormat}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
