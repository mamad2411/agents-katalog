---
name: nse-trader-exit
description: Exit Planner for NSE. Sets your stop and target before you enter, using the opening-range midpoint, an explicit level, or ATR, with NSE tick rounding and a hard flat-by time for MIS. Use when the user says "where's my stop", "set my stop and target", "plan the exit", "when do I get out", "stop loss", "what's my R", or right after nse-trader-entry triggers, before nse-trader-timemachine.
---

# nse-trader-exit

Sets the stop and target **before** the entry. On NSE intraday (MIS) the
position is squared off around 15:15, so every plan carries a flat-by time.
Prices round to the NSE cash tick of Rs 0.05 (stop down, target up). Long side
only. It never places an order.

## When to use

- "where's my stop", "set my stop and target", "plan the exit", "what's my R"
- right after `nse-trader-entry` says TRIGGERED
- before `nse-trader-timemachine`, `nse-trader-budget`, `nse-trader-risk`

## Run it

```bash
python scripts/exit.py --ticker RELIANCE --entry 1452.50 --or-low 1441.00 --or-high 1456.00 --rr 2
```

Futures or a **long option premium** (use the exact NSE contract symbol):

```bash
python scripts/exit.py --ticker NIFTY26NOV26000CE --entry 180 --stop 150 \
  --target 240 --segment FNO --instrument OPTION
```

```
PLAN  RELIANCE  entry 1452.50  stop 1448.50  target 1460.50  RR 2.0
  stop basis   : opening-range midpoint
  risk/share   : Rs 4.00
  flat by      : 15:15 (MIS)
  saved        : nse-trader/plan.json
```

Stop sources, in order of precedence:

| Source | Flag | Basis label |
|---|---|---|
| Your price | `--stop 1447` | explicit stop |
| Opening-range midpoint | `--or-low 1441 --or-high 1456` | opening-range midpoint |
| ATR multiple | `--atr-mult 1.5` (fetches ATR14) | ATR14 x 1.5 |
| Default | none | 0.8% below entry |

Target: `--target` or `--rr` (default 2R).

If `nse-trader/entry.json` exists for the ticker, `--from-entry` fills the
opening range automatically.

## Rules it enforces

- stop must be **below** entry, target **above** it
- stop distance at least max(2 ticks, 0.15% of entry) — too-tight stops are
  refused because the Rs 0.05 tick and spread will eat them
- reward:risk at least 0.5; invalid plans exit code 2 with the reason
- cash defaults to `MIS`; F&O defaults to the common `NRML` label. Map these
  labels to the equivalent product in your broker before manual entry
- `MIS`/`NRML` day-trade plans → flat-by 15:15, `CNC` → 15:30
- `FNO` requires `--instrument FUTURE` or `OPTION`; options here mean buying a
  premium with a stop below entry, never naked option selling
- plan is refused if it would be placed outside the current session without a
  note; the note says so instead of pretending it is live

## Files

| File | What |
|---|---|
| `nse-trader/plan.json` | written: entry, stop, target, rr, flat_by, ticket |
| `nse-trader/entry.json` | read with `--from-entry` |

## Example session

1. `nse-trader-entry` reported `TRIGGERED at 1452.50` on RELIANCE with OR
   1441–1456.
2. `exit.py --ticker RELIANCE --entry 1452.50 --from-entry --rr 2` → stop
   1448.50, target 1460.50.
3. `nse-trader-timemachine --plan nse-trader/plan.json` to see the odds.

Not financial advice. Educational tooling only.
