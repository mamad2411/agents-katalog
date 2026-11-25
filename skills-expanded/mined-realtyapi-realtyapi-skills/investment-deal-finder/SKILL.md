---
name: investment-deal-finder
description: >-
  Use when the user wants to find and screen real estate investment opportunities —
  foreclosures/auctions, below-market or price-reduced listings, and rental-yield
  candidates. Searches auction and listing portals, pulls rent/valuation context,
  estimates a rough yield/margin, and returns ranked deal candidates with reasoning.
  Triggers on "find investment properties", "foreclosures/auctions in …", "high cash
  flow rentals", "undervalued homes", "what's a good rental deal in …".
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
      - investing
      - foreclosure
      - auction
      - rental-yield
      - realtyapi
---

# Investment Deal Finder

## Overview

Surface and screen investment candidates against a simple, transparent rubric:
acquisition price vs. estimated value (equity/margin) and, for rentals, rent vs.
price (gross yield). Return a ranked shortlist with the math shown.

Use [`realtyapi-api`](../realtyapi-api/SKILL.md) for auth and endpoint discovery.

## When to Use

- "Find foreclosure/auction deals in {county}."
- "Show price-reduced or below-market homes in {area}."
- "Which rentals here cash-flow best?"
- Building an investor's lead list for buy-and-hold or flips.

## Workflow

1. **Strategy?** Distressed/auction (→ `auction`), discounted resale (→ listing
   portals with price-reduced/sold filters), or rental-yield (→ listing + rental
   portals). Confirm the target market and budget.
2. **Source candidates** — search the relevant portal(s) with filters (price ceiling,
   type, status, "price reduced" where supported). Paginate within a cap.
3. **Add value context** — for each promising candidate, pull the valuation/estimate
   and (for rentals) typical rent (`rental_market*` or comparable rentals).
4. **Screen with the rubric:**
   - **Equity/margin** = (estimated value − price) / estimated value.
   - **Gross yield** = annual rent / price (rentals).
   - Note obvious risks (auction = as-is, unknown condition/liens; thin comps).
5. **Rank** by the user's objective (margin, yield, or a blend) and present.

## Output Format

```markdown
# Investment Candidates: {strategy} in {area}

Budget: {} · Portal(s): {} · Screened {N} of {M} found

| # | Address | Price | Est. value | Equity % | Est. rent | Gross yield | Risk | Link |
|--:|---------|------:|-----------:|--------:|----------:|------------:|------|------|

## Top Picks
1. {address} — why it scores: {margin/yield}, watch-outs: {}
2. …

## Method & Caveats
- Equity % = (est. value − price)/est. value · Gross yield = annual rent/price
- Estimates are model-based; auction props are as-is — verify condition, liens, fees.
- Not investment advice; do full due diligence before offering.
```

## Common Pitfalls

- Don't present model estimates as guaranteed value; distressed comps are noisy.
- Auction/foreclosure = as-is — always flag unknown condition, liens, and buyer fees.
- Yield from listing rents is a rough gross figure (excludes vacancy, taxes, mgmt).
- Respect credits — screening adds valuation/rent calls per candidate; cap the set
  and tell the user the count.
- Make clear this is research, not financial advice.
