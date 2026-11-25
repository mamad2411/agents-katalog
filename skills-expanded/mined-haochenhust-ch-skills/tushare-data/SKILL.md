---
name: tushare-data
description: "This skill should be used when the user asks '查一下XX的行情', '拉一下财务数据', '估值数据', 'PE/PB多少', '股东变化', '业绩预告', or when any analysis/research task needs A-share market data, financial statements, valuation metrics, or shareholder data. Tushare Pro is the PRIMARY structured data source — more stable and comprehensive than AKShare. Requires a TUSHARE_TOKEN env var (your own Tushare Pro token)."
version: 1.0.0
effort: medium
---

# Tushare Data

Primary structured data source for A-share investment research via the [Tushare Pro](https://tushare.pro) API. A thin CLI wrapper (`scripts/fetch_tushare.py`) over the `tushare` Python SDK.

## When to Use

- Any task needing stock fundamentals, valuation, or financial statements
- Preferred over AKShare for: financial statements, PE/PB/PS, shareholder data, earnings forecasts
- AKShare remains preferred for: ETF data, sector fund flows, northbound capital (Tushare needs higher points)

## Setup

1. Get a token: register at https://tushare.pro and copy your API token from the user center. Financial-statement interfaces need ~2000 points.
2. Install deps and export your token:

```bash
python3 -m venv .venv
.venv/bin/pip install tushare pandas
export TUSHARE_TOKEN=<your Tushare Pro token>      # never hard-code this
PY=.venv/bin/python3
```

The script reads the token from the `TUSHARE_TOKEN` env var (or a `--token` flag). Keep it in your shell profile or a secret manager, not in the skill.

## Available Interfaces

### Market Data
| Mode | Description | Key Fields |
|------|-------------|------------|
| `daily` | Daily OHLCV | open, high, low, close, vol, pct_chg |
| `weekly` | Weekly OHLCV | Same as daily |
| `monthly` | Monthly OHLCV | Same as daily |
| `daily_basic` | Daily valuation | PE, PE_TTM, PB, PS, turnover, total_mv, circ_mv, dv_ratio |
| `adj_factor` | Adjustment factor | For computing forward/backward adjusted prices |
| `stock_basic` | Stock list | ts_code, name, industry, area, list_date, act_name |
| `trade_cal` | Trading calendar | cal_date, is_open, pretrade_date |

### Financial Statements
| Mode | Description | Key Fields |
|------|-------------|------------|
| `income` | Income statement | revenue, total_revenue, n_income, basic_eps, ebit, ebitda |
| `balancesheet` | Balance sheet | total_assets, total_liab, total_hldr_eqy, inventories |
| `cashflow` | Cash flow | n_cashflow_act, n_cashflow_inv_act, free_cashflow |
| `fina_indicator` | Financial ratios | ROE, ROA, grossprofit_margin, netprofit_margin, current_ratio, debt_to_assets, netprofit_yoy |

### Earnings & Dividends
| Mode | Description | Key Fields |
|------|-------------|------------|
| `forecast` | Earnings forecast | type (预增/预减/扭亏/首亏), net_profit_min/max, p_change_min/max |
| `express` | Earnings express | Quick earnings release before full report |
| `dividend` | Dividends | cash_div, stk_div, record_date, ex_date |

### Shareholder & Capital
| Mode | Description | Key Fields |
|------|-------------|------------|
| `top10_holders` | Top 10 shareholders | holder_name, hold_amount, hold_ratio, hold_change |
| `stk_holdernumber` | Shareholder count | Tracks concentration/dilution |
| `moneyflow` | Capital flow | Net inflow by trade size |
| `margin` | Margin trading | Market-wide margin data |

### Index & Fund
| Mode | Description | Key Fields |
|------|-------------|------------|
| `index_daily` | Index OHLCV | Same as daily for indices |
| `index_weight` | Index components | con_code, weight |
| `fund_basic` | Fund list | name, fund_type, management |
| `concept` | Concept themes | Thematic stock groups |
| `concept_detail` | Concept members | Stocks in each concept |

## Command Reference

```bash
# Stock info
$PY scripts/fetch_tushare.py --mode stock_basic --symbols 002463.SZ

# Daily price (date range)
$PY scripts/fetch_tushare.py --mode daily --symbols 002463.SZ --start 20260101 --end 20260317

# Daily valuation (PE/PB/turnover/market cap)
$PY scripts/fetch_tushare.py --mode daily_basic --symbols 002463.SZ --start 20260301

# Income statement / ratios / balance sheet / cash flow
$PY scripts/fetch_tushare.py --mode income --symbols 002463.SZ
$PY scripts/fetch_tushare.py --mode fina_indicator --symbols 002463.SZ
$PY scripts/fetch_tushare.py --mode balancesheet --symbols 002463.SZ
$PY scripts/fetch_tushare.py --mode cashflow --symbols 002463.SZ

# Earnings forecast / dividends / shareholders
$PY scripts/fetch_tushare.py --mode forecast --symbols 002463.SZ
$PY scripts/fetch_tushare.py --mode dividend --symbols 002463.SZ
$PY scripts/fetch_tushare.py --mode top10_holders --symbols 002463.SZ
$PY scripts/fetch_tushare.py --mode stk_holdernumber --symbols 002463.SZ

# Index components (CSI 300) / concept themes
$PY scripts/fetch_tushare.py --mode index_weight --symbols 000300.SH
$PY scripts/fetch_tushare.py --mode concept
```

## Tushare vs AKShare Decision Guide

| Need | Use Tushare | Use AKShare |
|------|-------------|-------------|
| Daily OHLCV | ✅ More stable | Backup |
| PE/PB/PS valuation | ✅ daily_basic | Limited |
| Financial statements | ✅ Structured, typed | Basic summary |
| Earnings forecast | ✅ forecast/express | Not available |
| Shareholder data | ✅ top10_holders | Not available |
| Dividend data | ✅ dividend | Not available |
| ETF search/data | Use AKShare | ✅ Better coverage |
| Northbound capital | Use AKShare | ✅ Free |
| Sector fund flows | Use AKShare | ✅ Free |
| Limit-up/down pool | Use AKShare | ✅ Free |

(For AKShare-based fetching, see the sibling `stock-market-data` and `financial-data-fetcher` skills.)

## Rules

1. **Always set TUSHARE_TOKEN env var** before calling the script — never hard-code it
2. **Tushare stock codes use suffix**: .SZ (Shenzhen), .SH (Shanghai), .BJ (Beijing)
3. **Date format**: YYYYMMDD (no dashes)
4. **Rate limit**: ~50 requests/minute at 2000 points level
5. **Financial data lag**: statements available after company announces (check ann_date)
