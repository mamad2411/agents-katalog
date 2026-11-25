---
name: armstat
description: Fast, read-only per-arm turn-log summary — billable turn count, httpStatus tally (catches rate-limiting / non-200s mid-run), cache_read/creation sums with the ephemeral 5m-vs-1h split (a direct knob-sanity check: A2/A3/A5 should show ephemeral_1h > 0, A0/A1/A4 should not), token-weighted hit rate, and thinkingBudget. Unlike the heavyweight `bench` analyzer it does no bootstrap/CI/pricing, so it is cheap to run at each arm boundary WHILE a suite is still in flight. Safe on a live, actively-appended NDJSON file (a partial trailing line is skipped). Use it to spot-check a just-finished arm before the next one starts.
---

# clawback per-arm turn-log stats

Run from the project root against one or more turn-log NDJSON files:

```bash
node benchmark/bin/arm_stat.js runs/<run>/turns.A0.ndjson
node benchmark/bin/arm_stat.js runs/<run>/turns.*.ndjson   # whole suite so far
```

Read-only — it only reads files already on disk, never the running proxy, so
it is safe to run while a benchmark arm is still driving.

## What it reports, per file

- `turns` — billable client turns (+ keep-alive `treatment-ping` records,
  counted separately and excluded from the billable tally), and any partial
  trailing line skipped on a live file.
- `httpStatus` — status tally with a ✓ when all are 200, or a ⚠️ flag the
  moment any non-200 appears (early rate-limit / error detection mid-run).
- `ttlMode` — `5m`/`1h` tally (passthrough arms stay `5m`).
- `cache_read` / `cache_create` — token sums, plus the per-turn first→last
  cache_read (warm-cache build-up), and the **ephemeral 5m-vs-1h split**. The
  split is a direct knob check: the 1h-TTL arms (A2/A3/A5) should show
  `ephemeral_1h > 0`; A0/A1/A4 should not.
- `hit rate` — token-weighted `cache_read / (cache_read + cache_create +
  input)`. A quick diagnostic only; the defensible headline is billable input
  reclaimed per turn with a CI, which the `bench` analyzer computes.
- `thinkingBudget` — distinct budgets seen and how many turns carried one
  (Haiku emits ~31999 regardless of `--effort`).

## When to use

- At each arm boundary of an in-flight suite, to confirm the just-finished arm
  produced turns, hit no rate-limit (all 200), warmed its cache, and applied
  the knob it was supposed to (5m vs 1h).
- NOT a substitute for `bench`: no CIs, no gap-bucket stratification, no
  pricing. Run `bench` for the committed study report.

## Sensitivity

Turn-logs carry per-turn token usage (not prompt content). Treat the run
directory as sensitive; this tool prints only counts and token sums.
