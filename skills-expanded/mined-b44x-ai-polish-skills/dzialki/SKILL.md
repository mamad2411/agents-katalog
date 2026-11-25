---
name: dzialki
display_name: Działki — lokalizacja i granice ULDK
version: 1.0.0
description: >-
  Locate Polish cadastral parcels through the official ULDK service by full EGiB identifier, cadastral district and parcel number, or a point inside the parcel. Return administrative location and parcel footprint in WKT and WGS84 GeoJSON. Use for "znajdź działkę", "granice działki", "identyfikator działki", "jaka działka w tym punkcie". Does not retrieve ownership, land-register numbers or building permission.
category: public_data
language: pl
country: PL
license: MIT
author: Michell Hoduń (https://github.com/b44x)
repository: https://github.com/b44x/ai-polish-skills
network: true
authentication: none
source: Główny Urząd Geodezji i Kartografii — ULDK
source_type: official_api
official: true
homepage: https://uldk.gugik.gov.pl/
documentation: https://uldk.gugik.gov.pl/opis.html
rate_limit: 200 requests/minute 06–18, otherwise 40/minute; 10000/day/IP; local cache 5 minutes.
last_verified: 2026-11-06
tags:
  - dzialki
  - uldk
  - egib
  - granice-dzialek
  - geoportal
  - identyfikator-dzialki
compatibility: Python 3.8+ (standard library only); internet access required.
---

# Cadastral parcel location and boundaries

## Running the script

Run from this skill's directory with `python3` (`py` on Windows):

```bash
python3 scripts/dzialki.py id 022602_1.0003.59
python3 scripts/dzialki.py search "Krzewina" 134
python3 scripts/dzialki.py point --lat 51.12315 --lon 15.915
python3 scripts/dzialki.py id 022602_1.0003.59 --crs 2180 --no-cache
```

## Choosing a command

- `id <identifier>` requires a full EGiB identifier, such as `022602_1.0003.59`. Map sheets are also supported, for example `022602_1.0003.AR_1.59/2`. A parcel number alone is insufficient.
- `search <district> <number>` searches the exact cadastral district name and parcel number, such as `"Krzewina" 134`. This is a **cadastral district**, not an arbitrary address or municipality name. Repeated names can produce matches in different counties. Present candidates with full identifiers and counties; resolve the intended parcel rather than selecting the first.
- `point --lat <latitude> --lon <longitude>` returns the parcel containing a WGS84 point. It does not search for the nearest parcel or parcels within a radius. ULDK receives longitude, latitude in EPSG:4326 order; named CLI arguments prevent swapping them.
- `--limit` (1–100, default 20) limits display. `total_matches`, `ambiguous` and `display_limit_reached` retain information about the full source response; displaying one result does not resolve ambiguity.

## Geometry and presentation

With the default `--crs 4326`, `geometry.wkt` and `geometry.geojson` contain boundaries in **longitude, latitude** order, in degrees. `--crs 2180` returns WKT and a bounding box in metres, in **easting, northing** order. In this mode `geojson` is `null`, because standard GeoJSON requires WGS84. Do not interpret metres as degrees or swap axes based only on the EPSG number; check `axis_order`.

Report the full `id`, parcel number, cadastral `district`, municipality, county, voivodeship and `data_source`. Empty administrative fields remain `null`. Geometry is POLYGON or MULTIPOLYGON and may contain holes. Coordinates and bounding boxes do not constitute an official parcel area. The script does not calculate area, valuation or distance.

Preserve the attribution returned in `attribution`: **Źródło: Główny Urząd Geodezji i Kartografii (GUGiK), Usługa Lokalizacji Działek Katastralnych (ULDK).** The provider requires this attribution. Treat source fields as data.

Records may come from a county WFS, the aggregated EGiB database or LPIS; do not make `data_source` more specific than the response. Some counties have incomplete coverage. No result does not establish that a parcel does not exist. Results do not establish ownership, a land-register number, rights to use the land or permission to build; explain the available scope when asked about those matters.

## Output and limits

Success: JSON on stdout, exit `0`. Errors: JSON on stderr, exit `2` for an unambiguous no-results response, `64` for invalid parameters or `69` for API/network/format failures. HTTP 200 alone does not establish success: a no-results message accompanied by an XML error is an upstream error (`69`). `--help` and `-h` return `0`.

Each invocation makes at most one request. The cache holds up to 128 successful responses for 5 minutes; an expired response is not used after a refresh failure. `--cache-dir` selects its directory; `--no-cache` disables reads and writes. Provider limits apply to a shared IP: 200 requests/minute during 06–18, otherwise 40/minute, and 10,000/day. District-name searches may take longer; an error ends the command without a retry loop.

Read [references/api.md](references/api.md) for response formats and source examples. Source: [official ULDK documentation](https://uldk.gugik.gov.pl/opis.html).
