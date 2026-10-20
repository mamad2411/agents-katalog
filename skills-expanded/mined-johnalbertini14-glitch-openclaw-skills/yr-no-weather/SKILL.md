---
name: yr-weather
description: Fetch weather forecasts from the Norwegian Meteorological Institute (MET) using the yr.no API. Use when the user asks for weather information, forecasts, temperature, precipitation, wind conditions, or any weather-related queries for specific locations. Supports coordinates-based lookups and returns current conditions plus forecasts.
---

# Yr.no Weather

Get weather forecasts from the Norwegian Meteorological Institute (MET Norway) via the free yr.no API.

## Overview

This skill provides weather data using MET Norway's Locationforecast API — a free, reliable weather service with global coverage. No API key required.

**Features:**
- Current weather conditions
- Hourly forecasts (up to 9 days)
- Temperature, wind, humidity, precipitation
- Weather symbols with emoji display

## Quick Start

```bash
# Get current weather for Cape Town (default)
python3 {baseDir}/scripts/weather.py

# Get weather for specific coordinates
python3 {baseDir}/scripts/weather.py -33.9288 18.4174

# Get weather with altitude
python3 {baseDir}/scripts/weather.py 59.9139 10.7522 100

# Get tomorrow's forecast
python3 {baseDir}/scripts/tomorrow.py

# Get tomorrow's forecast for specific location
python3 {baseDir}/scripts/tomorrow.py -33.9288 18.4174
```

## API Details

**Endpoint:** `https://api.met.no/weatherapi/locationforecast/2.0/compact`

**Parameters:**
- `lat`: Latitude (-90 to 90)
- `lon`: Longitude (-180 to 180)
- `altitude`: Altitude in meters (optional)

**Response:** JSON with timeseries data containing:
- `instant.details.air_temperature` - Temperature in °C
- `instant.details.wind_speed` - Wind speed in m/s
- `instant.details.relative_humidity` - Humidity in %
- `next_1_hours.summary.symbol_code` - Weather condition symbol
- `next_1_hours.details.precipitation_amount` - Rain/snow in mm

## Weather Symbols

| Symbol | Description |
|--------|-------------|
| clearsky | Clear sky |
| fair | Fair weather |
| partlycloudy | Partly cloudy |
| cloudy | Cloudy |
| rain | Rain |
| lightrain | Light rain |
| heavyrain | Heavy rain |
| rainshowers | Rain showers |
| sleet | Sleet |
| snow | Snow |
| lightsnow | Light snow |
| heavysnow | Heavy snow |
| snowshowers | Snow showers |
| fog | Fog |

Symbols may have suffixes like `_day`, `_night`, `_polartwilight` for time-of-day variants.

## Common Locations

| City | Latitude | Longitude |
|------|----------|-----------|
| Cape Town | -33.9288 | 18.4174 |
| Johannesburg | -26.2041 | 28.0473 |
| Durban | -29.8587 | 31.0218 |
| London | 51.5074 | -0.1278 |
| New York | 40.7128 | -74.0060 |
| Tokyo | 35.6762 | 139.6503 |
| Sydney | -33.8688 | 151.2093 |

## Usage Terms

**Required by MET Norway:**
- Include User-Agent header with contact info
- Cache responses (don't request more than once per 10 minutes for same location)
- Attribute data to "MET Norway" when displaying

This script complies with all terms of use.
