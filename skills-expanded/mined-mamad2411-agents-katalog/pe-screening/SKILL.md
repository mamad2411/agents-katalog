---
name: pe-screening
description: Screen for investment ideas — factor screens over public names plus private-market signals from the vault (IPO pipeline, sponsor ownership). Use when the user wants a watchlist, "find me companies that...", or idea generation.
---

# Idea Screening

Generate a ranked watchlist from explicit, user-confirmed criteria.

## Data access

- Alpha Vantage / Polygon apps (`apps_execute_tool`) for public-name
  fundamentals and prices. These APIs are per-symbol, not bulk screeners:
  build the candidate universe FIRST, then pull data per name — keep
  universes to ~15-25 candidates so the pull stays reasonable.
- Vault (`analyst_vault_query`) for universe building and private-market
  signals: sector cohorts, recent IPOs, sponsor-owned names (overhang or
  supply signals), acquisitive companies.
- Candidate universes can also come from the user (an index, a sector list,
  their existing watchlist).

## Workflow

1. **Pin the screen.** Restate criteria in one line (e.g. "mid-caps,
   revenue growth accelerating, margins expanding"). Confirm the universe
   source before pulling.
2. **Build the universe** (vault cohort, user list, or sector names), cap
   ~25.
3. **Pull metrics per name** and score against the criteria. Show the
   scoring basis.
4. **Deliver**: ranked table (name, ticker, the screen metrics, one-line
   why), the 3 best fits expanded to a short paragraph each, and the names
   that ALMOST made it with the disqualifying metric.
5. **Offer**: tearsheets on the top names (pe-company-tearsheet), CSV
   export, or a spreadsheet.

## Rules

- A screen is only as honest as its misses: always show the disqualified
  names count.
- Data vintages labeled; per-symbol APIs mean point-in-time pulls, not a
  survivorship-free backtest — say so if the user implies backtesting.
- Research support, not advice.
