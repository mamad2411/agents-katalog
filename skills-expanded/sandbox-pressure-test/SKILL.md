---
name: sandbox-pressure-test
title: Sandbox Pressure Testing Protocol
description: Pre-live stress test methodology — 100-trade worst-case simulation with 2.5x volatility
version: 1.0.0
type: reference
status: active
created: 2026-05-18
category: devops
license: MIT
tested: schema-only
tested_note: Protocol document only; no runtime validation claimed by this repo.
tags:
  - sandbox
  - pressure-test
  - stress-test
  - pre-live
  - risk-management
---

# Sandbox Pressure Testing

## Purpose
Validate strategy robustness before live deployment by simulating worst-case market conditions at scale.

## Passing Criteria
| Metric | Threshold | Rationale |
|--------|-----------|-----------|
| Survival | Balance > $1,000 | Must retain >10% capital |
| Max Drawdown | < 20% | Live tolerance for worst-case streak |
| Fitness Score | > 80% | Ending balance > 80% of starting |

## Results (May 18, 2026)
```
100 trades | 40% WR | $10,036.79 final | 3.57% max DD | SURVIVED ✅
```

## Parameters
- Volatility multiplier: 2.5x normal
- Leverage range: 3x–10x (random)
- Stop-loss: 3% enforced
- Risk per trade: 2%
- Entry signals: randomized (no strategy edge — pure stress)
