---
name: inpost
display_name: InPost & Paczkomaty
version: 1.0.0
description: >-
  Track InPost shipments and find Paczkomat parcel lockers and pickup points across Poland.
  Check shipment status and historical events by 24-digit tracking number (e.g. "gdzie moja paczka InPost",
  "status przesyłki"). Look up Paczkomat locker details by code (e.g. WAW01M, KRA01A) including address,
  location description, 24/7 accessibility, easy access zone (Strefa Łatwego Dostępu), payment options,
  and photo. Search lockers by city, street, postal code, or find nearest Paczkomaty by GPS coordinates
  with distances in meters. Use whenever the user asks about an InPost parcel, Paczkomat location,
  "gdzie jest paczkomat", "najbliższy paczkomat", or pastes an InPost tracking link/number.
category: logistics
language: pl
country: PL
license: MIT
author: Michell Hoduń (https://github.com/b44x)
repository: https://github.com/b44x/ai-polish-skills
network: true
authentication: none
source: InPost ShipX API
source_type: public_api
official: false
homepage: https://inpost.pl
documentation: https://dokumentacja-inpost.atlassian.net/wiki/spaces/PL/pages/11731057/ShipX+API
rate_limit: fair use
last_verified: 2026-09-28
tags:
  - inpost
  - paczkomaty
  - tracking
  - przesylki
  - kurier
  - logistyka
compatibility: Python 3.8+ (standard library only); network access to api-shipx-pl.easypack24.net.
---

# InPost & Paczkomaty

Tracks parcels and searches for Paczkomat lockers and pickup points across Poland using
`scripts/inpost.py`. Always outputs structured JSON.

## Running the script

Run from this skill's directory (or use relative path from repo root):

| OS | Command |
|---|---|
| Linux / macOS | `python3 scripts/inpost.py <command> …` |
| Windows | `py scripts/inpost.py <command> …` (or `python`) |

Zero external dependencies required (standard library only).

## Workflow

1. **Parcel Tracking:**
   - User provides a 24-digit tracking number or InPost link:
     `python3 scripts/inpost.py track <number>`
   - Report the current status title (`statusTitle`), timestamp, and if present, target locker (`targetMachine`).
   - If the user wants full journey history, list items from `events`.

2. **Finding a Paczkomat / Locker Point:**
   - **By locker code** (e.g. `WAW01M`, `KRA01A`):
     `python3 scripts/inpost.py point <name>`
   - **By city / address / street**:
     `python3 scripts/inpost.py search --city "Warszawa" --query "Chmielna"`
   - **By postal code**:
     `python3 scripts/inpost.py search --post-code "00-517"`
   - **By GPS coordinates** (closest lockers with distance in meters):
     `python3 scripts/inpost.py near 52.2297 21.0122 --limit 5`

3. **Presenting the locker to the user:**
   - Give the locker code (`name`), street address, and `locationDescription` (e.g. "Przy wejściu do Rossmanna").
   - Mention whether it is accessible 24/7 (`is24_7`) and if it supports Strefa Łatwego Dostępu (`easyAccessZone`).
   - Provide the `googleMapsUrl` for easy navigation.

## Commands

| Command | Description | Returns |
|---|---|---|
| `track <number>` | Track parcel by 24-digit tracking number | `status`, `statusTitle`, `targetMachine`, `events`, `trackingUrl` |
| `point <name>` | Look up locker details by code (e.g. `WAW322M`) | `name`, `typeDescription`, `address`, `locationDescription`, `openingHours`, `easyAccessZone`, `googleMapsUrl` |
| `search [--city C] [--query Q] [--post-code P]` | Search lockers in a city, street, or postal code | Matching operating lockers list with addresses and location tips |
| `near <lat> <lon> [--limit N] [--max-distance M]` | Find closest lockers to GPS coordinates | Closest lockers sorted by distance in meters (`distanceFormatted`) |
| `statuses` | List all official InPost parcel status codes & descriptions | Full catalog of parcel statuses in Polish |

Field reference: [references/output.md](references/output.md).

## Exit codes

JSON goes to stdout; errors go to stderr as `{"error": "...", "type": "..."}`.

| Code | Meaning | What to do |
|---|---|---|
| `0` | Success | Use the JSON output |
| `2` | Not found | Tracking number or point code does not exist |
| `64` | Bad usage | Invalid tracking number (must be 24 digits) or invalid arguments |
| `69` | Network / InPost API error | Retry once; check internet connection |

## Rules

- Don't invent fake tracking numbers or locations.
- If the user provides a tracking URL (e.g. `https://inpost.pl/sledzenie-przesylek?number=622...`), extract the 24-digit number.
- For locker inquiries, always include the code (`name`) and `locationDescription` (visual cue) to help the user identify the machine easily.
