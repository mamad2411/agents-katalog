---
name: four-pillars
description: Four Pillars Trading Strategy knowledge base. Covers entry signal logic (A/B/C grading), stochastic settings (John Kurisko Raw K), Ripster Cloud numbering, commission math (WEEX rebates), version history (v3.4.1→v3.7.1), SL/TP strategy comparison, and all architectural lessons learned. Triggers on terms like "four pillars", "4 pillars", "entry signal", "A trade", "B trade", "C trade", "commission rebate", "rebate farming", "breakeven raise", "v3.5", "v3.6", "v3.7", "stoch_k", "raw K".
---

# Four Pillars Trading Strategy

## System Overview

The Four Pillars system generates entry signals by aligning 4 pillars:
1. **Price Structure** — Ripster EMA Clouds (trend direction)
2. **Directional Bias** — VWAP / Anchored VWAP (institutional levels)
3. **Momentum** — Quad Rotation Stochastic (4 stochastics, entry timing)
4. **Volatility Filter** — BBWP (squeeze vs expansion)

**Current version:** v3.7.1 — `02-STRATEGY/Indicators/four_pillars_v3_7_1_strategy.pine`

---

## Stochastic Settings (John Kurisko)

**ALL four stochastics use Raw K (K smoothing=1, NO SMA on K line).**

| Name | K Length | Type | Role |
|------|----------|------|------|
| 9-3 | 9 | Raw K | Entry trigger — crosses zone boundary |
| 14-3 | 14 | Raw K | Confirmation |
| 40-3 | 40 | Raw K | Divergence detection |
| 60-10 | 60 | Raw K + D line SMA(10) | Macro filter |

```pinescript
// Raw K function — NO SMA smoothing
stoch_k(int k_len) =>
    float lowest = ta.lowest(low, k_len)
    float highest = ta.highest(high, k_len)
    highest - lowest == 0 ? 50.0 : 100.0 * (close - lowest) / (highest - lowest)

float stoch_9_3      = stoch_k(9)
float stoch_14_3     = stoch_k(14)
float stoch_40_3     = stoch_k(40)
float stoch_60_10    = stoch_k(60)
float stoch_60_10_d  = ta.sma(stoch_60_10, 10)   // D line only
```

**CRITICAL:** v3.5 accidentally applied SMA smoothing to K (used `stoch_fast()`). This delayed signals and missed entries. v3.5.1 reverted to Raw K. NEVER use `stoch_fast()` for Four Pillars.

---

## Ripster Cloud Numbering

| Cloud | EMAs | Role in Four Pillars |
|-------|------|---------------------|
| Cloud 1 | 8/9 | Not used |
| Cloud 2 | 5/12 | Short-term momentum, re-entry trigger |
| Cloud 3 | 34/50 | Medium-term trend, BC filter, price position |
| Cloud 4 | 72/89 | Long-term trend |
| Cloud 5 | 180/200 | Macro trend, not used |

---

## Entry Signal Grading

Signals fire via a 2-stage state machine (Stage 1: 9-3 enters zone → Stage 2: 9-3 exits zone):

| Grade | Requirement | Priority |
|-------|-------------|----------|
| **A** | 4/4 stochastics aligned + Ripster/D filters | Highest — can open and flip |
| **B** | 3/4 stochastics aligned + filters | Medium — can open fresh (if bOpenFresh on) and flip |
| **C** | 9-3 + 14-3 aligned + price above/below Cloud 3 | Lower — can open fresh (if bOpenFresh on) and flip |
| **R** | Cloud 2 re-entry after recent A/B/C signal | Lowest — flat only |

**Priority chain:** A flip > A new > BC flip > BC new/add > Re-entry

### B/C Open Fresh Pattern
When `bOpenFresh` is ON, B and C signals can:
- Open new positions when flat
- Flip direction (cancel stale exits + auto-reverse)

```pinescript
bool enter_long_bc = (long_signal_b or long_signal_c) and
    ((i_bOpenFresh and isFlat) or (not isFlat and posDir == "LONG")) and cooldownOK

bool flip_long_bc = (long_signal_b or long_signal_c) and
    i_bOpenFresh and not isFlat and posDir == "SHORT" and cooldownOK
```

### Cloud 2 Re-entry
Tracks bars since ANY signal (A/B/C), not just A. If price crosses Cloud 2 top/bottom within `reentryLookback` bars of a recent signal, re-enter in that direction.

---

## Commission Model (WEEX)

| Parameter | Value |
|-----------|-------|
| Taker fee | 0.06% per side |
| Margin | $500 cash |
| Leverage | 20x |
| Notional | $10,000 |
| Cost per side | **$6** |
| Round trip | **$12** |
| 70% rebate account | Net $3.60/RT |
| 50% rebate account | Net $6.00/RT |
| Rebate settlement | Daily at 5pm UTC |

### Pine Script Commission Setting
```pinescript
// CORRECT — deterministic, no leverage ambiguity
commission_type=strategy.commission.cash_per_order, commission_value=6

// WRONG — applies % to cash qty ($500), not notional ($10k)
// commission_type=strategy.commission.percent, commission_value=0.06
// This charges $0.30/side instead of $6/side!
```

### Impact on Expectancy

| Scenario | Net comm/RT | Expectancy/trade | Monthly (100 trades) |
|----------|-------------|------------------|----------------------|
| No rebate | $12.00 | $1.81 | $181 |
| 70% rebate | $3.60 | $10.21 | $1,021 |
| 70% rebate + BE raise | $3.60 | ~$34.40 | ~$3,440 |

---

## SL/TP Strategy Comparison

| Strategy | SL Type | TP Type | Best For | Weakness |
|----------|---------|---------|----------|----------|
| **Static ATR (v3.7.1)** | Fixed N×ATR at entry | Fixed N×ATR at entry | Rebate farming, high frequency | No trailing, misses runners |
| **Cloud 3 Trail (v3.5.1)** | Cloud 3 ± 1 ATR, trails | None (trail only) | Trending markets | Activation delay, bleeds in chop |
| **AVWAP Trail (v3.6)** | AVWAP ± max(stdev, ATR) | None (trail only) | Swing trades | stdev=0 on bar 1, barely trails early |
| **Phased (ATR-SL spec)** | Cloud 2→3→4 progression | Phase-based targets | Adaptive to trend strength | Complex, not yet built |

**Key finding:** 86% of losing trades saw unrealized profit before dying. Signal quality is fine — exit timing is the bottleneck. Trailing stops bleed in choppy markets. Breakeven+$X raise is the primary optimization target.

---

## v3.7.1 Architecture (Current)

- **Goal:** ~3000 trades/month, flat equity, commission rebates = profit
- **SL/TP:** 1.0 ATR SL, 1.5 ATR TP (fixed at entry, no trailing)
- **pyramiding=1:** One position at a time, fast turnover
- **Cooldown:** 3 bars minimum between entries
- **Flips:** `strategy.entry()` auto-reverses (no `strategy.close_all()`)
- **Stale exits:** `strategy.cancel()` before every flip
- **Commission:** `cash_per_order=6` (deterministic)

---

## Version History

| Version | SL Type | Commission | Key Change | Outcome |
|---------|---------|------------|------------|---------|
| v3.4.1 | 2.0 ATR static | percent 0.1% | Baseline | Marginally profitable |
| v3.5 | 2.0 ATR static | percent 0.1% | Added stochastic smoothing (bug) | Missed signals |
| v3.5.1 | Cloud 3 ± 1 ATR trail | percent 0.1% | Fixed Raw K, added trail | Bled out in chop |
| v3.6 | AVWAP ± stdev trail | percent 0.1% | AVWAP stops, separate order IDs | stdev=0 bug, bled out |
| v3.7 | 1.0 ATR static | percent 0.06% | Rebate farming, B/C fresh, free flips | Commission blow-up (phantom trades) |
| v3.7.1 | 1.0 ATR static | cash_per_order=6 | Fixed commission, cooldown, no close_all | Current — $1.81/trade |

---

## Lessons Learned

### 1. Commission: percent vs cash_per_order
`commission.percent` applies to CASH qty, not notional. With 20x leverage on $500 ($10k notional), 0.06% charges $0.30/side instead of $6. Use `cash_per_order=6` always.

### 2. Phantom Trade Bug
`strategy.close_all()` + `strategy.entry()` on same bar = 2 trades (close + new entry). Doubles commission on every flip. Fix: only `strategy.entry()` in opposite direction (auto-reverses). Always `strategy.cancel()` stale exits first.

### 3. Stochastic K Smoothing Regression
v3.5 used `stoch_fast()` which applies SMA to K. Four Pillars needs Raw K (smooth=1). v3.5.1 reverted to `stoch_k()`. Never use SMA-smoothed K for entry detection.

### 4. AVWAP stdev=0 on Bar 1
After anchor reset, stdev is 0 (one data point). Creates near-zero SL distance. Floor with `math.max(stdev, atr)`.

### 5. Trail Activation Delay
Cloud 3/4 trail (v3.5.1) and AVWAP trail (v3.6) both bleed in choppy markets. The trail doesn't protect early enough, and losers run to full SL. Tight symmetric SL/TP is better for rebate farming.

### 6. 86% of Losers Saw Green
Signal quality is fine. The problem is exit timing. Breakeven+$X raise converts these to small wins instead of full SL losses. Primary optimization target.

### 7. entryBar Must Persist Through Exit
If cooldown `entryBar` resets on exit, cooldown gate bypasses immediately. Do NOT reset in state sync block.

---

## Key Market Dates for Testing

| Date | Event | Expected Behavior |
|------|-------|-------------------|
| Nov 11 | Favorable conditions | Bot should profit |
| Dec 15 | BTC dump | Stress test — rapid shorts |
| Jan 15+ | Bearish grind | Chop, reduced win rate |
| Feb 4 | BTC dump | Stress test — rapid shorts |

---

## Key Files

| File | Purpose |
|------|---------|
| `02-STRATEGY/Indicators/four_pillars_v3_7_1_strategy.pine` | Current strategy (source of truth) |
| `02-STRATEGY/Indicators/four_pillars_v3_6.pine` | Current indicator |
| `02-STRATEGY/Indicators/four_pillars_v3_5_1_strategy.pine` | v3.5.1 (cloud trail exit) |
| `02-STRATEGY/Indicators/four_pillars_v3_6_strategy.pine` | v3.6 (AVWAP trail exit) |
| `02-STRATEGY/Indicators/ATR-SL-MOVEMENT-BUILD-GUIDANCE.md` | Phased SL/TP spec (not yet built) |
| `07-TEMPLATES/4Pv3.4.1-S_BYBIT_MEMEUSDT.P_2026-02-06_fcc84.csv` | Validation trade data |
