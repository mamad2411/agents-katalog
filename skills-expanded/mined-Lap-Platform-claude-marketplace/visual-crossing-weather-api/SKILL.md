---
name: visual-crossing-weather-api
description: "Visual Crossing Weather API skill. Use when working with Visual Crossing Weather for VisualCrossingWebServices. Covers 5 endpoints."
version: 1.0.0
generator: lapsh
---

# Visual Crossing Weather API
API version: 4.6

## Auth
Requires API key (key parameter)

## Base URL
https://weather.visualcrossing.com

## Setup
1. Include your API key via the key parameter
2. GET /VisualCrossingWebServices/rest/services/weatherdata/forecast -- verify access

## Endpoints

5 endpoints across 1 groups. See references/api-spec.lap for full details.

### VisualCrossingWebServices
| Method | Path | Description |
|--------|------|-------------|
| GET | /VisualCrossingWebServices/rest/services/timeline/{location} | Historical and Forecast Weather API |
| GET | /VisualCrossingWebServices/rest/services/timeline/{location}/{startdate} | Historical and Forecast Weather API |
| GET | /VisualCrossingWebServices/rest/services/timeline/{location}/{startdate}/{enddate} | Historical and Forecast Weather API |
| GET | /VisualCrossingWebServices/rest/services/weatherdata/forecast | Weather Forecast API |
| GET | /VisualCrossingWebServices/rest/services/weatherdata/history | Retrieves hourly or daily historical weather records. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Get timeline details?" -> GET /VisualCrossingWebServices/rest/services/timeline/{location}
- "Get timeline details?" -> GET /VisualCrossingWebServices/rest/services/timeline/{location}/{startdate}
- "Get timeline details?" -> GET /VisualCrossingWebServices/rest/services/timeline/{location}/{startdate}/{enddate}
- "List all forecast?" -> GET /VisualCrossingWebServices/rest/services/weatherdata/forecast
- "List all history?" -> GET /VisualCrossingWebServices/rest/services/weatherdata/history

## Response Tips
- Check response schemas in references/api-spec.lap for field details

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
