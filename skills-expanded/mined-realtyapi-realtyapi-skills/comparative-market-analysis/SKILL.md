---
name: comparative-market-analysis
description: >-
  Use when the user wants a CMA — an estimated value range for a property backed by
  comparable sales and local market trends. Combines the subject property's details,
  recent comparable/sold homes, the portal valuation, and area market data into a
  defensible value range with reasoning. Triggers on "run a CMA", "what should this
  list/sell for", "estimate the value of …", "what are the comps for …", "price this
  home".
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
      - cma
      - valuation
      - comps
      - market-data
      - realtyapi
---

# Comparative Market Analysis (CMA)

## Overview

Estimate what a property is worth by triangulating three sources: **comparable
sales**, the **portal valuation/estimate**, and **local market trends**. Produce a
value range with explicit reasoning — not a single magic number.

Use [`realtyapi-api`](../realtyapi-api/SKILL.md) for auth and endpoint discovery.
This skill builds on `property-research` (subject details) and adds rigor on comps.

## When to Use

- "What should I list this house for?"
- "Run a CMA on 123 Main St."
- "What are the comps and what's it worth?"
- Pre-listing pricing, offer strategy, or a sanity check on an asking price.

## Workflow

1. **Subject property** — fetch full details by address/URL (beds, baths, size, lot,
   year, condition signals). This anchors the comparison.
2. **Comparables** — pull comps/similar/nearby **sold** homes. Filter to genuinely
   comparable ones: similar size (±~15–20%), type, and recent sales (ideally last
   3–6 months) in the same area. Drop outliers and explain why.
3. **Portal valuation** — pull the estimate/valuation (`zestimate*`, `estimates`).
4. **Market trend** — pull area market data (`housing_market`, `market*`,
   `housingMarketTrends`): direction and $/sqft trend.
5. **Derive the range** — base it on comp $/sqft applied to the subject's size,
   cross-checked against the portal estimate, then nudge for trend and condition.
   Present a **low–high range** and a most-likely figure.
6. **Show your work** in the report.

## Output Format

```markdown
# CMA: {address}

Subject: {beds}bd/{baths}ba · {size} sqft · {type} · built {year} · {source/link}

## Estimated Value
**{low} – {high}**  (most likely: {point})
- Basis: comp median $/sqft {x} × {size} sqft, adjusted for {trend/condition}
- Portal estimate (cross-check): {value} ({source})

## Comparable Sales
| Address | Sold | Price | Beds/Baths | Size | $/sqft | Dist | Adj. notes |
|---------|------|------:|-----------|-----:|-------:|-----:|-----------|

## Market Context
- Trend: {rising/flat/falling} · Median $/sqft: {} · Days on market: {}

## Confidence & Caveats
- Confidence: {high/med/low} — {# of comps, recency, dispersion}
- Not an appraisal; based on public data and model estimates.
```

## Common Pitfalls

- Reject bad comps (wrong size/type, stale sales, different sub-market) — quality
  over quantity. State how many comps survived.
- Don't blindly trust the portal estimate; use it as a cross-check, not the answer.
- Always give a **range**; flag low confidence when comps are thin or scattered.
- Use **sold** prices for comps, not active list prices, where possible.
- This is a CMA, not a licensed appraisal — say so.
