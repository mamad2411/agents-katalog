---
name: imgw
display_name: IMGW-PIB Pogoda i Ostrzeżenia
version: 1.0.0
description: >-
  Fetch official meteorological and hydrological data for Poland from the Instytut Meteorologii
  i Gospodarki Wodnej (IMGW-PIB). Check current temperature, atmospheric pressure, humidity,
  wind speed and direction, and rainfall totals from synoptic stations (Warszawa, Kraków,
  Gdańsk, Zakopane and 58 others). Find the nearest weather station by GPS coordinates.
  Fetch official meteorological warnings (storms, gales, heat, frost) and hydrological
  warnings (hydrological drought, river water levels, alarm and warning levels on the Wisła,
  Odra, etc.). No API keys, 100% official public data. Use whenever the user asks about:
  "pogoda IMGW", "jaka jest temperatura w Warszawie", "ostrzeżenia IMGW", "stan Wisły",
  "stan wody", "alerty pogodowe", "ciśnienie", "wiatr", "opady w Polsce".
category: public_data
language: pl
country: PL
license: MIT
author: Michell Hoduń (https://github.com/b44x)
repository: https://github.com/b44x/ai-polish-skills
network: true
authentication: none
source: Instytut Meteorologii i Gospodarki Wodnej (IMGW-PIB)
source_type: official_api
official: true
homepage: https://imgw.pl
documentation: https://danepubliczne.imgw.pl/
rate_limit: fair use
last_verified: 2026-09-28
tags:
  - imgw
  - pogoda
  - synop
  - temperatura
  - cisnienie
  - wiatr
  - opady
  - ostrzezenia
  - alerty
  - hydro
  - rzeki
compatibility: Python 3.8+ (standard library only); network access to danepubliczne.imgw.pl.
---

# IMGW-PIB Weather, Alerts and Hydrology

Official skill integrating public data from the Instytut Meteorologii i Gospodarki Wodnej (IMGW-PIB)
via `scripts/imgw.py`. Works without API keys, uses only the Python standard library,
and returns structured JSON on `stdout`.

## Running the script

Run from the skill directory (or from the repository root path):

| Operating system | Command |
|---|---|
| Linux / macOS | `python3 scripts/imgw.py <command> …` |
| Windows | `py scripts/imgw.py <command> …` (or `python`) |

Zero external libraries (Python 3.8+ stdlib).

## Workflow

1. **Current weather for a specific city / station:**
   - When the user asks e.g. „Jaka jest teraz temperatura w Warszawie?”, „Pokaż pogodę z IMGW dla Zakopanego”:
     `python3 scripts/imgw.py weather Warszawa`
     `python3 scripts/imgw.py weather Kraków`
     `python3 scripts/imgw.py weather Zakopane`
   - The script automatically handles Polish diacritics (e.g. `Kraków` -> `krakow`),
     and safely handles mountain stations, where sea-level pressure is `null`.

2. **Finding the nearest IMGW station by GPS coordinates:**
   - When the user asks about weather in a town without a synoptic station (e.g. Sopot, Gdynia, Piaseczno)
     or provides GPS coordinates:
     `python3 scripts/imgw.py near 54.44 18.56`
   - Computes the great-circle (Haversine) distance to all 62 stations in Poland and automatically
     fetches current weather from the nearest station (in this example: Gdańsk, 7 km).

3. **Official IMGW warnings and alerts:**
   - When the user asks e.g. „Czy IMGW wydało ostrzeżenia dla województwa pomorskiego?”, „Czy są alerty pogodowe?”:
     `python3 scripts/imgw.py warnings --type all`
     `python3 scripts/imgw.py warnings --voivodeship pomorskie`
     `python3 scripts/imgw.py warnings --type meteo`

4. **River levels and flood / drought risk (Hydrology):**
   - When the user asks e.g. „Jaki jest stan wody na Wiśle?”, „Czy gdzieś w Polsce przekroczono stan alarmowy?”:
     `python3 scripts/imgw.py hydro --river Wisła`
     `python3 scripts/imgw.py hydro --alarm-only`
     `python3 scripts/imgw.py hydro --station Warszawa`

5. **Overview of all of Poland (Synop) or station list:**
   - Where it is currently warmest / coldest in Poland:
     `python3 scripts/imgw.py synop --sort temp_desc --limit 5`
     `python3 scripts/imgw.py synop --sort wind_desc --limit 5`
   - Checking available stations offline:
     `python3 scripts/imgw.py stations --search Poznań`

## Commands

| Command | Description | Returned data |
|---|---|---|
| `weather <station>` | Current weather from a synoptic station | `temperatureC`, `pressureHpa`, `windSpeedMs`, `windDirectionDeg`, `relativeHumidityPercent`, `rainfallMm`, `formatted`, `coordinates` |
| `near <lat> <lon> [--limit N]` | Nearest synoptic station to GPS coordinates | `closestStation` (with distance in km and weather), `nearbyStations` |
| `warnings [--type meteo\|hydro\|all] [--voivodeship V]` | Official meteo and hydro warnings | List of active alerts: `event`, `level`, `published`, `validFrom`, `validTo`, `course`, `voivodeships` |
| `hydro [--river R] [--station S] [--alarm-only]` | Measurements from water-gauge stations | `river`, `stationName`, `status`, `waterLevelCm`, `warningLevelCm`, `alarmLevelCm`, `waterTemperatureC` |
| `synop [--sort S] [--limit N]` | Overview of all 62 stations in Poland | Aggregate list of stations sorted by temperature, wind, pressure or name |
| `stations [--search Q]` | Catalog of synoptic stations (offline) | `stationId`, `stationName`, `slug`, `coordinates` |

Detailed description of schemas and fields: [references/output.md](references/output.md).

## Exit codes

Clean JSON goes to `stdout`; errors go to `stderr` as `{"error": "...", "type": "..."}`.

| Code | Meaning | Action |
|---|---|---|
| `0` | Success | Use the JSON data |
| `2` | Not found | Station or river does not exist in the IMGW database |
| `64` | Invalid invocation / validation | Check the command parameters or coordinates |
| `69` | IMGW server / network error | Temporary network error; try again |

## Rules

- Always cite the data source: **IMGW-PIB**.
- At mountain stations (e.g. Kasprowy Wierch, Śnieżka, Zakopane) pressure is often omitted (`null`), because it is not reduced to sea level in the standard way — inform the user about this.
- In responses to the user, use the ready-made formatted fields in the `formatted` object (`20.4 °C`, `1028.5 hPa`, `3.0 m/s (100°)`).
