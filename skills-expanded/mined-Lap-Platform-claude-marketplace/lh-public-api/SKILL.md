---
name: lh-public-api
description: "LH Public API skill. Use when working with LH Public for references, offers, operations. Covers 15 endpoints."
version: 1.0.0
generator: lapsh
---

# LH Public API
API version: 1.0

## Auth
OAuth2

## Base URL
https://api.lufthansa.com/v1

## Setup
1. Configure auth: OAuth2
2. GET /references/countries/{countryCode} -- verify access

## Endpoints

15 endpoints across 4 groups. See references/api-spec.lap for full details.

### references
| Method | Path | Description |
|--------|------|-------------|
| GET | /references/countries/{countryCode} | Countries |
| GET | /references/cities/{cityCode} | Cities |
| GET | /references/airports/{airportCode} | Airports |
| GET | /references/airports/nearest/{latitude},{longitude} | Nearest Airports |
| GET | /references/airlines/{airlineCode} | Airlines |
| GET | /references/aircraft/{aircraftCode} | Aircraft |

### offers
| Method | Path | Description |
|--------|------|-------------|
| GET | /offers/seatmaps/{flightNumber}/{origin}/{destination}/{date}/{cabinClass} | Seat Maps |
| GET | /offers/lounges/{location} | Lounges |

### operations
| Method | Path | Description |
|--------|------|-------------|
| GET | /operations/flightstatus/{flightNumber}/{date} | Flight Status |
| GET | /operations/flightstatus/route/{origin}/{destination}/{date} | Flight Status by Route |
| GET | /operations/flightstatus/arrivals/{airportCode}/{fromDateTime} | Flight Status at Arrival Airport |
| GET | /operations/flightstatus/departures/{airportCode}/{fromDateTime} | Flight Status at Departure Airport |
| GET | /operations/schedules/{origin}/{destination}/{fromDateTime} | Flight Schedules |

### cargo
| Method | Path | Description |
|--------|------|-------------|
| GET | /cargo/shipmentTracking/{aWBPrefix}-{aWBNumber} | Shipment Tracking |
| GET | /cargo/getRoute/{origin}-{destination}/{fromDate}/{productCode} | Retrieve all flights |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Get country details?" -> GET /references/countries/{countryCode}
- "Get city details?" -> GET /references/cities/{cityCode}
- "Get airport details?" -> GET /references/airports/{airportCode}
- "Get nearest details?" -> GET /references/airports/nearest/{latitude},{longitude}
- "Get airline details?" -> GET /references/airlines/{airlineCode}
- "Get aircraft details?" -> GET /references/aircraft/{aircraftCode}
- "Get seatmap details?" -> GET /offers/seatmaps/{flightNumber}/{origin}/{destination}/{date}/{cabinClass}
- "Get lounge details?" -> GET /offers/lounges/{location}
- "Get flightstatus details?" -> GET /operations/flightstatus/{flightNumber}/{date}
- "Get route details?" -> GET /operations/flightstatus/route/{origin}/{destination}/{date}
- "Get arrival details?" -> GET /operations/flightstatus/arrivals/{airportCode}/{fromDateTime}
- "Get departure details?" -> GET /operations/flightstatus/departures/{airportCode}/{fromDateTime}
- "Get schedule details?" -> GET /operations/schedules/{origin}/{destination}/{fromDateTime}
- "Get shipmentTracking details?" -> GET /cargo/shipmentTracking/{aWBPrefix}-{aWBNumber}
- "Get getRoute details?" -> GET /cargo/getRoute/{origin}-{destination}/{fromDate}/{productCode}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
