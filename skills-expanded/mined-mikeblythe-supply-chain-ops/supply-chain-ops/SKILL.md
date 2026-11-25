---
name: supply-chain-ops
description: >
  Real inventory and supply-chain operations math for small-to-mid-size businesses:
  Economic Order Quantity (EOQ), reorder point and safety stock calculation, ABC
  inventory classification, and simple demand forecasting (moving average / exponential
  smoothing). Every formula is standard, textbook operations management — not invented —
  and every result shows its work. Use when the user asks how much to order, when to
  reorder, which inventory items matter most, or wants a demand forecast from historical
  sales/usage data.
allowed-tools: Read, Write, Bash
---

# Supply Chain Ops

Four independent tools, all standard operations-research formulas (cited in
`reference/formulas.md`), none invented for this skill.

## 1. Economic Order Quantity (`scripts/eoq.py`)

The order quantity that minimizes total ordering + holding cost.

```bash
python3 scripts/eoq.py --annual-demand 12000 --order-cost 75 --holding-cost 3.50
```

## 2. Reorder point & safety stock (`scripts/reorder_point.py`)

When to place the next order, accounting for demand variability and lead time —
not just "average usage × lead time," which ignores the risk of stocking out during
an unusually fast-selling or slow-shipping stretch.

```bash
python3 scripts/reorder_point.py --avg-daily-demand 40 --max-daily-demand 65 \
  --avg-lead-time-days 7 --max-lead-time-days 12
```

## 3. ABC inventory classification (`scripts/abc_analysis.py`)

Ranks a CSV of items by annual dollar usage and classifies into A (top ~80% of value,
usually a small fraction of items), B (next ~15%), C (bottom ~5%) — the standard
Pareto-based approach to deciding what deserves tight inventory control vs. what doesn't.

```bash
python3 scripts/abc_analysis.py --csv items.csv
# CSV needs columns: item_id,annual_units,unit_cost
```

## 4. Demand forecast (`scripts/demand_forecast.py`)

Simple moving average and exponential smoothing from a column of historical period
demand — no ML, no black box, both are standard, auditable forecasting methods you
can sanity-check by hand.

```bash
python3 scripts/demand_forecast.py --csv sales_history.csv --method both --periods-ahead 3
# CSV needs a single column: demand (one row per period, oldest first)
```

## Honesty rules for this skill

- Every number shown, no hidden intermediate steps — a result should be verifiable by hand.
- Safety stock and reorder point use the actual demand/lead-time variability the user
  provides, not a made-up buffer percentage.
- Demand forecasts are only as good as the history given — with fewer than 3-4 periods
  of data, the tool says so rather than presenting a confident-looking number.
