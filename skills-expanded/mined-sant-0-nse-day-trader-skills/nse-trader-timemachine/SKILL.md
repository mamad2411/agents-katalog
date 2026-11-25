---
name: nse-trader-timemachine
description: Time Machine for NSE trades. Replays a planned entry, stop and target against recent 5-minute sessions and runs 10,000 bootstrap simulations to estimate target-first, stop-first and neither outcomes before sizing. Use when the user says "run the time machine", "replay this NSE trade", "what are the odds", "simulate this trade", "Monte Carlo", "backtest this setup", "target hit hoga?", or after nse-trader-exit and before nse-trader-budget.
---

# nse-trader-timemachine

Stress-tests the plan from `nse-trader-exit` against the ticker's own recent
5-minute NSE bars. It reports target-first, stop-first and neither-by-15:15
frequencies, average R and comparable historical triggers. It does **not**
claim to forecast tomorrow and never places an order.

## Run it

```bash
python scripts/timemachine.py --plan nse-trader/plan.json --sims 10000 --days 60
```

Example output:

```text
TIME MACHINE  RELIANCE  10,000 simulations  41 sessions
  target first :  38.4%
  stop first   :  44.1%
  neither      :  17.5%
  average R    : +0.082
  history      : 12 comparable triggers
  verdict      : MIXED - no robust target-first edge in this sample
```

Use `--seed 42` (the default) for a repeatable run. The script refuses malformed
plans and fewer than three complete sessions.

## What it actually measures

1. Fetches up to 60 days of 5-minute `.NS` bars.
2. Keeps regular-session bars from 09:15 through the 15:15 MIS flat-by time.
3. **Historical replay:** finds sessions where price crossed upward through the
   planned entry after 09:30, then checks stop versus target first.
4. **Bootstrap:** samples a recent session and resamples its observed 5-minute
   high/low/close shapes, starting at the proposed entry.
5. A bar containing both stop and target counts as **stop first**—conservative
   because OHLC cannot reveal intrabar order.

## Verdicts

- `FAVOURABLE_IN_SAMPLE` — target-first leads by at least ten points and
  average R is positive
- `MIXED` — no clear separation
- `UNFAVOURABLE_IN_SAMPLE` — stop-first dominates or average R is materially
  negative
- `INSUFFICIENT_HISTORY` — fewer than five comparable historical triggers

These are sample descriptions, not trade recommendations.

## Files

| File | What |
|---|---|
| `nse-trader/plan.json` | read: ticker, entry, stop, target |
| `nse-trader/sim.json` | probabilities, average R, replay details, limitations |

## Important limitations

- delayed third-party data; confirm in your broker or exchange-grade feed
- recent observations only; no out-of-sample guarantee
- resampling does not preserve news, regime or serial dependence
- charges, slippage, gaps, circuit limits and rejections are not simulated
- an absolute entry may produce few historical crosses if price shifted

Run `nse-trader-budget` next only after you decide the plan is still worth
considering. Educational tooling only, not financial advice.
