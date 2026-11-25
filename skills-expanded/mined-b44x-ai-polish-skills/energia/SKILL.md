---
name: energia
display_name: Energia — ceny RCE z PSE
version: 1.0.0
description: >-
  Read official Polish PSE market electricity prices (RCE), find the cheapest continuous consumption window and summarize historical prices. Use for "ceny RCE", "ceny energii PSE", "najtańsze godziny prądu" or "kiedy ładować przy cenach rynkowych". Reports complete and missing intervals; retail tariffs depend on the user's contract.
category: finance
language: pl
country: PL
license: MIT
author: Michell Hoduń (https://github.com/b44x)
repository: https://github.com/b44x/ai-polish-skills
network: true
authentication: none
source: Polskie Sieci Elektroenergetyczne (PSE)
source_type: official_api
official: true
homepage: https://www.pse.pl/
documentation: https://api.raporty.pse.pl/
rate_limit: fair use; local cache 5 minutes; maximum 31 days per query
last_verified: 2026-11-05
tags:
  - energia
  - rce
  - pse
  - prad
  - ceny-energii
  - ladowanie
compatibility: Python 3.8+ (standard library only); internet access required.
---

# PSE market electricity prices

## Running the script

Run `python3 scripts/energia.py <command> ...` from this skill's directory (`py` on Windows). No API key or pip packages are required.

| Command | Result |
|---|---|
| `day 2026-11-04` | Interval prices, minimum, maximum, mean of available data and daily completeness |
| `cheapest 2026-11-04 --minutes 120` | Cheapest continuous two hours in a complete day, starting at a PSE interval boundary |
| `cheapest 2026-11-04 --minutes 180 --kwh 12` | Also compute the RCE component for 12 kWh consumed at constant power over three hours |
| `summary --from 2026-11-01 --to 2026-11-04` | Summary of up to 31 days, missing dates and completeness of each day |

Without a date, `day` and `cheapest` use today's date in Poland. Every command accepts `--no-cache` and `--cache-dir <directory>`. Cache entries are valid for 5 minutes; a refresh failure ends the lookup with an error.

## Interpreting results

- Cite **PSE**, the date, prices in PLN/MWh or PLN/kWh and publication time. 1000 PLN/MWh = 1 PLN/kWh. These are market RCE prices; the bill depends on the user's contract and includes additional components. Negative RCE does not guarantee a negative bill. Do not assume a VAT rate or promise savings under a particular retail tariff.
- Use the date requested by the user; tomorrow's data may not be published yet. Missing data produces `not_found`, not a forecast or a zero price.
- `complete: false` means incomplete coverage. `mean_available_pln_mwh` covers only published intervals; `mean_full_period_pln_mwh` in the summary then remains `null`. `cheapest` requires a complete day to compare all candidate windows.
- Each interval has UTC boundaries and local ISO boundaries with UTC offsets. Use these for daylight-saving transitions: a day can have 23, 24 or 25 hours, and a local hour can repeat.
- `--minutes` specifies elapsed duration, not the difference between wall-clock readings. The final interval can be used partially, weighted by time, allowing a 90-minute window even with historical hourly prices. `--kwh` assumes constant consumption power. `rce_component_pln` is only the RCE component. The skill does not control chargers or other devices.

## Output and exit codes

Success: JSON on stdout, exit `0`. Errors: JSON on stderr, exit `2` for missing data/window, `64` for validation or `69` for API/network failures or an incomplete day when selecting a window. `--help` and `-h` return `0`.

Read [references/api.md](references/api.md) for field definitions and sources.
