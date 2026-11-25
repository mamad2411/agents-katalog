---
name: paper-trade-runner
description: Runs a signal-only paper-trading loop for Indian markets — generates entry signals, simulates fills at LTP, manages stop-loss and target, resolves at EOD, and persists trade history. Never places real orders. Trigger when user wants to paper trade, backtest live, simulate a strategy, or generate intraday signals without risk.
---

# Paper Trade Runner

The pattern behind a working signal-only daemon for Nifty / BankNifty intraday options.

## When to use

- User wants to test a strategy in live market conditions without real money.
- User wants signals delivered (UI / log / notification) but no order execution.
- User wants to build a P&L track record before sizing up.

## Core loop

```
every N seconds during market hours (09:15 – 15:30 IST):
  1. fetch live quotes / candles
  2. evaluate entry rules → generate signal (or skip)
  3. for each open position:
       a. update mark-to-market
       b. check stop-loss / target / time-stop
       c. if hit → resolve, log, free capital
  4. at 15:20 IST → force-close all open positions (intraday safety)
  5. at 15:35 IST → write EOD summary
```

## Required components

- **Signal generator** — pure function: `(market_state) → Signal | None`. Easy to unit test.
- **Position store** — JSON / SQLite. Each row: entry_time, instrument, side, qty, entry_price, sl, target, status, exit_time, exit_price, pnl.
- **Capital tracker** — starting balance, available margin, blocked margin. Reject signals that exceed available capital.
- **Loss cap** — hard stop at configurable daily DD (default: 5% of starting capital). Once hit, no new signals till next day.

## Signal schema

```json
{
  "id": "sig_20260606_0934_01",
  "instrument": "NIFTY26JUN24200CE",
  "side": "BUY",
  "qty": 50,
  "entry_price": 142.50,
  "stop_loss": 120.00,
  "target": 180.00,
  "rationale": "20EMA crossover + rising OI on 24200 CE",
  "generated_at": "2026-06-06T09:34:12+05:30"
}
```

## EOD review

At 15:35 IST, emit:
- Total signals generated / taken / passed
- Win rate, avg win, avg loss, expectancy
- Max DD intraday
- Best and worst trade with rationale

Feed this into `daily-pnl-reviewer` skill for journaling.

## Hard rules

- **No `kite.place_order()` call. Ever.** This skill is signal-only.
- **No leveraged sizing assumptions.** Use actual lot sizes and SEBI margin.
- **Square off at 15:20 IST** — intraday convention; avoids auto-square-off charges.

## Anti-patterns to refuse

- "Make this place real orders" → refuse, point to risk of unsupervised execution.
- "Remove the loss cap" → refuse, the cap is the moat.
