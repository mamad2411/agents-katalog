---
name: financial-analysis
description: >
  Comprehensive financial analysis skill for stock research, portfolio review, and opportunity discovery.
  Use this skill when the user wants to: analyze stocks, review a portfolio, scan for new stock ideas,
  get buy/sell ratings, compute support/resistance levels, check insider or Congress trades,
  assess sentiment from Reddit/StockTwits/news, pull analyst ratings, or generate entry/exit price targets.
  Triggers: stock analysis, portfolio review, stock scanner, financial analysis, buy/sell rating,
  price target, technical analysis, sentiment analysis, insider trading, Congress trades, stock ideas,
  swing trade, entry levels, exit levels, support resistance, watchlist, deep dive, stock report.
---

# Financial Analysis Skill

A multi-source financial analysis engine that aggregates data from 14+ free APIs and 20+ RSS feeds to produce professional-grade stock analysis with actionable buy/sell ratings and price targets.

## First-Time Setup

Before using this skill, read the API setup guide and configure API keys:

```
Read references/api_setup_guide.md
```

Then initialize the config:
```bash
python scripts/api_config.py init
python scripts/api_config.py status
```

Install Python dependencies:
```bash
pip install yfinance feedparser pandas pandas-ta requests --break-system-packages
```

## Architecture Overview

```
financial-analysis/
├── SKILL.md                          # This file — main instructions
├── scripts/
│   ├── api_config.py                 # API registry, keys, fallback chains
│   ├── usage_tracker.py              # Rate limit enforcement, logging, reports
│   ├── api_caller.py                 # Resilient caller with auto-fallback
│   └── rss_feeds.py                  # RSS feed catalog and parser
└── references/
    └── api_setup_guide.md            # Step-by-step key setup + rate limits
```

### How the API System Works

Every API call flows through `scripts/api_caller.py` which:

1. **Checks rate limits** before calling (per-minute, per-day, per-month)
2. **Enforces delays** between calls to avoid IP blocks
3. **Logs every call** to `~/.financial-analysis/logs/api_usage.jsonl`
4. **On failure**: logs to `error_log.jsonl` and tries the next API in the fallback chain
5. **On all failures**: returns an error with details of every attempt

The tracker at `scripts/usage_tracker.py` aggregates usage and generates:
- Daily usage reports with % of free limit consumed per API
- Error reports showing which APIs failed and which fallbacks worked
- **Paid tier recommendations** when any API exceeds 70% of its free limit

### Fallback Chains

Every data category has a prioritized chain of APIs. If the primary fails or is rate-limited, the next one is tried automatically. The chains are defined in `scripts/api_config.py` → `FALLBACK_CHAINS`. Key chains:

| Data Category | Primary → Fallback(s) |
|--------------|----------------------|
| Price History | yfinance → Polygon → Alpha Vantage → FMP |
| Financial Statements | yfinance + SEC EDGAR → Finnhub → FMP |
| Analyst Ratings | Finnhub → yfinance → SA RapidAPI → Mboum |
| Insider Trades | SEC EDGAR → Finnhub → Mboum → yfinance |
| Congress Trades | Mboum → Quiver (paid) |
| Technical Indicators | Alpha Vantage → Mboum → Polygon → FMP |
| News Sentiment | Finnhub → Alpha Vantage → Alpaca |
| Reddit Sentiment | ApeWisdom → StockTwits |

## Three Use Cases

This skill supports three distinct workflows. The user will ask for one of them (or you can suggest the appropriate one based on context).

---

### Use Case 1: Weekly Portfolio Review

**Trigger**: User provides a PDF, CSV, or list of current holdings and asks for a review, analysis, or buy/hold/sell recommendations.

**Input**: Portfolio holdings (tickers + optional quantities/cost basis)
**Output**: Per-ticker rating (Buy / Hold / Trim / Sell) with confidence score, 3 entry levels, 3 sell targets, and key reasons.
**Frequency**: Once per week (Sunday/Monday)

#### Workflow

Execute these phases in order. Use `call_with_fallback()` from `scripts/api_caller.py` for every API call to get automatic fallback + logging.

**Phase A — Data Collection** (for each ticker in portfolio):
1. Fetch current price + 1yr daily OHLCV history (yfinance)
2. Pull quarterly financial statements: income, balance sheet, cash flow (yfinance + SEC EDGAR)
3. Get analyst ratings consensus: buy/hold/sell counts (Finnhub)
4. Scan insider activity last 90 days: Form 4 filings (SEC EDGAR)
5. Check insider sentiment score: MSPR (Finnhub)
6. Pull front-month options chain (yfinance)
7. Get news sentiment (Finnhub + Alpha Vantage)
8. Single call: Reddit trending tickers + mention velocity (ApeWisdom)
9. Single call: recent Congress trades (Mboum)
10. Single call: upcoming earnings calendar (Finnhub)

**Phase B — Technical Analysis** (computed locally with pandas-ta, no API calls):
- SMA/EMA suite (10/20/50/100/200)
- RSI (14), MACD (12,26,9), Bollinger Bands (20,2)
- Stochastic Oscillator, ADX
- Volume analysis + OBV
- Pivot points (Classic + Fibonacci)
- Fibonacci retracement + extensions from recent swing
- ATR for position sizing

**Phase C — Scoring** (all local compute):
- Fundamental score (0-100): revenue growth, margins, FCF, ratios, peer comparison
- Technical score (0-100): trend, momentum, volatility, S/R positioning
- Sentiment score (0-100): analyst + insider + Congress + news + social
- **Composite score**: 40% fundamental + 30% technical + 30% sentiment
- Rating: 75-100 = **Buy** · 40-74 = **Hold** · 0-39 = **Trim/Sell**

**Phase D — Output Generation** (per ticker):

| Field | Description |
|-------|-------------|
| Rating | Buy / Hold / Trim / Sell |
| Composite Score | 0-100 |
| Confidence | Strong / Moderate / Weak (based on phase alignment) |
| Entry 1 (Aggressive) | Current price (high conviction) |
| Entry 2 (Moderate) | Nearest support / Fib 38.2% |
| Entry 3 (Conservative) | Strong support / Fib 61.8% |
| Target 1 (T1) | Nearest resistance / Fib ext 127.2% |
| Target 2 (T2) | Major resistance / Fib ext 161.8% |
| Target 3 (T3) | Full extension / Fib ext 261.8% |
| Stop Loss | Below key support or 1.5× ATR |
| Key Catalysts | Top 3-5 bullish drivers |
| Key Risks | Top 3-5 bearish risks |

After all tickers are analyzed, run the usage report:
```python
from scripts.usage_tracker import get_tracker
get_tracker().print_daily_report()
get_tracker().save_daily_summary()
```

---

### Use Case 2: Daily Opportunity Scanner

**Trigger**: User asks to find new stock ideas, scan for opportunities, or identify swing trades.

**Input**: User's portfolio focus (e.g., "growth", "value", "income") and optional current holdings to avoid duplicates.
**Output**: Top 5 Portfolio Adds + Top 5 Swing Trades, each with score, 3 entries, 3 exits.
**Frequency**: Daily (before market open)

#### Workflow

**Phase A — Source Aggregation** (cast a wide net):
1. Scan all Tier 1+2 RSS feeds using `scripts/rss_feeds.py` → `scan_all_feeds()`. Extract tickers mentioned across all feeds.
2. Pull Seeking Alpha per-ticker RSS for top 5 tickers from step 1.
3. Get Reddit trending tickers (ApeWisdom) — cross-reference with RSS mentions.
4. StockTwits sentiment scan for top 10 overlapping tickers.
5. Check new Congress trades (Mboum).
6. Pull upcoming earnings in next 5 days (Finnhub).

**Phase B — Screening** (narrow down to top 20 candidates):
7. News sentiment on top 20 candidates (Finnhub).
8. SA quant ratings + factor grades for top 5 (SA RapidAPI).
9. AI sentiment score for top 5 (Alpha Vantage — 5 of 25/day).
10. Price + volume screening (yfinance) — 52wk range positioning, volume vs avg.
11. Financial health check for top 10 (yfinance) — revenue growth, margins, PE.
12. Analyst consensus for top 10 (Finnhub).
13. Insider activity for top 10 (SEC EDGAR).

**Phase C — Analysis** (for top 10 survivors):
14. Compute S/R levels + entry/exit targets (pandas-ta locally).
15. Check unusual options activity for top 5 (Mboum).
16. Multi-factor scoring + final ranking (local compute).

**Phase D — Output**:

Present two lists:

**Portfolio Adds** (growth-aligned, longer horizon):
- Ticker, Score, Rating, 3 Entries, 3 Exits, Stop Loss, R:R, Catalysts

**Swing Trades** (momentum-based, shorter horizon):
- Ticker, Score, Rating, 3 Entries, 3 Exits, Stop Loss, R:R, Catalysts, Time Horizon

---

### Use Case 3: On-Demand Stock Deep Dive

**Trigger**: User asks to analyze a specific stock, do a deep dive on a ticker, or asks "should I buy X?"

**Input**: 1-10 tickers
**Output**: Full analyst-grade report per ticker with Buy / Watch·Hold / Sell rating, 3 entries, 3 exits, and comprehensive analysis.

#### Workflow

This is the most thorough analysis — every available data source is queried. Four phases, ~30 API calls per ticker.

**Phase A — Fundamentals** (11 steps per ticker):
Company profile, 5yr income statement, quarterly income trends, balance sheet, cash flow, XBRL cross-validation from SEC EDGAR, key ratio computation (PE/PB/PS/PEG/EV-EBITDA/ROE/ROA/D-E/FCF yield), peer comparison (5 peers), earnings history + surprises, upcoming earnings date, dividend history.

**Phase B — Technicals** (17 steps, mostly local via pandas-ta):
2yr daily + 6mo intraday price history, SMA/EMA suite, RSI, MACD, Bollinger Bands, Stochastic, ADX, Volume + OBV, VWAP, Pivot Points, Fibonacci Retracement, Fibonacci Extensions, Volume Profile, ATR, Ichimoku Cloud. Cross-validate 2 indicators via Alpha Vantage API.

**Phase C — Sentiment & Alternative Data** (16 steps):
Analyst ratings consensus (Finnhub), price targets (yfinance), insider Form 4 filings (SEC EDGAR), insider MSPR (Finnhub), Congress trades (Mboum), institutional holders (yfinance), short interest, news sentiment (Finnhub + AV AI), Reddit mentions (ApeWisdom), StockTwits sentiment, SA quant ratings + factor grades (SA RapidAPI), SA per-ticker articles (RSS), options flow (yfinance), unusual options (Mboum), recent SEC filings scan.

**Phase D — Scoring & Output** (12 steps, all local):
Fundamental score (0-100), Technical score (0-100), Sentiment score (0-100), Composite score (weighted 40/30/30), Rating assignment (Buy ≥75 / Watch·Hold 40-74 / Sell <40), 3 Entry levels, 3 Exit targets, Stop Loss, Risk:Reward ratio, Confidence level, Key Catalysts, Key Risks.

Output a comprehensive per-ticker report with all findings. Only recommend trades where R:R ≥ 2:1.

---

## Error Handling

When any API call fails, the system:

1. **Logs the error** to `~/.financial-analysis/logs/error_log.jsonl` with timestamp, API, category, and error message
2. **Tries the fallback** — next API in the chain for that data category
3. **Logs fallback result** — records which fallback was used and whether it succeeded
4. If all fallbacks fail, continues with available data and notes the gap in the output

### Viewing Errors
```bash
python scripts/usage_tracker.py errors      # Last 7 days
python scripts/usage_tracker.py errors 30   # Last 30 days
```

### Common Errors and Fixes
| Error | API | Fix |
|-------|-----|-----|
| 429 Too Many Requests | yfinance | Increase delay to 5s. Reduce batch size. |
| 429 Rate Limited | Alpha Vantage | 25/day limit hit. Wait or use pandas-ta locally. |
| 403 Forbidden | SEC EDGAR | Set User-Agent email in config. |
| API key invalid | Any | Check `~/.financial-analysis/api_keys.json` |
| Connection timeout | Any | Automatic fallback triggers. Check internet. |

## Usage Reports & Paid Tier Recommendations

After each workflow run, the usage tracker saves a daily summary. When any API exceeds 70% of its free limit, it generates a paid tier recommendation:

```bash
python scripts/usage_tracker.py daily    # See today's report
python scripts/usage_tracker.py summary  # Save JSON summary
```

The summary includes per-API: calls today/this month, % of free limit, error count, and a severity rating (SAFE / WARNING / CRITICAL).

The APIs most likely to need upgrading (in order):
1. **Alpha Vantage** (25/day) — first to hit limits. Upgrade: $29.99/mo
2. **Mboum** (600/mo) — tight if running all 3 use cases daily. Upgrade: $9.95/mo
3. **SA RapidAPI** (1K/mo) — tight with heavy deep dive usage. Check RapidAPI pricing.

## Important Notes

- This skill provides data-driven analysis, not financial advice. Always do your own due diligence.
- yfinance is an unofficial library — data may be delayed or temporarily unavailable.
- SEC EDGAR data is authoritative but requires parsing.
- All timestamps are in the timezone of the market being analyzed (US Eastern for US stocks).
- The scoring system weights can be adjusted based on user preference.
