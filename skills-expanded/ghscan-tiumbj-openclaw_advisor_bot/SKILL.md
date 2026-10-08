---
name: regime-classification
description: Classify current XAUUSD market regime (trending, ranging, breakout, volatile) for strategy context.
version: 1.2.15
owner_agent: intermarket-macro-agent
purpose: Label market regime from Python-computed indicators to guide strategy selection.
allowed_inputs:
  - evidence packet (multi-timeframe OHLC + macro context)
required_input_schema: object
output_schema: object
allowed_tools:
  - read
  - session_status
denied_tools:
  - group:runtime
  - group:web
  - group:ui
  - group:automation
  - group:messaging
  - group:plugins
  - group:memory
  - group:sessions
  - write
  - edit
  - apply_patch
  - exec
  - process
  - code_execution
  - browser
  - canvas
  - gateway
  - message
  - subagents
safety_constraints:
  - advisor-only
  - no secret access
  - no execution
failure_behavior: return REGIME_UNKNOWN if insufficient data
audit_fields:
  - evidence_id
  - regime_label
  - atr_value
  - trend_strength
  - regime_confidence
tests:
  - unit
  - integration
promotion_status: stable
---
# regime-classification

## Procedure
1. Receive ATR, ADX, and range_pct from Python evidence packet
2. Apply classification rules:
   - ADX > 25 and directional DI aligned → TRENDING
   - ADX < 20 and range_pct < 0.5% on H1 → RANGING
   - ATR spike > 2× 20-day ATR → VOLATILE
   - Price close outside H4 range with volume expansion → BREAKOUT
3. Attach regime_label, regime_confidence, and supporting numerics to evidence

## Decision Tree
- ADX and ATR present → classify regime
- Only ATR available → classify VOLATILE vs non-volatile only
- No indicator data → REGIME_UNKNOWN (proceed but disable strategy-specific scoring)

## Quality Gates
- ATR and ADX must come from Python MT5 adapter with timeframe declared
- Agent cannot compute ATR/ADX from raw OHLC in its reasoning

## Failure Modes
- MT5 indicator history too short (<14 periods) → REGIME_UNKNOWN
- Transition period (regime just changed): confidence=LOW, attach transition flag
