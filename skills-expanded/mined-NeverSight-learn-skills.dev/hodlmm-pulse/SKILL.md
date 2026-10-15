---
name: hodlmm-pulse
description: "Fee velocity and volume momentum tracker for Bitflow HODLMM pools — detects entry windows by comparing today's fee capture against the 7-day baseline, building a local time-series to surface trend direction (accelerating, stable, cooling)."
metadata:
  author: "ghislo749"
  author-agent: "Grim Seraph"
  user-invocable: "false"
  arguments: "doctor | scan | track | report"
  entry: "hodlmm-pulse/hodlmm-pulse.ts"
  requires: ""
  tags: "defi, read-only, mainnet-only, l2, infrastructure"
---

# HODLMM Pulse

Fee velocity and volume momentum tracker for Bitflow HODLMM (DLMM) concentrated liquidity pools.

## What it does

Answers the question **"is now a good time to deploy liquidity?"** by tracking *how fast* fees are being generated relative to the 7-day rolling baseline. A pool earning 3× its daily average in fees is in an active volume spike — the prime window to enter, capture fees, and exit before volume normalises.

Two modes of operation:

1. **Single-shot** (`scan`) — instant momentum ranking across all pools from a single API call. Useful for quick triage.
2. **Time-series** (`track` + `report`) — run `track` on a cron (e.g. every 5 min) to build a local snapshot history. The more data collected, the more accurate the trend direction (accelerating / stable / cooling). `report` surfaces the full picture.

## Why agents need it

`hodlmm-advisor` tells you *where* to deploy (which pool has the best risk-adjusted yield). `hodlmm-pulse` tells you *when* — detecting fee spikes and volume acceleration before they appear in slow-moving APR averages. Together they form a complete LP entry decision loop:

1. `hodlmm-pulse scan` → identify pools with active momentum
2. `hodlmm-pulse track --pool-id <id>` → confirm trend direction over multiple polls
3. `hodlmm-advisor entry-plan --pool-id <id>` → get exact bin range + strategy
4. Execute only when both pulse signal is `spike`/`elevated` and advisor returns `"Deploy now"`

## Safety notes

- **Read-only** — never submits transactions or moves funds
- **No wallet required** — safe to call from any agent without authentication
- **Mainnet-only** — Bitflow HODLMM API is mainnet-only
- State file written to `~/.hodlmm-pulse-state.json` (local disk only, no network writes)
- Rolling window: last 288 snapshots per pool (~24h at 5-min polling intervals)

## Commands

### doctor

Checks all data sources and state file readiness.

```bash
bun run hodlmm-pulse/hodlmm-pulse.ts doctor
```

### scan

Fetches all pools in one call, computes momentum scores, ranks by fee velocity. Use for quick triage without needing prior tracking history.

```bash
bun run hodlmm-pulse/hodlmm-pulse.ts scan
bun run hodlmm-pulse/hodlmm-pulse.ts scan --min-tvl 10000
```

Options:
- `--min-tvl <usd>` — exclude pools below this TVL (default: 500)

### track

Appends a timestamped snapshot for a single pool to local state, then outputs the current signal and trend direction. Trend accuracy improves with each successive call.

```bash
bun run hodlmm-pulse/hodlmm-pulse.ts track --pool-id dlmm_1
```

Options:
- `--pool-id` (required) — pool identifier (e.g. `dlmm_1`, `dlmm_3`)

Recommended: run via cron every 5 minutes for each pool of interest.

### report

Reads all stored snapshots and outputs a trend summary per pool: current signal, trend over the full tracking window, peak momentum seen. Prioritises pools with active signals at the top.

```bash
bun run hodlmm-pulse/hodlmm-pulse.ts report
bun run hodlmm-pulse/hodlmm-pulse.ts report --pool-id dlmm_1
```

Options:
- `--pool-id` (optional) — limit output to one pool

## Momentum model

### Fee velocity

Primary signal. Ratio of today's fees to the 7-day daily average:

```
feeVelocity = feesUsd1d / (feesUsd7d / 7)
```

`1.0` = average day. `3.0` = earning 3× the daily average.

### Volume velocity

Secondary signal. Same ratio applied to volume:

```
volumeVelocity = volumeUsd1d / (volumeUsd7d / 7)
```

### APR spike ratio

Tertiary signal. How much today's realized APR exceeds the long-run average:

```
aprSpike = apr24h / apr
```

### Momentum score (composite, weighted)

```
momentumScore = feeVelocity × 0.6 × 50 + volumeVelocity × 0.3 × 50 + aprSpike × 0.1 × 50
```

`50` = average day. Higher = more active than usual.

### Signal thresholds

| Signal | Condition | Meaning |
|---|---|---|
| `🔥 spike` | feeVelocity ≥ 3× | Exceptional activity — prime entry window |
| `📈 elevated` | feeVelocity ≥ 1.5× | Above average — monitor closely |
| `〰️ normal` | 0.5× ≤ feeVelocity < 1.5× | Within baseline — no special action |
| `📉 cooling` | feeVelocity < 0.5× | Below baseline — not an entry window |
| `⬜ flat` | Fees + volume near zero | Inactive pool — skip |

### Trend direction (time-series only)

| Trend | Meaning |
|---|---|
| `⬆️ accelerating` | Fee velocity rising across recent snapshots |
| `↔️ stable` | Fee velocity flat — activity sustained |
| `⬇️ cooling` | Fee velocity declining — window closing |
| `🆕 new` | Insufficient history (< 2 snapshots) |
| `— flat` | Pool is inactive |

## Output contract

All outputs are JSON to stdout.

**Success:**
```json
{ "status": "success", "network": "mainnet", "timestamp": "...", ... }
```

**Error:**
```json
{ "error": "descriptive message" }
```

## Data sources

| Source | Data | Endpoint |
|---|---|---|
| Bitflow App API (pools list) | All pools: feesUsd1d, feesUsd7d, volumeUsd1d, volumeUsd7d, apr, apr24h, tvlUsd | `bff.bitflowapis.finance/api/app/v1/pools` |
| Bitflow App API (pool detail) | Single pool detail (used by `track`) | `bff.bitflowapis.finance/api/app/v1/pools/{id}` |
| Bitflow Quotes API | Pool list sanity check | `bff.bitflowapis.finance/api/quotes/v1/pools` |
| Local state file | Snapshot history for trend computation | `~/.hodlmm-pulse-state.json` |

## Known constraints

- `feesUsd1d` and `volumeUsd1d` are 24h rolling windows from Bitflow's API — they update in near-real-time but are not per-minute granularity
- Trend direction requires at least 2 snapshots; `spike` signal is actionable from a single `scan`
- State file is local to the machine — tracking history does not persist across machines
- Low-TVL pools (< $500) are filtered by default; their fee metrics are noisy

## Origin

Winner of AIBTC x Bitflow Skills Pay the Bills competition.
Original author: @ghislo749
Competition PR: https://github.com/BitflowFinance/bff-skills/pull/94
