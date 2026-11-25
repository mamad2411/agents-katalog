---
name: exposure-coach
description: Use this skill to combine market breadth, uptrend participation, and account drawdown state into one summarized "how much new risk does today support" exposure ceiling. Trigger on "market posture", "exposure coach", "how much risk should I take today", "should I add new positions". Requires the outputs of [market-breadth-analyzer](../market-breadth-analyzer/SKILL.md), [uptrend-analyzer](../uptrend-analyzer/SKILL.md), and optionally [drawdown-circuit-breaker](../drawdown-circuit-breaker/SKILL.md) — this skill aggregates, it doesn't compute those inputs itself.
---

# Exposure Coach

## Overview

A daily market check produces several separate numbers (breadth %, uptrend %, account drawdown state) — this skill combines them into one plain-language read: how much new risk today's conditions support. It's the synthesis step at the end of a market-regime check, not a replacement for the individual skills that feed it.

**Not financial advice.** This is one configurable heuristic for summarizing market conditions plus your own account's risk state — not a signal to act on mechanically, and not a substitute for judgment about the specific setup in front of you.

## When to use

- สรุปภาพรวมตลาดหลังเช็ค breadth และ uptrend แล้ว ว่าวันนี้ควร "เปิดรับความเสี่ยงใหม่" มากแค่ไหน
- Combining a market-regime read with the account's own drawdown state into one exposure-ceiling recommendation
- The synthesis step of a daily/weekly market check (after running market-breadth-analyzer and uptrend-analyzer)

## When NOT to use

- Breadth/uptrend numbers haven't been computed yet — run those skills first; this skill has nothing to combine without them
- The user wants a signal for one specific stock — this is a market-wide/account-wide posture read, not a single-name call

## Core knowledge

**Priority rule**: the account's own drawdown state always overrides a favorable market read. A "halt_new_positions" drawdown-gate state produces a "minimal" exposure ceiling regardless of how strong breadth/uptrend look — a personal risk rule isn't meant to be overridden by good market conditions. A "reduced_size" gate state caps the market-derived ceiling one notch lower.

**Market-derived ceiling** (before any drawdown adjustment):

| Breadth % | Uptrend % | Ceiling |
|---|---|---|
| ≥ 60% | ≥ 50% | High |
| ≥ 40% | ≥ 30% | Moderate |
| below both | — | Low |

These thresholds are a starting heuristic, not a validated model — like the individual skills feeding it, tune them against the user's own strategy history rather than treating them as fixed truth.

## Common mistakes

1. Treating "high exposure ceiling" as "take every setup available" — it means the market backdrop doesn't argue against new risk, not that any specific trade is good.
2. Letting a favorable market read override an active drawdown-gate halt — the priority order matters and is intentional (see Core knowledge).
3. Running this skill with stale or mismatched-date breadth/uptrend inputs — the synthesis is only as current as its inputs.
4. Treating the ceiling as a percentage of capital to deploy — it's a qualitative posture label (high/moderate/low/minimal), not a sizing formula; use [position-sizer](../position-sizer/SKILL.md) for the actual per-trade math.

## Code

`posture.py` — pure logic, no dependencies:

- `evaluate_posture(breadth_pct, uptrend_pct, drawdown_action="full_size")` → `PostureResult(exposure_ceiling, reasons)`

Run `python3 posture.py` for the self-test.

## Known limitations

- Thresholds are illustrative defaults, not calibrated against any specific strategy or universe — recalibrate before relying on them.
- Only combines the three inputs listed — doesn't account for other regime signals (volatility index level, sector rotation, macro calendar) a fuller market-regime process might use.
- This is a rule-based summary, not a probabilistic forecast — it describes current conditions, not future returns.
