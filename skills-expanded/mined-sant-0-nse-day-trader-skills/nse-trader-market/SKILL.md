---
name: nse-trader-market
description: Indian Market Overview. Analyzes NIFTY 50, BANK NIFTY, India VIX, Nifty 50/100 breadth, sector rotation, and FII/DII cash flow, then produces a transparent 0-100 market-health score with dated data-confidence and provisional-session labels. Use when the user says "analyze the Indian market today", "market outlook", "is the market bullish", "Nifty today", "market breadth", "risk on or risk off", or before scanning individual setups.
---

# nse-trader-market

Use this as the first step for **“Analyze the Indian market today.”** It joins
index trend, stock participation, volatility, sector rotation, and institutional
cash flow into a dated market-context report. It never places orders and its
score is not a buy/sell signal.

## Run it

```bash
python scripts/market.py
```

Default: Nifty 100 breadth, nine sector indices, NIFTY 50, BANK NIFTY, India
VIX, and latest FII/DII data.

Useful options:

```bash
# Faster, narrower market breadth
python scripts/market.py --universe nifty50

# Smoke test / explicitly degraded scope
python scripts/market.py --universe nifty50 --limit 10

# Skip optional sources when they are unavailable
python scripts/market.py --skip-sectors --skip-flows

# Control parallel quote requests and output location
python scripts/market.py --workers 4 --out reports/today
```

## Score contract

| Component | Maximum |
|---|---:|
| NIFTY 50 trend: 1D change, 20DMA, 50DMA | 25 |
| Breadth: advances, above 20DMA, above 50DMA | 35 |
| India VIX level and direction | 15 |
| BANK NIFTY confirmation | 10 |
| Sector participation | 10 |
| FII/DII cash flow | 5 |

Missing optional components are excluded and weights are normalized over the
available evidence. The report always shows `available_points` and each
component's exact contribution.

FII/DII carries extra rules because NSE publishes the daily aggregates after
market close:

- every FII/DII number is displayed with its session date, `data_date` and
  `data_status` (`LIVE`, `CURRENT_SESSION`, `PREVIOUS_SESSION`, `END_OF_DAY`,
  `STALE`, `UNKNOWN`) — never as a bare `FII Net: ₹X Cr` line
- freshness is measured in **completed trading sessions** (`sessions_behind`
  against `latest_completed_session`), not calendar days. Friday data on
  Monday — or on the Tuesday after a Monday holiday — is the latest available
  published session; do not call it stale because the calendar age is 3+ days
- `freshness_status` (`FRESH`, `DELAYED`, `STALE`, `UNKNOWN`) reflects actual
  trading-session distance: 0 sessions behind = FRESH, 1 = DELAYED, more =
  STALE, unverified calendar or missing date = UNKNOWN
- the figures are never labelled live; `is_live` is false because no skill in
  this pack receives live intraday institutional flow
- `DELAYED`/`STALE` (a newer completed session exists than the data date),
  `UNKNOWN` (missing or unparseable source date), or an unverified holiday
  calendar keeps the flows out of the score with a warning
- the component detail states the session date, sessions behind, and that the
  data is context only, not live intraday flow or an entry trigger

| Score | Zone |
|---:|---|
| 75–100 | `RISK_ON` |
| 60–74.9 | `POSITIVE` |
| 40–59.9 | `NEUTRAL` |
| 25–39.9 | `CAUTIOUS` |
| 0–24.9 | `RISK_OFF` |

Zones describe current evidence; they do not prescribe exposure or orders.

## Breadth contract

For the selected Nifty universe, calculate on the dominant business date:

- advancers / decliners / unchanged
- percentage above 20-day and 50-day moving averages
- 20-day closing highs and lows
- equal-weight and median one-day change
- current/stale symbols and coverage percentage

Do not combine stale rows with the dominant-date breadth ratios.

## Snapshot labels

- `LIVE_SESSION_PROVISIONAL`: NSE is open/squaring off and the index data date
  is today. Daily bars can still change.
- `LAST_COMPLETED_SESSION`: after hours, weekends, holidays, or when the source
  only has the prior session.

Always state `as_of_date`, `generated_ist`, data confidence, component coverage,
breadth coverage, and source errors.

Data confidence measures source availability, date alignment, and breadth
coverage. It is not confidence in a forecast.

## Outputs

| File | Contents |
|---|---|
| `nse-trader/market.json` | machine-readable snapshot, score and provenance |
| `nse-trader/market.md` | human market report |

Use `NSE_TRADER_STATE_DIR` or `--out` to change the state location.

## Workflow handoff

```text
nse-trader-market → nse-trader-scanner → nse-trader-news
                  → entry/exit/simulation → budget → risk → manual ticket
```

Run the scanner only after the market overview when the user's goal is broad
market analysis. A healthy index with weak breadth is selective, not broadly
confirmed.

## Data sources and limitations

- Yahoo chart JSON for indices, VIX, sectors, and constituent daily bars
- NSE `fiidiiTradeReact` (daily aggregates published **after** the session;
  previous-session/end-of-day context, never live intraday flow)
- bundled Nifty constituent snapshots for breadth
- quotes may be delayed; full-universe requests may have partial failures
- FII/DII publication dates can lag the index snapshot; stale or undated
  FII/DII is excluded from the score rather than silently used
- this is not a macro, valuation, derivatives-positioning, or forecasting model

Educational tooling only. Verify all data before financial decisions.
