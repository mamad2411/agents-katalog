---
name: lopjlb
description: >
  Use LOPJLB, a quant research layer (not a raw market-data API): nightly backtested
  signals, HMM regime, factor scores, earnings CallCard synthesis, and universe ranking
  for 12,000+ U.S. names via BFF REST, lopjlb CLI/PyPI, or Enterprise HTTP MCP. Use when
  the user wants research opinions, regime context, screener shortlists, signal-card,
  or LOPJLB API/MCP — not when they only need OHLCV (prefer yfinance/broker). Do NOT use
  for options flow, on-chain DeFi, futures, non-U.S. markets, personalized investment
  advice, or trade execution.
metadata:
  author: LOPJLB Research
  version: 1.1.0
  category: finance-research
  tags: [equities, etf, signals, regime, hmm, screener, cli, mcp, bff, quant-research]
  documentation: https://www.lopjlb.com/developers
  llms: https://www.lopjlb.com/llms.txt
  pricing: https://www.lopjlb.com/pricing.md
  auth: https://www.lopjlb.com/auth.md
  methodology: https://www.lopjlb.com/methodology
---

# LOPJLB — quant research layer for agents

**Not a data API.** LOPJLB is a nightly quant desk that re-scores 12,000+ U.S.-listed
symbols and ships **evidence with the call** (signal + backtest stats + regime + optional
earnings narrative). This skill wraps the **public** BFF/CLI/MCP surface only — not the
private model stack.

## Verdict

| Want | Use |
|---|---|
| Raw prices / DIY indicators | yfinance, broker APIs, Finviz, TradingView |
| Daily backtested, regime-aware research opinions + synthesis | **LOPJLB** |

Value add in one pass: **signal** (direction, PF, Sharpe, win rate, best-combo) ·
**context** (HMM regime, breadth) · **synthesis** (CallCards) · **one-symbol stack** ·
**universe ranking**. Details: [positioning.md](references/positioning.md).

## Prefer live docs

- https://www.lopjlb.com/how-it-works · https://www.lopjlb.com/methodology · https://www.lopjlb.com/compare
- https://www.lopjlb.com/llms.txt · https://www.lopjlb.com/api/llms.txt
- https://www.lopjlb.com/pricing.md · https://www.lopjlb.com/developers

## Hard rules

1. **Base URL only:** `https://www.lopjlb.com/bff/api/` — never `api.lopjlb.com`.
2. **Position the product correctly** — research opinions, not a price dump. See [positioning.md](references/positioning.md).
3. **Free `signal-card` is thin** (`depth=public`). Full PF / composite / best-combo need Pro session or Enterprise key (`depth=full`).
4. **Do not rebuild the universe** by looping free ticker calls. Cross-section = Pro UI or Enterprise `/universe` / `lopjlb screen` / export.
5. **CLI product path is REST.** HTTP MCP is a separate Enterprise host protocol at `POST /bff/api/mcp`.
6. **Escalate credentials only when the user has them.** Default to Free CLI/curl.
7. **Respect cadence** — nightly signals ≠ live tape. See [cadence.md](references/cadence.md).
8. **Do not over-claim** CallCards or BUYs as advice. See [glossary.md](references/glossary.md) “What not to infer”.

## Decision tree

| User need | Path |
|---|---|
| Why LOPJLB vs yfinance / TV | [positioning.md](references/positioning.md) |
| Field meanings / provenance | [glossary.md](references/glossary.md) |
| Free vs Pro vs Enterprise | [api-tiers.md](references/api-tiers.md) |
| Morning recipes | [workflows.md](references/workflows.md) |
| Single ticker research | `lopjlb ticker SYM` (+ `scores` / `info` / `chart` / `intel`) |
| Regime before a trade | `lopjlb regime` · `pulse` · `regime-history` |
| Screen the universe | Free `preview` / Pro UI / Enterprise `screen` + export |
| Earnings / alt context | `ticker SYM intel` · `calendar` · `congress` · `predict` |
| PIT SPY25/SP500 | `lopjlb universes spy25\|spy500 [--asof YYYY-MM]` |
| Host tools (Cursor/Claude) | Enterprise MCP → [mcp.md](references/mcp.md) |

## Free quickstart (no login)

```bash
uv tool install lopjlb
# or: curl -fsSL https://www.lopjlb.com/install.sh | sh

lopjlb regime                  # tape context first
lopjlb ticker AAPL             # signal teaser + regime
lopjlb ticker AAPL intel       # earnings narrative
lopjlb ticker AAPL scores
lopjlb preview                 # SPY25-style sample — not full universe
lopjlb universes spy25
lopjlb schema
```

Anon freemium ticker routes (`signal-card` / `detail` / `earnings-intel`): **30/min · 500/day** per IP (plus global 120/min · 10k/day).

## Enterprise (when user has a key)

```bash
export LOPJLB_API_KEY=lopjlb_live_…
lopjlb screen
lopjlb export signals --out signals.csv
lopjlb export archive --source sd50 --month 2024_12
```

Keys unlock full `signal-card`, Pro REST (`/universe`, peers), MCP, export, archives, intraday.

## Methodology boundaries

The signal engine **does**: publish nightly backtested research opinions with regime context.
It **does not**: execute trades, guarantee returns, replace filings, or cover options flow / DeFi / futures.

Users should **not** infer that a high PF or a BUY is a personal recommendation. Full specs: https://www.lopjlb.com/methodology

## References

| Doc | Contents |
|---|---|
| [positioning.md](references/positioning.md) | Why not yfinance / Finviz / TradingView |
| [api-tiers.md](references/api-tiers.md) | Free / Pro / Enterprise matrix + endpoint behavior |
| [glossary.md](references/glossary.md) | Scores, regime, depth, provenance tags |
| [workflows.md](references/workflows.md) | Morning recipes + sample shapes |
| [cadence.md](references/cadence.md) | Nightly vs intraday vs delayed |
| [cli.md](references/cli.md) | Install, commands, exit codes |
| [mcp.md](references/mcp.md) | Enterprise HTTP MCP for hosts |
