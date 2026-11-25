---
name: odjazdy
display_name: Odjazdy — Gdańsk, Poznań i Szczecin
version: 1.0.0
description: >-
  Find public transport stops and upcoming bus or tram departures in Gdańsk, Poznań and Szczecin using transport operators' public services. Use for "kiedy tramwaj", "odjazdy z przystanku", "opóźnienie autobusu". Distinguishes realtime predictions, schedules, canceled services and stale data. Coverage is limited to the three supported networks; no route planning or ticket purchases.
category: utilities
language: pl
country: PL
license: MIT
author: Michell Hoduń (https://github.com/b44x)
repository: https://github.com/b44x/ai-polish-skills
network: true
authentication: none
source: ZTM Gdańsk, ZTM Poznań (PEKA), ZDiTM Szczecin
source_type: official_api
official: true
homepage: https://www.zditm.szczecin.pl/pl/zditm/dla-programistow
documentation: https://www.zditm.szczecin.pl/pl/zditm/dla-programistow/api-tablice-odjazdow
rate_limit: Szczecin 100 requests/minute/IP; one-shot lookups, upstream HTTP cache honored
last_verified: 2026-11-05
tags:
  - odjazdy
  - komunikacja-miejska
  - autobus
  - tramwaj
  - gdansk
  - poznan
  - szczecin
compatibility: Python 3.8+ (standard library only); internet access required except cities.
---

# Public transport departures

## Running the script

Run `python3 scripts/odjazdy.py <command>` from this skill's directory (`py` on Windows).

| Command | Purpose |
|---|---|
| `cities` | Supported networks, sources and capabilities; works offline |
| `stops Gdańsk --query "Dworzec Główny"` | Find individual stop poles/platforms by name |
| `stops Szczecin --lat 53.4285 --lon 14.5528 --limit 5` | Nearest stops by straight-line distance |
| `stops Poznań --query "Rondo Kaponiera"` | PEKA stops and directions; GPS lookup is not supported in Poznań |
| `departures gdansk 2001 --limit 5` | Departure board for an identifier returned by `stops` |
| `departures poznan RKAP71 --line 3` | One line's departures; use `id`, not `public_code` |
| `departures szczecin 10822` | ZDiTM departures and messages |

## Choosing a stop and interpreting results

1. Resolve city, stop name and direction. Call `stops` first, then `departures` with `id`. Several matches usually mean different poles/platforms or directions; do not arbitrarily choose the other side of the street. City names accept Polish diacritics or ASCII spelling. PEKA uses provider suggestions and may require diacritics in stop names.
2. Show the line, direction, time and status of each service. `realtime` means a provider prediction, `scheduled` means a timetable entry and `canceled` means a canceled service. Do not guarantee arrival times. Include `messages` and `warnings`.
3. ISO timestamps from Gdańsk/Szczecin are UTC with `Z`; display them in Europe/Warsaw, accounting for date and daylight-saving changes. `fetched_at` is retrieval time; `source_updated_at` is source time. Explicitly flag `freshness: stale` or `measurement_stale: true`. An absent source timestamp means `freshness: unknown`.
4. **PEKA uses a distinct time format:** `scheduled_local` contains Europe/Warsaw local time. The provider appends `Z` to a local clock reading, so do not interpret `provider_departure_raw` as valid UTC. For realtime services, prefer `minutes`; `estimated_at` is an approximation derived from those minutes and the server clock. PEKA does not publish the last measurement time: freshness remains unknown even with `realtime`.
5. `usable_realtime` is true only for a board with confirmed fresh time, a non-canceled service and no detected stale position. False alone does not turn a scheduled service into a cancellation.
6. An empty board (`no_departures`) reflects the provider's time window and filters. It does not mean no service exists for the whole day. The nearest stop is not necessarily the best route; the skill does not plan transfers or buy tickets.

## Sources and limits

Coverage is limited to **three networks: Gdańsk, Poznań and Szczecin**, including suburban stops present in their data. Do not claim nationwide coverage. The Gdańsk catalogue may contain other operators' stops with empty ZTM boards. Kraków and other cities have no adapters in this version.

Cite the source and data time, and identify the transformation (field normalization, filtering and any distance/minute calculations). Gdańsk: CC BY; Szczecin: CC0 1.0; Poznań: reuse terms require source, update and transformation information. Read [references/providers.md](references/providers.md) for provider details and links.

The script honors HTTP `Cache-Control` and `ETag`. Without HTTP guidance, the Gdańsk catalogue is cached for an hour and departure boards are not cached. `ODJAZDY_CACHE_DIR` overrides the cache directory. A network failure does not return an old board as current. Do not start frequent background polling for an ordinary departure request.

## Output and exit codes

Success: JSON on stdout, exit `0`. Errors: JSON on stderr, exit `2` for a missing stop/resource, `64` for invalid arguments or an unsupported city, or `69` for API/network/format errors. `--help` and `-h` return `0`.
