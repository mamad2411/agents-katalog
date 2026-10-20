---
name: finance-intelligence-agent
description: "Build and operate automated financial intelligence pipelines — SEC EDGAR scanning, CIA World Factbook economic snapshots, patent expiration monitoring, watchlist management, options portfolio management, risk-based position sizing, and metrics tracking. Integrates with Yahoo Finance for live quotes and options chains."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [windows]
metadata:
  hermes:
    tags: [finance, trading, options, sec, edgar, watchlist, portfolio, metrics, position-sizing]
    triggers: [finance-agent, options-trading, sec-edgar, watchlist, position-size, financial-intelligence, portfolio-management, volatility]
---

# Finance Intelligence Agent

Build automated financial intelligence pipelines that aggregate, analyze, and act on free public data sources — from SEC filings to options chains.

## Architecture

```
the planning repo/02-executive-council/finance-agent/
├── soul.md                     # Agent identity and mission
├── agent.md                    # Responsibilities, data sources, pipeline tiers
├── skill.md                    # Reusable workflows (SEC, CIA, patents, etc.)
├── tools.md                    # Complete repo inventory with local paths
├── memory.md                   # Persistent context and cron schedules
├── options/
│   └── portfolio.json          # Multi-portfolio config (allocation, risk, strategies)
├── options.py                  # CLI: portfolio management, scanning, position sizing
├── watchlist.json              # 35+ tickers across 6 named watchlists
├── watchlist_manager.py        # CLI: watchlist CRUD, strategy toggles, SEC targets
├── metrics.py                  # Pipeline performance tracking and reporting
└── metrics/
    ├── history.jsonl           # Append-only event log
    └── summary.json            # Aggregated stats
```

## Setup

### Dependencies
```bash
pip install sec-edgar-downloader numpy-financial
```

### Repo locations
- Agent framework: `the planning repo/02-executive-council/finance-agent/`
- Cloned FOSS tools: `${MY_REPOS}/` (sec-edgar-downloader, factbook-json, cdp-backend, numpy-financial, patents-public-data, Koha)
- SEC filings cache: `${MY_REPOS}/Documents/research/sec_filings/`
- Economic snapshots: `${MY_REPOS}/Documents/research/`

## Data Sources

| Resource | Tool | Data Type | FOSS Equivalent |
|----------|------|-----------|----------------|
| SEC EDGAR | sec-edgar-downloader | 10-K, 10-Q, 8-K, UPLOAD, CORRESP, Form 4 | Open-source Python package |
| CIA World Factbook | factbook.json | Economic, gov, infrastructure data (266 countries) | Structured JSON |
| Patent Data | Google Patents Public Data | IP expiration schedules | BigQuery public datasets |
| Zoning Minutes | Council Data Project | Municipal development plans | Open-source CDP backend |
| Bloomberg Terminal | Public library access / OpenBB | Real-time financial data | OpenBB Terminal (FOSS) |
| Options Chains | Yahoo Finance API | Option quotes, IV, OI | Free REST API |
| Stock Quotes | Yahoo Finance API | Price, volume, change | Free REST API |

## Key Commands

### Watchlist Management
```bash
cd <finance-agent-dir>
python watchlist_manager.py list              # Full watchlist view
python watchlist_manager.py sec-targets       # Get tickers for SEC EDGAR scan
python watchlist_manager.py top               # Priority 1-2 tickers
python watchlist_manager.py add <wl> <TICKER> # Add ticker to watchlist
python watchlist_manager.py remove <wl> <TICKER> # Remove ticker
python watchlist_manager.py enable <strategy> # Enable a strategy
```

### Options Portfolio
```bash
python options.py list                        # All portfolios with $ allocations
python options.py show <portfolio>            # Strategy rules, exit rules, watchlist
python options.py scan                        # Live price/volume scan of 26+ tickers
python options.py allocate                    # Allocation breakdown table
python options.py size <portfolio> <entry> <stop> [capital]  # Position sizing
python options.py add <TICKER> <type> [priority]  # Add to core watchlist
```

### Metrics
```bash
python metrics.py report                      # Full performance over last 7 days
python metrics.py report --days=30            # Last 30 days
python metrics.py trend <metric_name> [days]  # Trend for a metric
python metrics.py summary                     # One-liner for cron delivery
python metrics.py log <pipeline> <status> [count] [details]  # Log execution
python metrics.py signal <pipeline> <tier> [count] [desc]    # Log signal
```

### Live Scanning
```bash
python options.py scan                        # Quick scan all watchlist tickers
python options.py scan --high-vol             # High-volatility screener
```

## Portfolio Structure (Example — $100K model)

| Portfolio | Strategy | Allocation | Tickers |
|-----------|----------|-----------|---------|
| Volatility Alpha | vol_event (0-7 DTE) | 20% | VXX, UVXY, SVXY |
| Momentum Swing | momentum (7-30 DTE) | 30% | LAMR, NVDA, META, PLTR |
| Income Generator | theta_income (30-60 DTE) | 25% | LEN, DHI, PHM, SOUN |
| Earnings Events | earnings_binary (0-3 DTE) | 10% | AAPL, NVDA, META |
| Macro Hedge | tail_hedge (30-90 DTE) | 5% | VXX, SPY, QQQ |
| Freelance Hedge | sector_directional (14-45 DTE) | 5% | FVRR, UPWK, TTD |

**Adjust all allocations, risk %, and strategy rules in** `options/portfolio.json`.

## Watchlists

35+ unique tickers across 6 named watchlists:
- **Core Portfolio** (priority 1) — AAPL, MSFT, GOOGL, AMZN, NVDA, META
- **AI/ML Ecosystem** (priority 2) — PLTR, CRM, SNOW, SOUN, BBAI
- **Land & Real Estate** (priority 2) — LEN, DHI, PHM, NVR, TOL, OPEN, Z
- **MES/GovCon/Defense** (priority 3) — RTX, BA, LMT, GD, SAIC, LDOS, CACI
- **Patent Intelligence** (priority 3) — MRK, PFE, ABBV, AMGN, IBM
- **Freelance Economy** (priority 4) — FVRR, UPWK, TTD

## Position Sizing

Three methods configured in `options/portfolio.json`:
1. **Fixed Risk** — position = (capital × risk_pct) / (entry - stop)
2. **Kelly Criterion** — optimal size from win rate and avg win/loss (capped at 25% Kelly fraction)
3. **Percent Risk** — fixed % of portfolio allocation per position

Default method: `percent_risk`. Switch per-portfolio in the JSON config.

## Cron Jobs

| Job | Schedule | Purpose |
|-----|----------|---------|
| SEC EDGAR Scan | Mon 6am | Scan filings for all sec-targets tickers |
| Economic Snapshot | Mon 7am | CIA Factbook macroeconomic brief |
| Metrics Report | Mon 8am | Weekly performance review |

All crons are in the cronjob list and update the metrics history automatically.

## Pitfalls

- **Yahoo Finance rate limits:** The free API has no formal limit but successive rapid calls may get rate-limited. Add a 0.5s delay between tickers in scanning loops.
- **SEC EDGAR rate limits:** sec-edgar-downloader respects the SEC's 10 requests/second limit automatically, but bulk scanning 30+ tickers takes several minutes.
- **Watchlist manager path resolution:** The write_file tool may write to `C:\e\...` instead of `E:\...` due to path resolution differences between MSYS and Python. Always verify the actual file location and copy to the git-tracked E: drive if needed.
- **MSYS path mangling:** When running `gh api` commands from git-bash, MSYS rewrites leading `/` in API endpoint paths as Windows filesystem paths. Use curl with `$(gh auth token)` instead (see `github-stars-extraction` skill).
- **Options chain parsing:** Yahoo Finance v7 API returns options data keyed by expiration — the response contains multiple expiration dates. Parse the `optionChain.result[0].options` array which contains one entry per expiration date with separate calls/puts arrays.
- **Metrics start empty:** `metrics/history.jsonl` is append-only. First runs after creation will show "No data" in reports until at least one pipeline executes.
