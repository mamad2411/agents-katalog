---
name: odb-microstructure-forensics
description: Investigate why ODB bars are oversized, have zero duration, or show anomalous price ranges by forensically analyzing Parquet.
allowed-tools: Read, Grep, Glob, Bash
---

# ODB Microstructure Forensics

Systematic methodology for investigating Open Deviation Bar anomalies by tracing from ClickHouse cache back to raw Parquet trade data. Distinguishes algorithm correctness issues from market microstructure phenomena (liquidation cascades, order book sweeps, matching engine batch effects).

> **Self-Evolving Skill**: This skill improves through use. If instructions are wrong, parameters drifted, or a workaround was needed — fix this file immediately, don't defer. Only update for real, reproducible issues.

## When to Use

- ODB bars appear visually larger (taller or wider) than neighbors at the same threshold
- Bars have zero or near-zero duration with extreme price range
- `abs_dev_dbps` exceeds the threshold (e.g., 22 dbps on a 100 dbps bar)
- Clusters of micro-bars appear at a single timestamp
- Diagnosing whether anomalies are data bugs vs market microstructure
- Investigating specific time windows flagged by the Flowsurface chart UI

## Data Sources

| Source             | Location                                                                                | Schema                                                                                    | Access                                                                             |
| ------------------ | --------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------- |
| ClickHouse cache   | `opendeviationbar_cache.open_deviation_bars` on **gpu-host-1**                            | 76 columns, see [schema reference](./references/clickhouse-schema.md)                     | `ssh gpu-host-1 'curl -s http://localhost:8123/ -d "..."'`                           |
| Parquet tick cache | `/home/tca/.cache/opendeviationbar/ticks/{SYMBOL}/{YYYY-MM-DD}.parquet` on **gpu-host-1** | `agg_trade_id, price, quantity, first_trade_id, last_trade_id, timestamp, is_buyer_maker` | `ssh gpu-host-1 'cd /home/tca && uv run --python 3.14 python3 -c "..."'` with Polars |

**Access pattern**: Always query gpu-host-1 directly via SSH. The SSH tunnel (`localhost:18123`) is for the Flowsurface app runtime only — forensic queries go direct.

## Investigation Methodology

The investigation follows a 3-layer drill-down: ClickHouse overview → per-bar anomaly detection → Parquet trade-level root cause.

### Layer 1: ClickHouse Bar Overview

Query bars in the suspect time window. Look for anomaly signals in the result set.

```sql
-- Adjust symbol, threshold, and time window to match the investigation
SELECT
    toDateTime64(close_time_us / 1000000, 3) AS close_ts,
    toDateTime64(open_time_us / 1000000, 3) AS open_ts,
    open, high, low, close,
    round((high - low) / open * 10000, 1) AS range_dbps,
    round(abs(close - open) / open * 10000, 1) AS abs_dev_dbps,
    agg_record_count AS n_agg,
    individual_trade_count AS n_trades,
    round(duration_us / 1e6, 1) AS dur_s,
    first_agg_trade_id AS first_id,
    last_agg_trade_id AS last_id,
    is_orphan, is_liquidation_cascade AS is_liq
FROM opendeviationbar_cache.open_deviation_bars
WHERE symbol = '{SYMBOL}'
  AND threshold_decimal_bps = {THRESHOLD}
  AND close_time_us >= toUnixTimestamp('{START_UTC}', 'UTC') * 1000000
  AND close_time_us <= toUnixTimestamp('{END_UTC}', 'UTC') * 1000000
ORDER BY close_time_us
FORMAT PrettyCompact
```

**Anomaly signals to flag:**

| Signal              | Column Pattern                    | Meaning                                            |
| ------------------- | --------------------------------- | -------------------------------------------------- |
| Threshold overshoot | `abs_dev_dbps >> threshold / 10`  | Single trade crossed beyond threshold              |
| Zero duration       | `dur_s = 0`                       | Entire bar formed within one matching engine cycle |
| Extreme range       | `range_dbps > 2 * threshold / 10` | Price swept far beyond threshold                   |
| Micro trade count   | `n_agg < 10` with high range      | Giant individual fills eating book                 |
| Burst clustering    | Multiple bars at same second      | Liquidity sweep fragmented across bars             |

### Layer 2: Anomaly Isolation

Filter to just the anomalous bars to get agg_trade_id ranges for Parquet drill-down:

```sql
-- Bars with threshold overshoot or zero duration
SELECT close_ts, dur_s, open, high, low, close,
    range_dbps, abs_dev_dbps, n_agg,
    first_agg_trade_id, last_agg_trade_id
FROM (... Layer 1 query ...)
WHERE dur_s < 1.0 OR abs_dev_dbps > {THRESHOLD / 10 * 1.5}
```

Record the `first_agg_trade_id` and `last_agg_trade_id` ranges — these are the Parquet lookup keys.

### Layer 3: Parquet Trade-Level Root Cause

Use Polars on gpu-host-1 to analyze raw trades. Three analyses in sequence:

#### 3a. Timestamp Burst Detection

Group trades by timestamp to find matching engine batches (hundreds of trades sharing exact microsecond):

```python
import polars as pl

df = pl.read_parquet("/home/tca/.cache/opendeviationbar/ticks/{SYMBOL}/{DATE}.parquet")

burst = df.filter(
    (pl.col("agg_trade_id") >= {FIRST_ID}) &
    (pl.col("agg_trade_id") <= {LAST_ID})
).sort("agg_trade_id")

# Group by timestamp to find single-cycle batches
ts_groups = burst.group_by("timestamp").agg([
    pl.col("price").min().alias("min_price"),
    pl.col("price").max().alias("max_price"),
    pl.col("quantity").sum().alias("total_qty"),
    pl.len().alias("count"),
]).sort("timestamp")
```

**Key diagnostic**: If a single timestamp has hundreds of trades spanning the full price range, it is a matching engine batch (single large order sweeping the book).

#### 3b. Order Flow Analysis

Determine whether the sweep is buy or sell dominated:

```python
buys = burst.filter(~pl.col("is_buyer_maker"))   # taker buy
sells = burst.filter(pl.col("is_buyer_maker"))    # taker sell

print(f"Taker buys:  {len(buys)} trades, {buys['quantity'].sum():.4f} BTC")
print(f"Taker sells: {len(sells)} trades, {sells['quantity'].sum():.4f} BTC")
```

Liquidation cascades are typically 95%+ one-sided (all taker sells or all taker buys).

#### 3c. Price Gap Analysis

Find individual trades with large price jumps — these are the direct cause of threshold overshoot:

```python
with_gap = burst.sort("agg_trade_id").with_columns([
    (pl.col("price") - pl.col("price").shift(1)).alias("price_diff"),
    (pl.col("timestamp") - pl.col("timestamp").shift(1)).alias("ts_diff_us"),
])

# Trades with gaps exceeding threshold dollar equivalent
threshold_dollars = open_price * threshold_dbps / 10000
big_jumps = with_gap.filter(pl.col("price_diff").abs() > threshold_dollars)
```

If individual trade-to-trade price gaps exceed the threshold, the ODB algorithm cannot split within a single agg_trade — overshoot is inherent and correct.

## Root Cause Classification

After completing the 3-layer analysis, classify the finding:

| Classification          | Evidence Pattern                                                    | Action                                                         |
| ----------------------- | ------------------------------------------------------------------- | -------------------------------------------------------------- |
| **Liquidation cascade** | 95%+ one-sided, 50-100+ BTC, same-µs timestamp, sweeps $200+        | Oracle bit-exact — no fix needed. Document the event.          |
| **Thin book sweep**     | Fewer trades but large price gaps between levels                    | Oracle bit-exact — book was thin at that moment.               |
| **Orphan bar**          | `is_orphan = 1` in ClickHouse                                       | Known phenomenon — writer-boundary artifact. Skip in analysis. |
| **Algorithm bug**       | Trades are normally distributed, no burst, but bar still overshoots | File upstream issue on opendeviationbar-py.                    |
| **Data gap**            | `agg_trade_id` discontinuity between adjacent bars                  | Missing Parquet data. Check collection pipeline.               |

## Threshold Overshoot Mechanics

The ODB algorithm processes agg_trades sequentially. A bar closes when the first trade deviates beyond the threshold from the bar's open. The overshoot mechanism:

1. Bar opens at price P₀ with threshold T (e.g., 100 dbps = 0.1%)
2. Algorithm scans trades: P₁, P₂, ... Pₙ
3. At trade Pₖ: `|Pₖ - P₀| / P₀ ≥ T` — bar closes at Pₖ
4. If Pₖ₋₁ was within threshold but Pₖ jumps far beyond, overshoot = `|Pₖ - P₀| / P₀ - T`

Overshoot is larger at lower thresholds because:

- BPR10 threshold = $70 on $70k BTC. A $150 order book gap → 2x overshoot.
- BPR50 threshold = $350 on $70k BTC. Same $150 gap → well within threshold.

This is inherent to discrete trade data — not a bug.

## Related Skills

| Skill                                                                | Relationship                                                                               |
| -------------------------------------------------------------------- | ------------------------------------------------------------------------------------------ |
| [opendeviation-eval-metrics](../opendeviation-eval-metrics/SKILL.md) | Evaluates ODB signal quality (output metrics). This skill investigates input data quality. |
| [exchange-session-detector](../exchange-session-detector/SKILL.md)   | Session flags in ClickHouse. Cascades often cluster at session boundaries (NY open/close). |

## Post-Execution Reflection

After this skill completes, check before closing:

1. **Did the queries succeed?** — If ClickHouse schema changed (column renames, new columns), update the Layer 1 SQL template.
2. **Did the Parquet schema change?** — If tick cache columns changed, update the Polars snippets.
3. **Was a new root cause pattern discovered?** — Add it to the Root Cause Classification table with evidence pattern and action.
4. **Did the threshold overshoot mechanics explanation hold?** — If a new overshoot mechanism was found, document it.

Only update if the issue is real and reproducible — not speculative.
