---
name: smog
display_name: Smog — jakość powietrza GIOŚ
version: 1.0.0
description: >-
  Read official GIOŚ air quality measurements and the Polish air quality index. Find stations by city or the nearest station by GPS. Use for "smog", "jakość powietrza", "PM2.5", "PM10", "najbliższa stacja GIOŚ". Shows measurement times and missing data; does not provide forecasts or medical advice.
category: public_data
language: pl
country: PL
license: MIT
author: Michell Hoduń (https://github.com/b44x)
repository: https://github.com/b44x/ai-polish-skills
network: true
authentication: none
source: Główny Inspektorat Ochrony Środowiska (GIOŚ)
source_type: official_api
official: true
homepage: https://powietrze.gios.gov.pl/
documentation: https://powietrze.gios.gov.pl/pjp/content/api
rate_limit: Endpoint-specific limits; see GIOŚ documentation
last_verified: 2026-11-04
tags:
  - smog
  - powietrze
  - pm10
  - pm25
  - gios
  - jakosc-powietrza
compatibility: Python 3.8+ (standard library only); internet access required.
---

# GIOŚ air quality

## Running the script

Run from this skill's directory:

| OS | Command |
|---|---|
| Linux / macOS | `python3 scripts/smog.py <command> ...` |
| Windows | `py scripts/smog.py <command> ...` |

| Command | Purpose |
|---|---|
| `stations --city Kraków` | All stations in the city; `Krakow` also works |
| `stations` | GIOŚ station catalogue |
| `near 50.06 19.94` | Nearest station, straight-line distance, index and measurements |
| `station 400` | Index and latest available measurements for a station |

## Choosing a station and reporting results

1. For a city, call `stations --city` first. If several stations match, present the options; do not describe one station as the city-wide average. Use `near` for supplied coordinates.
2. Report the station name, **GIOŚ** attribution, value, unit and measurement time for each pollutant. All concentrations from this API, including CO, are in µg/m³. Measurement and index times are local Europe/Warsaw times; `fetched_at` is UTC.
3. `latest_slot_missing` means the latest time slot has no measurement and the result comes from an earlier slot. `no_current_data` and `null` mean missing data, never zero. Different sensors may report measurements from different hours.
4. Show the index category supplied by GIOŚ; do not calculate a separate index or substitute US AQI. Report missing or incomplete index status. The data is provisional and may be corrected later.
5. This skill does not provide forecasts, health advice or continuous monitoring. The nearest station may not reflect conditions at the user's exact address.

## API and exit codes

Use `https://api.gios.gov.pl/pjp-api/v1/rest/`. The script supports JSON-LD pagination without pip dependencies or API keys. Do not use the retired `/pjp-api/rest/` endpoint.

Success: JSON on stdout, exit `0`. Errors: JSON on stderr, exit `2` for a missing station, `64` for validation or `69` for API/network failures. Missing measurements at an existing station are a valid result with `null` fields. A sensor-fetch network failure stops the lookup instead of masquerading as a missing measurement. `--help` and `-h` return `0`.

Read [references/output.md](references/output.md) for field details. Source: [GIOŚ API documentation](https://powietrze.gios.gov.pl/pjp/content/api).
