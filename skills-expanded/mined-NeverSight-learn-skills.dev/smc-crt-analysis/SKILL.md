---
name: smc-crt-analysis
description: Analyze any asset (stocks, crypto, forex) using Smart Money Concepts (SMC) and Candle Range Theory (CRT). Use when the user asks for technical analysis, market structure analysis, liquidity analysis, order block identification, or price action reading. Triggers include "SMC analysis", "CRT analysis", "market structure", "order blocks", "liquidity sweep", "break of structure", "change of character", "fair value gap", "imbalance", "premium/discount", "smart money", "institutional flow", "POI", "sniper entry", "turtle soup", "where is smart money", "Wyckoff", "Elliott Wave", or any request to analyze price charts using institutional order flow concepts. Also triggers when analyzing entry/exit points, stop loss placement, or identifying manipulation patterns on any timeframe.
license: MIT
metadata:
  author: arraydude
  version: "1.0.0"
---

# SMC + CRT Analysis Framework

Multi-timeframe institutional order flow analysis. Follow this top-down protocol for every analysis.

## Rule Categories by Priority

| Priority | Category | Impact | Prefix |
|----------|----------|--------|--------|
| 1 | Market Structure | CRITICAL | `structure-` |
| 2 | Liquidity Mapping | CRITICAL | `liquidity-` |
| 3 | Order Blocks & POIs | HIGH | `orderblock-` |
| 4 | Premium / Discount | HIGH | `premium-discount-` |
| 5 | CRT (Candle Range Theory) | CRITICAL | `crt-` |
| 6 | SMT Divergence | MEDIUM | `smt-` |
| 7 | Time & Price | MEDIUM | `time-` |
| 8 | IPDA Cycles | MEDIUM | `ipda-` |
| 9 | Risk Management | HIGH | `risk-` |

## Quick Reference

### 1. Market Structure (CRITICAL)

- `structure-identification` - HTF to LTF trend identification with BOS/CDC/CHoCH
- `structure-strong-weak-points` - Identify strong lows and weak highs

### 2. Liquidity Mapping (CRITICAL)

- `liquidity-mapping` - Map BSL, SSL, IRL, ERL before identifying POIs
- `liquidity-inducement` - Recognize false BOS and retail traps
- `liquidity-killzones` - Best session times for trading

### 3. Order Blocks & POIs (HIGH)

- `orderblock-validation` - Three requirements: momentum, imbalance, location
- `orderblock-poi-hierarchy` - Extremo vs Decisional POI classification

### 4. Premium / Discount (HIGH)

- `premium-discount-zones` - Divide range at 50% for buy/sell zones

### 5. CRT - Candle Range Theory (CRITICAL)

- `crt-cycle` - Reference candle, manipulation, expansion protocol
- `crt-range-types` - Intra TS, Pendiente, Reiniciada, Previa, Completada
- `crt-pdm` - Punto de Máxima Decisión validation sequence
- `crt-fractal-execution` - H4 direction, M15 trap, M1 entry
- `crt-double-liquidity-sweep` - Wait for two sweeps, enter after second

### 6. SMT Divergence (MEDIUM)

- `smt-divergence` - Correlated asset comparison for manipulation confirmation

### 7. Time & Price (MEDIUM)

- `time-price-alignment` - Timeframe hierarchy and session timing

### 8. IPDA Cycles (MEDIUM)

- `ipda-cycles` - 20-40-60 day rebalancing windows

### 9. Risk Management (HIGH)

- `risk-management` - Position sizing, max losses, minimum R:R

## Output Format

Structure every SMC+CRT analysis as:

1. **HTF Structure** — Current trend, BOS/CDC levels
2. **Liquidity Map** — BSL/SSL pools, EQH/EQL, inducement
3. **Key POIs** — OBs validated with momentum + imbalance + location
4. **Premium/Discount** — Position within range
5. **CRT Reading** — Recent candle range setups, sweep status
6. **SMT Check** — Correlated asset divergence
7. **Bias + Levels** — Direction, entry, SL, TP

## Core Mental Model

1. **Top-down analysis** — Always start from HTF, drill down to LTF
2. **Liquidity first** — Map all liquidity BEFORE identifying POIs
3. **Smart money leaves footprints** — OBs, FVGs, and sweeps reveal institutional intent
4. **Wait for confirmation** — Double sweep + SMT + rejection, not single signals

## Full Compiled Document

For the complete guide with all rules expanded: `AGENTS.md`
