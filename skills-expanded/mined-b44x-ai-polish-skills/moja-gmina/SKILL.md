---
name: moja-gmina
display_name: Moja gmina — statystyki GUS BDL
version: 1.0.0
description: >-
  Search official GUS BDL statistics and compare Polish municipalities, counties or voivodeships for a common year. Use for population, local demography, construction or unemployment comparisons, finding territorial units and statistical indicators. Preserves geographic levels, units of measure and missing-data attributes.
category: public_data
language: pl
country: PL
license: MIT
author: Michell Hoduń (https://github.com/b44x)
repository: https://github.com/b44x/ai-polish-skills
network: true
authentication: none
source: Główny Urząd Statystyczny — Bank Danych Lokalnych
source_type: official_api
official: true
homepage: https://bdl.stat.gov.pl/
documentation: https://api.stat.gov.pl/home/bdlapi
rate_limit: Anonymous 5 requests/s, 100/15 min, 1000/12 h, 10000/week; optional BDL_API_KEY increases limits.
last_verified: 2026-11-05
tags:
  - gus
  - bdl
  - gmina
  - powiat
  - demografia
  - ludnosc
  - statystyki
compatibility: Python 3.8+ (standard library only); internet access required.
---

# GUS BDL local statistics

## Running the script

Run `python3 scripts/moja_gmina.py <command>` from this skill's directory (`py` on Windows).

| Command | Purpose |
|---|---|
| `units "Piaseczno" --level 6` | Find municipalities, preserving unit type and parent identifier |
| `indicators "ludność" --level 6` | Search indicators and their dimensions |
| `indicators "bezrobotni" --level 5` | Find an appropriate county-level series |
| `indicator ludnosc` | Full definition and available years for total population (BDL 72305) |
| `compare --units <ID_BDL_1> <ID_BDL_2> --indicators ludnosc --year 2024` | Compare units found through `units` for a common year |
| `compare --units <ID_BDL_1> <ID_BDL_2> --indicators <INDICATOR_ID>` | Select the latest year with data for both units |

## Workflow and interpretation

1. Resolve units through `units`; the 12-digit BDL identifier differs from a shortened TERYT code. For matching names, inspect `level`, `kind` and `parentId`. An urban-rural municipality, its town and its rural part may be separate units.
2. Select an indicator through `indicators`, then inspect its full definition with `indicator`. Names `n1`…`n5`, unit of measure, geographic level and available years are part of the definition. Total and per-capita income are different series; wages or unemployment rates may not be available at municipality level.
3. `compare` accepts up to 10 units of the same level and up to 5 indicators. Without `--year`, it chooses the latest common year **separately for each indicator**. `no_common_data` means no comparable data; do not substitute another unit's latest year.
4. Cite **GUS, Bank Danych Lokalnych**, the year, unit of measure and indicator definition. Preserve attributes, methodological notes and territorial scope. `null`, absent observations and statistical confidentiality do not mean zero. Population size is neither a quality-of-life rating nor a forecast.

## Cache, availability and exit codes

Metadata is cached for 24 hours and data for 1 hour in `~/.cache/ai-polish-skills/moja-gmina`. Put `--no-cache` before the command to force a fetch. `requests` contains the URL, actual retrieval time and cache status. Root-level `fetched_at` is the response preparation time. Override the cache directory with `MOJA_GMINA_CACHE_DIR`. There is no fallback to expired data.

The API supports anonymous access; optionally set `BDL_API_KEY` for the `X-ClientId` header. On HTTP 429, the skill exits with 69 and reports `retry_after`; respect that delay before another attempt. Do not increase request frequency during an outage. During verification on 2026-11-05, official API documentation and the schema were available, but REST data requests timed out; offline tests do not confirm service availability.

Success: JSON on stdout, exit `0`. Errors: JSON on stderr, exit `2` for a missing resource/results, `64` for validation or `69` for network/API/format/rate-limit errors. `--help` returns `0`. Read [references/api.md](references/api.md) for API details.
