---
name: trade-karne
description: >
  Trade quality-control scorecard and postmortem analysis. Deterministic, zero-token,
  zero external dependencies. Computes a 3-axis weekly grade (Result 40%, Growth 30%,
  Process 30%) from equity curves and trade logs. Includes 16 risk-adjusted performance
  metrics (Sharpe, Sortino, Calmar, MAR, Ulcer Index, Profit Factor, Expectancy),
  idle-cash penalty detection, and 8-tag deterministic trade postmortems (thesis
  verification, regime violation, sizing errors, premature entries, perfect exits).
  Pure Python stdlib — works with any broker, any ledger format via pluggable data
  adapter. Use when: building a trading quality-control system, setting up anti-stall
  guardrails for a trading pod, implementing a weekly trader scorecard, running
  post-trade analysis, detecting "standing still" (idle cash accumulation) in a
  systematic trading operation, or replacing self-reported P&L with broker-verified
  fill reconciliation. DO NOT USE FOR: live order execution, broker integration,
  real-time risk management, or portfolio optimization.
license: MIT
metadata:
  version: 1.0.0
  category: finance
  tags: [trading, risk-management, performance-attribution, postmortem, scorecard]
---

# Trade-Karne — Deterministic Trading Scorecard

## What This Does

Trade-Karne grades your trading operation with a single weekly score — not just
"did equity go up," but *did you trade well*. It computes a 3-axis Karne (report
card) from your equity curve and trade log:

1. **Result (40%)** — Risk-adjusted return: Sharpe, Sortino, Calmar, max drawdown,
   alpha vs benchmark
2. **Growth (30%)** — Realized trade quality: equity change, profit factor, win rate,
   expectancy, average R-multiple from actual fills
3. **Process (30%)** — Discipline: R:R logging rate, capability progress, lessons
   written — minus penalties for idle cash, blind runs, and consecutive losses

The score is pure math — zero LLM tokens, zero API calls, zero external
dependencies. It reads your existing ledger (SQLite, CSV, or in-memory dicts)
and produces a JSON payload and a human-readable English report.

## When to Use It

Use this skill when you want to:
- Build a trading quality-control system with measurable weekly grades
- Set up anti-stall guardrails that detect "standing still" (idle cash piling up)
- Implement a weekly scorecard across multiple trader books or personas
- Run post-trade analysis with deterministic MAE/MFE and behavioral tagging
- Get an honest assessment of whether your returns are luck or skill

## When NOT to Use

This skill does NOT handle:
- Live order execution or broker integration — it's read-only analysis
- Real-time risk management — it's a weekly/periodic score
- Portfolio optimization or allocation decisions — it measures, doesn't prescribe

## How to Use

### Quick Start (Python API)

```python
from trade_karne import DictDataSource, load_book_input, compute_book_karne, render_report_en

ds = DictDataSource({
    "equity_series": [10000, 10100, 10250, 10400],
    "cash": 1000,
    "hwm": 10400,
    "trade_pnls": [120, -50, 200],
    "trade_rs": [2.0, -1.0, 2.5],
})
inp = load_book_input(ds, "momentum", lessons_count=3)
karne = compute_book_karne(inp)
print(render_report_en(karne, [karne], week="2026-W26", generated_at="today"))
```

### CLI

```bash
trade-karne score --db trades.db --book momentum
trade-karne postmortem --db trades.db --book momentum --out-dir ./reports
trade-karne metrics --list
```

### Plug Into Your Existing System

Implement `TradeDataSource` (7 methods) and pass it to `load_book_input()`. The
Karne never touches your files or DB directly — it only calls those 7 methods.
See `workflows/integration.md` for a step-by-step guide.

## Validation

After running a score:
1. Verify the Process axis — if it's below 40, idle cash or blind runs are dragging
   you down
2. Check the rolling Sharpe trends — a declining trend means skill is degrading
3. Run the postmortem and look for tag clusters (e.g., many `premature_entry` tags
   mean entries need tightening)
4. Compare Result axis across books — large variance means some personas need
   rebalancing or rethinking
