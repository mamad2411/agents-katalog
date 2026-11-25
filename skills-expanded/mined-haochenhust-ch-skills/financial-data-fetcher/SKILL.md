---
name: financial-data-fetcher
description: "This skill should be used when the user asks to '查一下XX的财务数据', '这只股票估值多少', '找一下XX ETF', '对比一下同行', 'ETF日线行情', or when any analysis task needs financial statements, valuation metrics, ETF listings, or ETF daily OHLCV data. Fetches stock financials (revenue, profit, margins, ROE, PE/PB) and ETF data via Tushare Pro (primary) and AKShare (fallback + ETFs)."
version: 1.0.0
effort: medium
---

# Financial Data Fetcher

Fetch financial statements, valuation metrics, and ETF data. **Tushare Pro is the primary data source** (more stable, richer data); AKShare as fallback and for ETFs.

This skill orchestrates the fetch scripts shipped by the sibling `tushare-data` and `stock-market-data` skills. Install those first, then point the variables below at wherever you installed them.

## Setup

```bash
export TUSHARE_TOKEN=<your Tushare Pro token>       # never hard-code; see the tushare-data skill
PY=python3                                          # a python3 with tushare/pandas/akshare (e.g. stock-market-data/.venv/bin/python3)
SKILLS=~/.claude/skills                             # where these skills are installed
TUSHARE_SCRIPT=$SKILLS/tushare-data/scripts/fetch_tushare.py
AKSHARE_SCRIPT=$SKILLS/stock-market-data/scripts/fetch_financial_data.py
```

### Primary: Tushare Pro (preferred)

```bash
# Financial statements
$PY $TUSHARE_SCRIPT --mode income --symbols 002463.SZ
$PY $TUSHARE_SCRIPT --mode balancesheet --symbols 002463.SZ
$PY $TUSHARE_SCRIPT --mode cashflow --symbols 002463.SZ

# Financial ratios (ROE, margins, growth)
$PY $TUSHARE_SCRIPT --mode fina_indicator --symbols 002463.SZ

# Valuation (PE/PB/PS/market cap/dividend yield)
$PY $TUSHARE_SCRIPT --mode daily_basic --symbols 002463.SZ --start 20260101

# Earnings forecast & express
$PY $TUSHARE_SCRIPT --mode forecast --symbols 002463.SZ
$PY $TUSHARE_SCRIPT --mode express --symbols 002463.SZ

# Dividends
$PY $TUSHARE_SCRIPT --mode dividend --symbols 002463.SZ

# Shareholder data
$PY $TUSHARE_SCRIPT --mode top10_holders --symbols 002463.SZ
$PY $TUSHARE_SCRIPT --mode stk_holdernumber --symbols 002463.SZ
```

**Note:** Tushare codes use suffix: .SZ (Shenzhen), .SH (Shanghai), .BJ (Beijing)

### Fallback: AKShare (for ETFs and when Tushare unavailable)

#### ETF Daily OHLCV

```bash
# Single ETF daily history (default: last 60 days)
$PY $AKSHARE_SCRIPT --mode etf-daily --symbols 159967

# Date range
$PY $AKSHARE_SCRIPT --mode etf-daily --symbols 159967 --start 20260101 --end 20260321

# Multiple ETFs
$PY $AKSHARE_SCRIPT --mode etf-daily --symbols 510300,159967 --start 20260301
```

Returns: date, open, close, high, low, volume, amount (+ amplitude, change_pct, turnover when eastmoney source available). Uses eastmoney as primary source with sina fallback.

#### Individual Stock Financials

```bash
# Single stock
$PY $AKSHARE_SCRIPT --mode stock --symbols 002463

# Multiple stocks (peer comparison)
$PY $AKSHARE_SCRIPT --mode stock --symbols 002463,300724,600183
```

Returns:
- **financial_abstract**: Revenue, net profit, gross margin, NAV per share, debt ratio — across last 4 reporting periods
- **financial_ratios**: Net margin, ROE, ROA, debt ratio, current ratio, asset turnover, operating margin
- **price**: Latest close, change%, volume, turnover
- **valuation**: Approximate PE (TTM) and PB
- **profit_yoy_growth** / **revenue_yoy_growth**: YoY growth rates

#### ETF Search

```bash
# Search ETFs by keyword
$PY $AKSHARE_SCRIPT --mode etf --filter 半导体

# List cross-border ETFs (US, HK, Japan, etc.)
$PY $AKSHARE_SCRIPT --mode etf-cross-border

# List sector/industry theme ETFs
$PY $AKSHARE_SCRIPT --mode etf-sector
```

Returns: ETF list sorted by volume (most active first), with code, name, price, change%, volume, amount.

## Data Coverage

### Stock Financials
- Source: AKShare `stock_financial_abstract` + `stock_financial_analysis_indicator`
- Coverage: All A-share stocks
- Periods: Latest 4 quarterly reports + historical
- Key metrics: Revenue, profit, margins, ROE, ROA, debt ratio, turnover ratios

### ETFs
- Source: AKShare `fund_etf_category_sina`
- Coverage: ~1400+ ETFs on A-share market
- Cross-border categories: 纳指, 标普, 恒生, 港股, 中概, 日经, 黄金, 原油, QDII
- Sector categories: 半导体, AI, 机器人, 新能源, 医药, 军工, 证券, 消费, etc.

## Data Source Priority

1. **Tushare Pro** (primary) — financial statements, ratios, valuation, forecasts, shareholder data
2. **AKShare** (fallback/complement) — ETF data, quick summary when Tushare unavailable

## Known Limitations

- AKShare price data may intermittently fail due to eastmoney proxy issues
- AKShare PE calculation is approximate (not true TTM); prefer Tushare daily_basic for accurate PE/PB
- Tushare requires 2000+ points for financial data access
- No real-time intraday data from either source, only daily close
