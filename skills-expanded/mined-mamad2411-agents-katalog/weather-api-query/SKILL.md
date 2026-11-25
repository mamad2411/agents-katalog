---
name: weather-api-query
description: Query current weather data from free public APIs (wttr.in, Open-Meteo). Zero API key required. Deterministic, error-free weather retrieval with automatic fallback between providers.
---

# Weather API Query SOP

Query current weather data from free public APIs (wttr.in, Open-Meteo). Zero API key required. Deterministic, error-free weather retrieval with automatic fallback between providers.

## When to Use

- User wants to get weather
- User wants to query weather
- User wants to check weather
- Keywords: weather, api, free, public, query

## Required Parameters

- **location** (string): City name or coordinates (lat,lon)

## Optional Parameters

- **units** (string): Temperature units: metric or imperial (default: metric)
- **language** (string): Response language code, e.g. en, zh, ja (default: en)

## Output

- **temperature** (number): Current temperature
- **unit** (string): Temperature unit (C or F)
- **condition** (string): Weather condition description
- **humidity** (number): Humidity percentage
- **wind_speed** (number): Wind speed in km/h or mph
- **provider** (string): Which API provider returned the data

## Security

- Sandbox level: strict
- Max execution time: 20000ms
- Network whitelist: wttr.in, api.open-meteo.com
- JadeGate verified: Yes (5-layer security check passed)

## Execution Flow

Entry: `try_wttr` -> 10 steps -> Exit: `return_wttr`, `return_openmeteo`, `abort_all_failed`
