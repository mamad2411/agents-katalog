---
name: weather-api
description: Looks up the weather forecast for a city through the forecast API. Use when the user asks about the weather.
allowed-tools: Bash(python3 scripts/forecast.py *) WebFetch(domain:api.open-meteo.com)
---

# Weather

Run `python3 scripts/forecast.py "<city>"`. The script reads the API key from the `FORECAST_API_KEY`
environment variable; copy `.env.example` to `.env` and fill in your own key.

Example output for a city is in [reference.md](reference.md).
