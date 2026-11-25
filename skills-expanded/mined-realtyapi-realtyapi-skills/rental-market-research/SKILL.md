---
name: rental-market-research
description: >-
  Use when the user wants to research rentals — long-term apartments/homes or
  short-term/vacation stays — in an area, and understand rent levels and trends.
  Searches the right rental portals (Apartments.com, HotPads, Zillow rentals,
  Flatmates, regional portals; Airbnb/Vrbo for short-term), pulls rent/market
  trends, and returns options plus a rent summary. Triggers on "find rentals in …",
  "what's rent for a 2-bed in …", "Airbnb options near …", "is rent rising in …".
allowed-tools: Bash, Read, Write, WebFetch
version: 1.0.0
homepage: https://www.realtyapi.io
repository: https://github.com/realtyapi/realtyapi-skills
license: MIT
metadata:
  openclaw:
    requires:
      env:
        - REALTYAPI_API_KEY
    primaryEnv: REALTYAPI_API_KEY
    homepage: https://www.realtyapi.io
    tags:
      - real-estate
      - rentals
      - short-term-rentals
      - market-data
      - realtyapi
---

# Rental Market Research

## Overview

Help the user understand the rental picture for an area: available units that match
their needs **and** what rent looks like (typical levels and trend). Works for
long-term rentals and short-term/vacation stays.

Use [`realtyapi-api`](../realtyapi-api/SKILL.md) for auth and endpoint discovery.

## When to Use

- "Find 2-bed rentals under $2,500 in Denver."
- "What does a furnished short-term stay cost near this address?"
- "Is rent going up in this zip?"
- Relocation, investment rent estimates, or budgeting.

## Workflow

1. **Long-term vs. short-term?** Long-term → `apartments`, `hotpads`, `zillow`
   rentals, `flatmates` (shared, AU), or the regional portal. Short-term/vacation →
   `airbnb`, `vrbo`, `agoda`, `trip`.
2. **Resolve the area** with `autocomplete` / `locations`.
3. **Search rentals** with the rent **status filter** set, plus beds/baths/price.
   Read the endpoint `openapi.json` for the exact params; paginate as needed (cap it).
4. **Rent trends** — pull rental-market analytics where available
   (`rental_market*`, `market*`, regional trend endpoints) for typical rent and
   direction.
5. **Synthesize**: options table + a short rent summary (median-ish level, range,
   trend). Distinguish observed listing rents from any modeled estimate.

## Output Format

```markdown
# Rental Research: {criteria} in {area}

Type: {long-term / short-term} · Portal(s): {} · {N} options

## Rent Summary
- Typical rent for {beds}-bed: {level / range}
- Trend: {rising / flat / falling} ({source})

## Options
| # | Address/Listing | Rent | Beds/Baths | Size | Available | Link |
|--:|-----------------|-----:|-----------|-----:|-----------|------|

## Notes
- Sorted by: {criterion} · Pages/credits used: {}
- Caveats: listing rents ≠ signed-lease rents; sample size {}
```

## Common Pitfalls

- Set the **rent** status — don't return for-sale homes by accident.
- Short-term nightly rates aren't comparable to monthly long-term rent; label units.
- A small number of listings is a weak trend signal — say so.
- Respect credits across search pages and trend calls.
