---
name: ptv-timetable-api-version-3
description: "PTV Timetable API - Version 3 API skill. Use when working with PTV Timetable API - Version 3 for departures, directions, disruptions. Covers 26 endpoints."
version: 1.0.0
generator: lapsh
---

# PTV Timetable API - Version 3
API version: v3

## Auth
ApiKey token in query

## Base URL
https://timetableapi.ptv.vic.gov.au

## Setup
1. Set your API key in the appropriate header
2. GET /v3/disruptions -- verify access

## Endpoints

26 endpoints across 11 groups. See references/api-spec.lap for full details.

### departures
| Method | Path | Description |
|--------|------|-------------|
| GET | /v3/departures/route_type/{route_type}/stop/{stop_id} | View departures for all routes from a stop |
| GET | /v3/departures/route_type/{route_type}/stop/{stop_id}/route/{route_id} | View departures for a specific route from a stop |

### directions
| Method | Path | Description |
|--------|------|-------------|
| GET | /v3/directions/route/{route_id} | View directions that a route travels in |
| GET | /v3/directions/{direction_id} | View all routes for a direction of travel |
| GET | /v3/directions/{direction_id}/route_type/{route_type} | View all routes of a particular type for a direction of travel |

### disruptions
| Method | Path | Description |
|--------|------|-------------|
| GET | /v3/disruptions | View all disruptions for all route types |
| GET | /v3/disruptions/route/{route_id} | View all disruptions for a particular route |
| GET | /v3/disruptions/route/{route_id}/stop/{stop_id} | View all disruptions for a particular route and stop |
| GET | /v3/disruptions/stop/{stop_id} | View all disruptions for a particular stop |
| GET | /v3/disruptions/{disruption_id} | View a specific disruption |
| GET | /v3/disruptions/modes | Get all disruption modes |

### fare_estimate
| Method | Path | Description |
|--------|------|-------------|
| GET | /v3/fare_estimate/min_zone/{minZone}/max_zone/{maxZone} | Estimate a fare by zone |

### outlets
| Method | Path | Description |
|--------|------|-------------|
| GET | /v3/outlets | List all ticket outlets |
| GET | /v3/outlets/location/{latitude},{longitude} | List ticket outlets near a specific location |

### pattern
| Method | Path | Description |
|--------|------|-------------|
| GET | /v3/pattern/run/{run_ref}/route_type/{route_type} | View the stopping pattern for a specific trip/service run |

### routes
| Method | Path | Description |
|--------|------|-------------|
| GET | /v3/routes | View route names and numbers for all routes |
| GET | /v3/routes/{route_id} | View route name and number for specific route ID |

### route_types
| Method | Path | Description |
|--------|------|-------------|
| GET | /v3/route_types | View all route types and their names |

### runs
| Method | Path | Description |
|--------|------|-------------|
| GET | /v3/runs/route/{route_id} | View all trip/service runs for a specific route ID |
| GET | /v3/runs/route/{route_id}/route_type/{route_type} | View all trip/service runs for a specific route ID and route type |
| GET | /v3/runs/{run_ref} | View all trip/service runs for a specific run_ref |
| GET | /v3/runs/{run_ref}/route_type/{route_type} | View the trip/service run for a specific run_ref and route type |

### search
| Method | Path | Description |
|--------|------|-------------|
| GET | /v3/search/{search_term} | View stops, routes and myki ticket outlets that match the search term |

### stops
| Method | Path | Description |
|--------|------|-------------|
| GET | /v3/stops/{stop_id}/route_type/{route_type} | View facilities at a specific stop (Metro and V/Line stations only) |
| GET | /v3/stops/route/{route_id}/route_type/{route_type} | View all stops on a specific route |
| GET | /v3/stops/location/{latitude},{longitude} | View all stops near a specific location |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Get stop details?" -> GET /v3/departures/route_type/{route_type}/stop/{stop_id}
- "Get route details?" -> GET /v3/departures/route_type/{route_type}/stop/{stop_id}/route/{route_id}
- "Get route details?" -> GET /v3/directions/route/{route_id}
- "Get direction details?" -> GET /v3/directions/{direction_id}
- "Get route_type details?" -> GET /v3/directions/{direction_id}/route_type/{route_type}
- "List all disruptions?" -> GET /v3/disruptions
- "Get route details?" -> GET /v3/disruptions/route/{route_id}
- "Get stop details?" -> GET /v3/disruptions/route/{route_id}/stop/{stop_id}
- "Get stop details?" -> GET /v3/disruptions/stop/{stop_id}
- "Get disruption details?" -> GET /v3/disruptions/{disruption_id}
- "List all modes?" -> GET /v3/disruptions/modes
- "Get max_zone details?" -> GET /v3/fare_estimate/min_zone/{minZone}/max_zone/{maxZone}
- "List all outlets?" -> GET /v3/outlets
- "Get location details?" -> GET /v3/outlets/location/{latitude},{longitude}
- "Get route_type details?" -> GET /v3/pattern/run/{run_ref}/route_type/{route_type}
- "List all routes?" -> GET /v3/routes
- "Get route details?" -> GET /v3/routes/{route_id}
- "List all route_types?" -> GET /v3/route_types
- "Get route details?" -> GET /v3/runs/route/{route_id}
- "Get route_type details?" -> GET /v3/runs/route/{route_id}/route_type/{route_type}
- "Get run details?" -> GET /v3/runs/{run_ref}
- "Get route_type details?" -> GET /v3/runs/{run_ref}/route_type/{route_type}
- "Get search details?" -> GET /v3/search/{search_term}
- "Get route_type details?" -> GET /v3/stops/{stop_id}/route_type/{route_type}
- "Get route_type details?" -> GET /v3/stops/route/{route_id}/route_type/{route_type}
- "Get location details?" -> GET /v3/stops/location/{latitude},{longitude}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
