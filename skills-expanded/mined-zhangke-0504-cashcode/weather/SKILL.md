---
name: weather
description: Get current weather and forecasts. Use for temperature, rain, wind, humidity, or forecast questions for a place.
version: 1
tags: [weather, forecast, temperature, rain]
triggers: [weather today, tomorrow forecast, temperature, will it rain]
requires:
  tools: [web_fetch]
optional:
  tools: [web_search]
---

# Weather

Use current external data; never answer a current-weather question from memory.

1. Resolve an ambiguous place with `web_search` or ask the user for region/country.
2. Fetch a compact response from `https://wttr.in/<url-encoded-place>?format=j1` with `web_fetch`.
3. If that source fails, use Open-Meteo after resolving latitude and longitude.
4. Report location, observation/forecast time, conditions, temperature, precipitation, and wind in the user's units.
5. State the source and distinguish observations from forecasts.

Do not execute package scripts or request an API key for these public sources.
