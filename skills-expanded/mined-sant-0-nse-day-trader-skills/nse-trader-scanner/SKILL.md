---
name: nse-trader-scanner
description: Chart Scanner for NSE. Scans Nifty 50/100/500 or the full NSE equity list for 20-day breakouts, bull flags, 20-DMA reclaims, oversold bounces, 52-week-high proximity and intraday opening-range breaks, then writes a watchlist for the news and entry skills. Use when the user says "scan the Indian market", "find NSE setups", "what is breaking out", "scan Nifty 100", "opening range breakout", "bull flags", "oversold stocks", "आज कौन सा स्टॉक", or at the start of an Indian trading day.
---

# nse-trader-scanner

Scans Indian equities bar by bar and produces a ranked watchlist. It supports
Nifty 50, Nifty 100, Nifty 500 and all NSE `EQ`-series shares. Data comes from
Yahoo's NSE chart feed (`.NS`) and may be delayed, so always confirm prices in
your broker or an exchange-grade feed. It never places an order.

## Run it

Quick Nifty 100 scan:

```bash
python scripts/scan.py --mode daily --universe nifty100 --top 10
```

Full NSE scan (can take several minutes):

```bash
python scripts/scan.py --mode daily --universe eq --min-price 50 --min-turnover 5
```

Opening-range scan:

```bash
python scripts/scan.py --mode intraday --universe nifty50 --top 10
```

For a fast smoke test, add `--limit 8`. `--min-turnover` is average daily
turnover in crore rupees. A custom universe is one NSE symbol per line:
`--universe file:my-stocks.txt`.

## Daily setups

| Label | Meaning |
|---|---|
| `20D_BREAKOUT` | close clears the prior 20-day pivot |
| `BULL_FLAG` | strong impulse, shallow pullback, turn up above 20-DMA |
| `RECLAIM_20MA` | close crosses back above the 20-day average |
| `OVERSOLD` | RSI14 ≤ 35 |
| `OVERSOLD_BOUNCE` | RSI turns up from oversold with a positive day |
| `52W_HIGH_PROX` | within 3% of the true one-year high |

The score also rewards trend alignment, relative volume and liquidity. A
setup score is a prioritisation aid, not a probability or recommendation.

## Intraday rules

- opening range = 09:15–09:30 IST (first three 5-minute bars)
- `OR_BREAKOUT` = first completed bar closing above the opening-range high
- `OR_LOW_BREAK` is a warning when price closes below the opening-range low
- the midpoint is saved as a stop hint for `nse-trader-exit`
- NSE cash session is 09:15–15:30; MIS trades should be flat by 15:15

## Files

| File | What |
|---|---|
| `assets/nifty50.txt`, `nifty100.txt`, `nifty500.txt` | bundled NSE constituents |
| `nse-trader/watchlist.json` | ranked items with setup, score and levels |

## Workflow

1. Run this scanner before or during the session.
2. Send `watchlist.json` to `nse-trader-news`.
3. Use `nse-trader-entry` to time one selected setup.
4. Plan the exit before sizing or approving anything.

Educational tooling only, not financial advice. Confirm symbols, prices,
liquidity, circuit limits and corporate actions in your broker and NSE sources.
