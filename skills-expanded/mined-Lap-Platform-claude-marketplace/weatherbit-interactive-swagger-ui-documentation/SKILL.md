---
name: weatherbit-interactive-swagger-ui-documentation
description: "Weatherbit - Interactive Swagger UI Documentation API skill. Use when working with Weatherbit - Interactive Swagger UI Documentation for alerts, current, history. Covers 18 endpoints."
version: 1.0.0
generator: lapsh
---

# Weatherbit - Interactive Swagger UI Documentation
API version: 2.0.0

## Auth
ApiKey key in query

## Base URL
https://api.weatherbit.io/v2.0

## Setup
1. Set your API key in the appropriate header
2. GET /alerts -- verify access

## Endpoints

18 endpoints across 5 groups. See references/api-spec.lap for full details.

### alerts
| Method | Path | Description |
|--------|------|-------------|
| GET | /alerts | Returns severe weather alerts issued by meteorological agencies - Given a lat/lon. |

### current
| Method | Path | Description |
|--------|------|-------------|
| GET | /current | Returns a Current Observation - Given a lat/lon. |
| GET | /current/lightning | Returns nearest and most recent lightning observations - Given a lat/lon. |
| GET | /current/airquality | Returns current air quality conditions - Given a geolocation. |

### history
| Method | Path | Description |
|--------|------|-------------|
| GET | /history/lightning | Returns lightning data by lat/lon from a given date. |
| GET | /history/airquality | Returns 72 hours of historical air quality conditions - Given a geolocation. |
| GET | /history/agweather | Returns Historical Agweather - Given a lat/lon. |
| GET | /history/daily | Returns Historical Observations - Given a lat/lon. |
| GET | /history/hourly | Returns Historical Observations - Given a lat/lon. |
| GET | /history/subhourly | Returns Historical Observations - Given a lat/lon. |
| GET | /history/energy | Returns Energy API response  - Given a single lat/lon. |

### forecast
| Method | Path | Description |
|--------|------|-------------|
| GET | /forecast/daily | Returns a daily forecast - Given Lat/Lon. |
| GET | /forecast/minutely | Returns a 60 minute precipitation forecast - Given Lat/Lon. |
| GET | /forecast/airquality | Returns 72 hour (hourly) Air Quality forecast - Given a geolocation. |
| GET | /forecast/hourly | Returns an hourly forecast - Given a lat/lon. |
| GET | /forecast/agweather | Returns Agweather Forecast - Given a lat/lon. |
| GET | /forecast/energy | Returns Energy Forecast API response  - Given a single lat/lon. |

### normals
| Method | Path | Description |
|--------|------|-------------|
| GET | /normals | Returns Historical Climate Normals (Averages) - Given a lat/lon. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all alerts?" -> GET /alerts
- "List all current?" -> GET /current
- "List all lightning?" -> GET /history/lightning
- "List all lightning?" -> GET /current/lightning
- "List all daily?" -> GET /forecast/daily
- "List all minutely?" -> GET /forecast/minutely
- "List all airquality?" -> GET /forecast/airquality
- "List all airquality?" -> GET /history/airquality
- "List all airquality?" -> GET /current/airquality
- "List all hourly?" -> GET /forecast/hourly
- "List all agweather?" -> GET /forecast/agweather
- "List all agweather?" -> GET /history/agweather
- "List all normals?" -> GET /normals
- "List all daily?" -> GET /history/daily
- "List all hourly?" -> GET /history/hourly
- "List all subhourly?" -> GET /history/subhourly
- "List all energy?" -> GET /forecast/energy
- "List all energy?" -> GET /history/energy
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
