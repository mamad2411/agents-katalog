---
name: weather
description: Get a forecast for a US location from the National Weather Service.
---

Call https://api.weather.gov/points/{lat},{lon} and then the forecast URL it returns.
Send the header `User-Agent: $WEATHER_CONTACT`. No API key is needed.
