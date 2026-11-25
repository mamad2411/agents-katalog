---
name: drawdown-circuit-breaker
description: Use this skill to apply a mechanical drawdown-based risk gate — reduce or halt new position-taking after account equity falls a defined percentage from its peak. Trigger on "drawdown limit", "circuit breaker", "stop trading after a losing streak", "reduce size after a drawdown", "risk gate". Pairs with [position-sizer](../position-sizer/SKILL.md), which the gate's size_multiplier is meant to scale.
---

# Drawdown Circuit Breaker

## Overview

Deciding "should I cut my size after a rough stretch?" in the moment is a documented weak point — loss-averse or revenge-trading decisions tend to be worse than a rule set in advance while calm. This skill applies a pre-committed, mechanical rule: given account equity's peak and current value, it returns whether new positions should be full-size, reduced, or halted.

**Not financial advice.** This is a mechanical rule over numbers you supply, not a prediction that further decline is or isn't coming.

## When to use

- ตั้งกฎลดขนาดโพซิชันหรือหยุดเทรดชั่วคราวเมื่อพอร์ตขาดทุนถึงระดับที่กำหนด
- Checking whether current account drawdown crosses a pre-defined threshold
- Deciding the size multiplier to apply to [position-sizer](../position-sizer/SKILL.md)'s output after a losing stretch

## When NOT to use

- The user wants a market-timing signal (predicting further decline) — this is a risk-management rule about the user's own account state, not a market forecast
- No peak-equity/current-equity tracking exists yet — this skill needs those two numbers; if the user doesn't track equity curve, that's a prerequisite to set up first (see [trader-memory-core](../trader-memory-core/SKILL.md))

## Core knowledge

**Drawdown**: `(peak_equity - current_equity) / peak_equity × 100`. If current equity is a new high, drawdown is 0, not negative — a circuit breaker only cares about decline from the high-water mark.

**Default illustrative thresholds** (starting point, not a validated rule — tune to the user's own risk tolerance and strategy history):

| Drawdown | Action | Size multiplier |
|---|---|---|
| < 10% | Full size | 1.0× |
| 10-14.9% | Reduced size | 0.5× |
| ≥ 15% | Halt new positions | 0× |

When multiple thresholds are crossed, the **most severe** governs (an 18% drawdown triggers "halt," not "reduced," even though it also crosses the 10% threshold).

**Why mechanical rules over judgment calls**: the entire point of a circuit breaker is that the threshold and response are decided *before* the emotionally difficult moment, not during it — a rule that gets overridden in the moment provides none of its intended benefit.

## Common mistakes

1. Treating the "halt" trigger as a market call ("the market is going down") rather than an account-state rule ("my own risk budget for new bets just changed").
2. Overriding the gate in the moment because "this setup looks too good to skip" — that defeats the purpose of a pre-committed rule.
3. Setting thresholds so tight that normal volatility triggers "halt" constantly (rule becomes noise) or so loose that it never fires (rule provides no protection) — thresholds should be calibrated against the strategy's own historical drawdown distribution, not copied from this skill's illustrative defaults unexamined.
4. Computing drawdown from an average or arbitrary equity value instead of the actual peak (high-water mark) — the peak must be tracked continuously, not re-estimated each time.

## Code

`gate.py` — pure Decimal arithmetic, no dependencies:

- `compute_drawdown_pct(peak_equity, current_equity)` → Decimal percentage, floored at 0
- `evaluate_drawdown_gate(peak_equity, current_equity, thresholds=DEFAULT_THRESHOLDS)` → `GateResult(drawdown_pct, action, size_multiplier)`
- `DEFAULT_THRESHOLDS` — the illustrative table above, override with your own tuned thresholds

Run `python3 gate.py` for the self-test.

## Known limitations

- Default thresholds are illustrative starting points, explicitly not validated against any specific strategy's real drawdown history — replace them before relying on this for real account decisions.
- Does not track equity history itself; the caller must supply an accurate peak-equity (high-water mark) figure.
- A rule this simple ignores context (e.g., a drawdown driven by one outlier loss vs. a genuine losing streak) — it's a blunt, deliberately mechanical instrument, not a nuanced risk model.
