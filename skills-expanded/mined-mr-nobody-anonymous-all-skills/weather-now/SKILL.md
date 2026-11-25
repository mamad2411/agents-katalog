---
name: weather-now
description: Retrieve current weather and local conditions with location, timestamp, and source clarity.
category: utilities
aliases:
- weather
- forecast
- temperature
- conditions
triggers:
- What's the weather
- Weather forecast
- Current conditions
- Temperature
keywords:
- weather
- forecast
- temperature
- conditions
- location
dependencies:
- optional:weather-api
risk: low
version: 1.0.0
source: custom
enabled: true
capabilities:
- weather-now
- utilities
inputs:
- task
- context
outputs:
- result
- report
lifecycle: enabled
author: Mr-Nobody-Anonymous
tags:
- conditions
- forecast
- now
- temperature
- utilities
- weather
compatibility:
  claude-code: '>=1.0'
  skillhub: '*'
  cursor: '>=0.40'
  codex: '*'
network_access: false
filesystem_access: read
credential_access: false
destructive_operations: false
---

# Weather Now

## Purpose
Retrieve current weather conditions and forecasts with clear location identification,
timestamps, and data source attribution. The skill provides accurate weather information
for planning and decision-making.

## When to Use
- User asks about current weather or forecast
- Weather affects planned activities
- Including weather in summaries or reports

## When NOT to Use
- For critical decisions (aviation, emergency services)
- When precise instruments are required
- For historical weather data (use specialized services)

## Capabilities
- Current conditions (temperature, humidity, wind, precipitation)
- Hourly and daily forecasts
- Severe weather alerts
- Multiple location support
- Unit conversion (Celsius/Fahrenheit)
- Data source attribution
- Cache management for rate limits

## Inputs
- `location` (required) — city name, coordinates, or location ID
- `units` (optional) — metric or imperial
- `forecast` (optional) — current, hourly, daily, extended
- `include_alerts` (optional, default: true) — include severe weather

## Workflow
1. **Resolve** — Convert location to coordinates
2. **Fetch** — Query weather API
3. **Format** — Present in clear, readable format
4. **Attribute** — Include source and timestamp
5. **Cache** — Store for repeated queries

## Tools
- Weather API (OpenWeatherMap, WeatherAPI, etc.)
- Geocoding service

## Examples
**User:** "What's the weather in San Francisco?"
**Response:**
```
San Francisco, CA
Updated: Feb 9, 2026 at 10:30 AM PST
Source: OpenWeatherMap

Current: 58Â°F (14Â°C), Partly Cloudy
Humidity: 72%
Wind: 8 mph NW
Visibility: 10 miles

Today's Forecast:
- Morning: 54Â°F, Clear
- Afternoon: 62Â°F, Partly Cloudy
- Evening: 55Â°F, Clear

No severe weather alerts.
```

## Safety
- Always include data freshness timestamp
- Attribute data source
- Flag low-confidence forecasts
- Don't use for critical safety decisions

## Source
Auto-generated from openclawskills.net description.

## Notes
Maintained as part of canonical utilities category.
