---
name: nse-trader-alerts
description: Price and time alerts for NSE. Creates once-only alerts for a price, plan stop, target, percentage move, the 09:15 opening bell or the 15:15 MIS flat-by time, understands NSE weekends and cached official holidays, and refuses to fire stale price alerts while the market is closed. Use when the user says "alert me when RELIANCE hits", "watch my stop", "target alert", "market open kab hoga", "remind me to exit by 3:15", or after nse-trader-exit.
---

# nse-trader-alerts

Persists one-shot alerts in your local `nse-trader/` workspace. Price checks use
the free Yahoo NSE chart feed; time alerts understand IST, weekends and the
official NSE 2026 holiday list. The script does not run in the background—your
agent, Task Scheduler or terminal must invoke `check`.

## Add alerts

```bash
# The direction is inferred from the current quote
python scripts/alerts.py add --ticker RELIANCE --level 1500 --note "breakout"

# Read stop and target from nse-trader/plan.json
python scripts/alerts.py add --stop
python scripts/alerts.py add --target

# 3% above the previous close (negative values make below alerts)
python scripts/alerts.py add --ticker TCS --pct 3

# Next trading-day opening bell / flat-by reminder
python scripts/alerts.py add --bell
python scripts/alerts.py add --ticker RELIANCE --flatby 15:15
```

## Check and manage

```bash
python scripts/alerts.py check --once
python scripts/alerts.py list
python scripts/alerts.py clear --id a1b2c3d4e5
python scripts/alerts.py clear                 # all
```

`check` always exits 0 after a valid check, even if nothing fired. A fired
alert stays `FIRED` and never repeats. Re-adding the identical alert does not
re-arm it; clear it or change the level.

## Safety and session rules

- normal NSE session 09:15–15:30 IST
- price alerts are checked only in `OPEN` or `SQUAREOFF`; a stale weekend or
  holiday quote cannot ring
- opening bell schedules 09:15 on the next valid trading day
- flat-by defaults are explicit; 15:15 is a conservative intraday cutoff, but
  verify your broker's actual square-off policy
- 2026 NSE holidays are an offline fallback; unknown years trigger a cached
  refresh from NSE's official holiday-master endpoint
- Yahoo prices may be delayed—confirm inside your broker

## Files

| File | What |
|---|---|
| `nse-trader/plan.json` | read by `--stop` / `--target` |
| `nse-trader/alerts.json` | all active and fired alerts |

This tool only prints reminders in the current execution environment. It does
not send push notifications and cannot close a position. Educational tooling,
not financial advice.
