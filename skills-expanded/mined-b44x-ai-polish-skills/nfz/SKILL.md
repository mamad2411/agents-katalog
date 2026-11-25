---
name: nfz
display_name: NFZ Kolejki i Czas Oczekiwania (PCUŚ)
version: 1.0.0
description: >-
  Official data from the Narodowy Fundusz Zdrowia (NFZ, Polish National Health Fund) on queues,
  medical facilities and estimated waiting times for healthcare services (PCUŚ). Search medical
  services (MRI, CT, colonoscopy, gastroscopy, cardiology clinic, orthopedist, ophthalmologist),
  check the estimated waiting time (in days and months) and the number of waiting patients for
  stable and urgent cases. Find the nearest facilities within a given radius in kilometers
  (Haversine) and compare waiting times across hospitals and clinics. No API keys, 100% official
  public data from the NFZ Terminy Leczenia API. Use whenever the user asks about: "kolejki NFZ",
  "czas oczekiwania do kardiologa", "gdzie na rezonans na NFZ", "terminy leczenia",
  "poradnia NFZ w Gdańsku", "najkrótsza kolejka do endokrynologa", "NFZ czas oczekiwania".
category: health
language: pl
country: PL
license: MIT
author: Michell Hoduń (https://github.com/b44x)
repository: https://github.com/b44x/ai-polish-skills
network: true
authentication: none
source: Narodowy Fundusz Zdrowia (NFZ)
source_type: official_api
official: true
homepage: https://terminyleczenia.nfz.gov.pl/
documentation: https://apinfz.nfz.gov.pl/app-itl-api-pcus/
rate_limit: fair use
last_verified: 2026-09-28
tags:
  - nfz
  - zdrowie
  - kolejki
  - pcus
  - lekarz
  - przychodnia
  - szpital
  - rezonans
  - tomografia
  - kardiolog
  - stomatolog
  - terminy
compatibility: Python 3.8+ (standard library only); network access to apinfz.nfz.gov.pl.
---

# NFZ Queues and Waiting Times (PCUŚ)

Official skill integrating open data from the Narodowy Fundusz Zdrowia (NFZ) Terminy Leczenia / PCUŚ v1.4 API
via the `scripts/nfz.py` tool. Works without registration and without API keys, uses only the Python standard
library, and returns structured JSON on `stdout`.

> **Important:** PCUŚ (*Prognozowany Czas Oczekiwania na Świadczenie*, estimated waiting time for a service)
> is a statistical estimate calculated by NFZ — it is **not** the date of the first free appointment.

## Running the script

Run from the skill directory (or from the repository root path):

| Operating system | Command |
|---|---|
| Linux / macOS | `python3 scripts/nfz.py <command> …` |
| Windows | `py scripts/nfz.py <command> …` (or `python`) |

Zero external libraries (Python 3.8+ stdlib).

## Workflow

1. **Looking up the official service name:**
   - When the user asks generally about a test or specialty (e.g. „rezonans”, „kardiolog”, „kolonoskopia”):
     `python3 scripts/nfz.py benefits rezonans`
     `python3 scripts/nfz.py benefits kardiolog`
     `python3 scripts/nfz.py benefits kolonoskopia`
   - Returns a list of official NFZ service names that can be passed to subsequent queries.

2. **Queues and waiting times in a given city / voivodeship (województwo):**
   - Checking the waiting time for a service in a specific city:
     `python3 scripts/nfz.py queues --benefit "REZONANS MAGNETYCZNY" --locality Gdańsk`
     `python3 scripts/nfz.py queues --benefit "ŚWIADCZENIA Z ZAKRESU KARDIOLOGII" --locality Warszawa`
   - Filtering for an urgent case (urgent / "cito" referral):
     `python3 scripts/nfz.py queues --benefit "REZONANS MAGNETYCZNY" --locality Gdańsk --urgent`

3. **Geographic search for facilities within a radius in kilometers (`near`):**
   - Finding facilities providing a given service within a radius of a given city or coordinates:
     `python3 scripts/nfz.py near Gdańsk --benefit "rezonans" --radius-km 50`
     `python3 scripts/nfz.py near 54.35 18.64 --benefit "kolonoskopia" --radius-km 30`
   - Sorting by shortest waiting time (`--sort time`) or smallest distance (`--sort distance`).

4. **Comparing facilities and shortest queues (`compare`):**
   - Side-by-side comparison of facilities, highlighting the facility with the shortest waiting time:
     `python3 scripts/nfz.py compare --benefit "rezonans" --locality Gdańsk`
     `python3 scripts/nfz.py compare --benefit "kardiolog" --province pomorskie`

5. **List of NFZ voivodeship codes (`provinces`):**
   - Overview of the 16 NFZ codes (e.g. `11` for pomorskie, `07` for mazowieckie):
     `python3 scripts/nfz.py provinces`

## Commands

| Command | Description | Returned data |
|---|---|---|
| `benefits <query>` | Dictionary of official service names | `query`, `count`, `benefits` |
| `queues [--benefit B] [--province P] [--locality L] [--urgent]` | Waiting times and list of facilities | `place`, `provider`, `locality`, `address`, `phone`, `waitingTime` (`pcus`, `averagePeriodDays`, `awaiting`), `accessibility` |
| `near <location\|lat> [lon] --benefit <B> [--radius-km R]` | Facilities within a radius in km, with distances | Facility objects with computed `distanceKm`, sorted by the chosen criterion |
| `compare --benefit <B> [--locality L] [--province P]` | Comparative summary of facilities | `highlights` (`shortestWaitClinic`, `fewestAwaitingClinic`, `closestClinic`), list of facilities |
| `provinces` | Dictionary of the 16 voivodeships and NFZ codes | Two-digit codes and voivodeship names (offline) |

Detailed description of JSON schemas: [references/output.md](references/output.md).

## Exit codes

Clean JSON goes to `stdout`; errors go to `stderr` as `{"error": "...", "type": "..."}`.

| Code | Meaning | Action |
|---|---|---|
| `0` | Success | Use the JSON data from `stdout` |
| `2` | Not found | No facilities or no such service in the NFZ register |
| `64` | Invalid invocation / validation | Check the parameters (min. 3-character phrase, valid voivodeship code) |
| `69` | NFZ server / network error | `apinfz.nfz.gov.pl` API error or network problem |

## Rules

- **Always cite the data source:** Narodowy Fundusz Zdrowia (NFZ / Terminy Leczenia).
- **Distinguish PCUŚ from an appointment date:** NFZ data presents the *Prognozowany Czas Oczekiwania na Świadczenie* (a statistical time calculated by NFZ based on recent months), not a guaranteed first free appointment. Explain this to the user.
- **Medical neutrality:** The tool provides administrative queue data. Do not make medical diagnoses or assess the quality of care at a given facility.
- **Recommend a phone call:** Suggest that the user contact the facility's registration desk directly by phone (number given in the `phone` field) before going there in person.
