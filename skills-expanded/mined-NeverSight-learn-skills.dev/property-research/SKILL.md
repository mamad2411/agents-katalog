---
name: property-research
description: >-
  Use when the user wants a complete profile of a single property — by street
  address or a portal listing URL. Pulls full details, price/tax history,
  valuation/estimate, comparables, and neighborhood context (schools, climate,
  walkability) and turns them into a property brief. Triggers on "tell me about
  this house", "look up this address", "is this listing a good deal", "what's
  this property worth", "pull the details for this Zillow/Redfin/Rightmove link".
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
      - property
      - due-diligence
      - realtyapi
---

# Property Research

## Overview

Produce a single, well-sourced brief on **one property**: what it is, its history,
what it's likely worth, how it compares to nearby homes, and the neighborhood
context — so the user can judge it quickly.

Use the [`realtyapi-api`](../realtyapi-api/SKILL.md) skill as the data layer: it
explains auth, endpoint discovery via `llms.txt`, and per-provider `openapi.json`.

## When to Use

- "Tell me everything about 123 Main St."
- "Here's a Zillow/Redfin/Rightmove link — is it a good buy?"
- "What's this property worth and how does it compare to others nearby?"
- Pre-offer or pre-showing due diligence on a specific home.

## Workflow

1. **Pick the portal** from the address's country/market (see the catalog in
   `realtyapi-api`). If the user pasted a listing URL, use that portal and its
   URL-based endpoint.
2. **Resolve & fetch core details** — call the property-details endpoint by address
   or URL (`…byaddress` / `…byurl` / `detailsbyaddress`). Use `autocomplete` first
   if the endpoint needs an internal id.
3. **History** — pull price history and tax history (`pricehistory`, `taxinfo*`,
   `sold-prices`) if available.
4. **Valuation** — pull the estimate/valuation (`zestimate*`, `estimates`).
5. **Comparables** — pull comps/similar/nearby homes for context.
6. **Neighborhood** (optional, if relevant) — schools, climate, walk/transit/bike.
7. **Synthesize** into the brief below. Flag any field a portal didn't return rather
   than inventing it.

## Output Format

```markdown
# Property Brief: {address}

**Source:** {portal} — {listing URL}  ·  Status: {for sale / sold / off-market}

## Snapshot
- Price / last list: {} · Beds/Baths: {} · Size: {} · Lot: {} · Year built: {} · Type: {}

## Estimated Value
- Estimate: {value or range} ({source})
- vs. list price: {over / under / in line}

## History
| Date | Event | Price |
|------|-------|------:|

## Comparables
| Address | Price | Beds/Baths | Size | $/sqft | Distance |
|---------|------:|-----------|-----:|-------:|---------:|

## Neighborhood (if pulled)
- Schools: {} · Walk/Transit: {} · Climate/risk: {}

## Assessment
- Priced {fairly/high/low} vs. estimate and comps because …
- Watch-outs: …
- Missing data: {fields no portal returned}
```

## Common Pitfalls

- Don't present an estimate as an appraisal — it's a model output; show the range.
- Don't compare a US address against a non-US portal; match portal to market.
- Keep comps truly comparable (similar size/type/recency); note when they aren't.
- Warn before endpoints that cost more than 1 credit, and don't silently loop comps.
