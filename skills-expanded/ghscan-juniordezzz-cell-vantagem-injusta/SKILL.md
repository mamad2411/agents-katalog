---
name: rwa-nav-dislocation
description: Research and trading framework for Real World Asset (RWA) token NAV dislocation opportunities. Covers mechanisms causing token price to diverge from underlying net asset value, detection methods, and arbitrage strategies.
---

# RWA NAV Dislocation Research Framework

## Overview

Real World Asset (RWA) tokens tokenize traditional financial assets (bonds, real estate, commodities) onto blockchain. The token price should track the underlying asset's Net Asset Value (NAV), but market forces create dislocations — opportunities for arbitrage.

## Key Concepts to Research

1. **NAV Calculation** — How protocols compute per-token NAV from underlying assets
2. **Dislocation Mechanisms** — Liquidity constraints, redemption premiums/discounts, market sentiment, yield distribution dynamics
3. **Detection Signals** — Price vs NAV divergence, trading volume spikes, liquidity depth analysis
4. **Arbitrage Strategies** — Converge trade, yield farming carry, redemption arbitrage
5. **Risk Factors** — Smart contract risk, asset illiquidity, regulatory risk, oracle manipulation

## Research Questions

- What is the mathematical model for NAV dislocation detection?
- Which protocols exhibit the most consistent dislocation patterns?
- How does protocol design (lockups, fees, redemption windows) affect dislocation depth?
- What are the key leading indicators of dislocation widening/narrowing?

## Output Structure

This skill produces research structured across:
- `research.md` — Distilled concepts and findings
- `formulas.md` — Mathematical models and formulas
- `sources.md` — Curated references
- `backtesting/` — Strategy simulation logs

## Application to Genesis Protocol

This research feeds:
- **Pillar 3 (HOLD)**: Identifying RWA tokens trading below fair value for accumulation
- **Pillar 4 (RWA Study)**: Fundamental analysis of protocol mechanics and NAV calculation
- **Dashboard**: Real-time dislocation monitoring widgets
