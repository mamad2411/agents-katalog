---
name: fundamentals-pit
description: >
  Pull point-in-time quarterly fundamentals for a US equity — a row is visible only
  if its filing date is on or before the as-of date, so backtests never see numbers
  that had not been filed yet. Returns TTM profitability and capital-return ratios,
  leverage, long-window ERM3 valuation betas, a CAPM cost-of-capital layer, an
  equity-bridge
  decomposition, and SEC-sourced raw line items per cell. Use for PIT fundamentals,
  as-of history, and anti-look-ahead research.
argument-hint: "[ticker] [as_of?]"
---

# Point-in-time quarterly fundamentals

PIT-normalized fundamentals derived from SEC filings and licensed sources. The
differentiator is the **`as_of` discipline**: rows are returned only where
`filed_date <= as_of`, so a query dated in the past reflects exactly what had been
filed by then — no silent restatement, no look-ahead. This skill wraps the hosted
RiskModels MCP; it reports tool outputs and computes nothing itself.

## What to call

Resolve a company name to a ticker first (`riskmodels_search`), then:

- **`riskmodels_get_fundamentals`** — the one tool. Params: `ticker`, `as_of`
  (PIT date, default today), `periods` (quarterly rows, most recent last). Set
  `grid=true` for the cost-of-capital sensitivity table (see the `cost-of-capital`
  skill).

## Reading the response

Each row carries:

- **Ratios** — TTM `roe_ttm`, `roa_ttm`, `fcf_margin`, `leverage_ratio`, and the
  capital-return set (`payout_ratio`, `retention_ratio`, `buyback_ratio`,
  `total_payout_ratio`, `sustainable_growth`). Ratios are null unless four finite
  trailing quarters exist — report null as "not enough history," never as zero.
- **`sec_facts`** — raw line items **only for the cells whose serving value is SEC
  XBRL**, each as `{value, source}` with `source` ∈ {`us_gaap`, `ifrs`}. A concept
  is absent for a period when that cell is not SEC-sourced. Do not describe the panel
  as "raw fundamentals" — raw values are present per-cell where SEC-sourced and not
  elsewhere. Values are as-originally-reported (earliest filing).
- **`equity_bridge_residual` + `equity_bridge_inputs`** — a disclosed decomposition
  of the quarter-over-quarter change in equity. The residual is a **plug** that makes
  the roll-forward an identity by construction; it is frequently large. Report it as
  a decomposition, not truth. For modelling, anchor on `retained_earnings`.
- **Valuation betas** — `beta_market` / `beta_sector` / `beta_subsector` with
  `beta_source`. These are the long-window monthly, Vasicek-shrunk betas used by
  the cost-of-capital layer, distinct from the short-half-life hedging surface.

## Boundary

Realized/historical data only — no forecasts, targets, or recommendations. You are
an analyst, not an investment adviser. Always call the tool before quoting a figure.

## Example prompts

- `/fundamentals-pit AAPL`
- `/fundamentals-pit XOM 2021-06-30` — "what did Exxon's fundamentals look like as of
  mid-2021, using only what had been filed by then?"
- "Show NVDA's last 8 quarters of ROE and FCF margin, point-in-time."
- "Which of MSFT's recent line items are SEC-sourced vs vendor-sourced?"
