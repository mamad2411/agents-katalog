---
name: pe-company-tearsheet
description: One-page company tearsheet — profile, price and valuation, fundamentals trend, ownership and pre-IPO history, recent developments. Use when the user asks for a tearsheet, company snapshot, or "get me up to speed on <ticker>".
---

# Company Tearsheet

Produce a one-page snapshot a PM can read in two minutes.

## Data access

- **Market data and fundamentals**: the Alpha Vantage app via
  `apps_execute_tool` (app=alpha_vantage) — quote, market cap, valuation
  ratios, revenue and earnings history. Polygon (app=polygon), when
  connected, for finer price history.
- **Private-market context**: `analyst_vault_query` over the Caeros vault
  (PitchBook in BigQuery) — pre-IPO funding history, notable investors,
  M&A the company has done.
- If Alpha Vantage isn't connected, pause and ask the user to connect it
  from the plugin page; deliver only the vault sections in the meantime.

## Sections (in order)

1. **Header**: name, ticker, exchange, sector, market cap, price and 52-week
   range.
2. **What they do**: 2-3 sentences, plain language.
3. **Valuation now**: P/E, EV/Revenue or EV/EBITDA as available, vs the
   figure's period. One line vs history ("high end of its 3-year range")
   only when the data supports it.
4. **Fundamentals trend**: revenue and margin direction over the last 4-8
   quarters; one line on the driver.
5. **Ownership and history** (vault): pre-IPO backers still relevant,
   acquisitions made, anything structurally notable.
6. **Recent developments**: latest earnings date and headline result; use
   the X plugin or news search when connected for market reaction.
7. **Watch items**: 2-3 bullets a PM would actually track.

## Rules

- Every number is sourced (app, vault, or user); no memory-based figures —
  models are stale on prices by construction.
- Label data vintages (quote timestamp, quarter ends).
- This is research support, not investment advice; keep judgments about
  what to buy or sell out of it.
