---
name: nse-trader-risk
description: Broker-neutral Risk Manager for NSE. Checks every ticket against your limits and blocks anything over them before manual entry: stop required, per-trade loss, reward:risk, daily loss, trades per day, entry window, flat-by time, blocked names, duplicates and F&O capital. Use when the user says "check my order", "is this safe", "risk check", "can I take this trade", or before nse-trader-broker, always.
---

# nse-trader-risk

The gate between a sized order and your broker. Prints **PASS** or **BLOCK**
with the exact reason, and records every verdict so the day's risk adds up.
No manual broker ticket is produced without a PASS from this skill.

## Run it

```bash
python scripts/risk.py --order nse-trader/orders.json --capital 50000
```

```
PASS  RELIANCE  qty 34  risk@stop Rs 197.20  day risk now Rs 197.20
  next: nse-trader-broker to print the manual broker ticket
```

Blocked example:

```
BLOCK  RELIANCE
  - outside the entry window 09:15-15:00
  - day risk Rs 1,240.00 would exceed the daily limit Rs 1,000.00
```

## Checks, in order

1. ticket well-formed (ticker, positive qty, prices, known segment)
2. stop exists and sits below entry
3. reward:risk ≥ minimum (default 1.5)
4. loss at the stop — measured from the **higher** of entry and a fresh quote
   with `--fresh-quote` — fits the per-trade limit, charges included
5. session is open, inside the 09:15–15:00 entry window, before 15:15
6. ticker not on the blocked list
7. futures estimated margin, long-option premium, or cash cost fits your capital
8. day's risk + this trade ≤ daily limit (default 2× per-trade limit, plus
   `--day-loss` for realised losses)
9. trades today < max (default 5)
10. no duplicate PASS for the same ticker today

## Rules file

Override defaults with `--rules rules.json`:

```json
{
  "max_loss_per_trade": 500,
  "daily_loss_limit": 1000,
  "max_trades_per_day": 3,
  "min_rr": 2,
  "entry_window": ["09:20", "14:45"],
  "flat_by": "15:15",
  "blocked_tickers": ["XYZ"],
  "margin_pct": 15
}
```

`--now 2026-11-02T09:45` overrides the clock for testing or replay.

## Files

| File | What |
|---|---|
| `nse-trader/orders.json` | read: the ticket to judge |
| `nse-trader/risk_state.json` | written: verdicts, day risk, trade count |

## Exit codes

`0` PASS · `3` BLOCK · `2` bad input. Scripts and agents can rely on these.

## Example session

1. `nse-trader-budget` wrote a 34-share RELIANCE ticket.
2. `risk.py --capital 50000` → PASS, day risk Rs 197.
3. A second RELIANCE ticket the same day → BLOCK (duplicate).
4. `nse-trader-broker` only shows a ticket that passed.

Not financial advice. It enforces the rules you set; it does not pick trades.

F&O scope is long futures and **long options** only. It does not approve naked
or short-option strategies.
