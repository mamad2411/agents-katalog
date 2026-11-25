---
name: portfolio-hedge
description: >
  Build ETF hedge legs for a single position or a multi-name portfolio from the
  ERM3 cascade — scale the market / sector / subsector hedge ratios to dollar
  notionals and aggregate the ETF legs, or dispatch the Lstar level that isolates a
  position's residual return. Use when asked what would neutralize a book's market
  or sector exposure, or how to isolate idiosyncratic return.
argument-hint: "[ticker or positions: TICKER:WEIGHT ...]"
---

# Portfolio & position hedging (ERM3 cascade + Lstar)

Report the ETF hedge legs the decomposition implies for a position or portfolio. This
skill wraps the hosted RiskModels MCP and reports tool outputs; it computes nothing
itself.

## What to call

- **`riskmodels_get_my_positions`** — the caller's linked book (Alpaca Connect, Connect
  Trade, or Plaid). Call this first when the user means their account and has not
  pasted tickers. Pass `for_analysis` and `for_hedge` to the long-only portfolio tools
  below; when `has_shorts` is true or the book has more than 100 names, pass
  `for_exposure` to `riskmodels_portfolio_exposure`. This server does not place orders.
- **`riskmodels_decompose`** with `dollars` — one ticker: scale the L-level ETF hedge
  ratios to a dollar position.
- **`riskmodels_analyze_portfolio`** — a long-only book: holdings-weighted L1/L2/L3
  hedge-level aggregate; with dollar positions it also scales the hedge ratios at the
  chosen cascade level (`level` L1/L2/L3) into ETF USD hedge legs.
- **`riskmodels_portfolio_exposure`** — a signed long/short book (dollar values,
  short < 0, up to 1000 names): beta-dollars by sector, the ETF trades that neutralise
  the book at L1/L2/L3, and the systematic vs residual risk split. Use it whenever any
  position is short or the book has more than 100 names; `riskmodels_analyze_portfolio`
  takes long positions only (up to 100). Report any
  `coverage.dropped` names or `warnings` to the user.
- **`riskmodels_get_residual_returns`** (1-100 tickers) — dispatch the simplest
  cascade level that clears the marginal-ER threshold for a name (or basket) and
  return the residual-return series after that hedge.

For an ETF or 13F filer named instead of pasted tickers, resolve real holdings first
(`riskmodels_search` → `riskmodels_get_etf` with `holdings_top`, or
`riskmodels_get_filer` with `holdings_top` / `riskmodels_get_fund` with `holdings_limit`) and treat the result as the portfolio. Never
fabricate or approximate holdings — if no tool covers the portfolio, say so and ask
the user to paste the positions.

## How to present

- Name each ETF leg and frame it as what it **would mechanically neutralize**, e.g.
  "$0.62 of SPY per $1 of book neutralizes the market leg." A hedge ratio is a model
  output, like a beta — reporting it is reporting the math.
- Aggregate legs across positions into a single per-ETF USD figure for the book.
- If residual ER is high, note that the leftover is stock-specific and not hedgeable
  with sector/market ETFs.
- Negative hedge ratios are valid (orthogonalization); don't read a negative market
  leg as "short the market" — it often offsets beta embedded in the sector/subsector
  legs.

## Boundary

You are an analyst, not an investment adviser. Report what each hedge leg would
neutralize; never tell the user to place, trim, or rebalance a trade, and never
assess whether the book is suitable for them. No options, swaps, or derivatives —
ETF legs only. Always call the tools before quoting figures.

## Example prompts

- `/portfolio-hedge NVDA:0.4 MSFT:0.35 XOM:0.25`
- "What SPY + sector-ETF legs would neutralize the market and sector risk in this book?"
- "Isolate the residual return on PLTR — what Lstar level does the model dispatch?"
