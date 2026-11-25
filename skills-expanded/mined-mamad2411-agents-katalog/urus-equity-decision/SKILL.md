---
name: urus-equity-decision
description: Rank Urus Stage 4B watchlist equities and ETFs from paired pre-market/pre-close price, trend, moving-average, relative-strength, MACD, Bollinger, volatility, volume effort/result, and event evidence. Use for SEPA-inspired screening, setup ranking, market-regime checks, and strict JSON equity research decisions. Do not invent missing fundamentals or execute trades.
---

# Urus Equity Decision

Turn paired Urus observations into a compact, evidence-linked watchlist ranking. Use SEPA concepts as a framework while reporting what Urus can and cannot actually evaluate.

## Required references

Read these files before producing a decision:

1. `references/input-contract.md`
2. `references/decision-rules.md`
3. `references/output-contract.md`

## Workflow

1. Confirm `schema_version` is `urus.stage4b_decision_packet.v1`.
2. Stop with `insufficient_data` when quality has blocking errors or usable market and instrument observations are absent.
3. Establish the market and theme regime before ranking symbols. Use SPY, QQQ, SMH, SOXX, and IGV when present; do not assume missing ETF evidence. Compare SMH with SOXX instead of treating one semiconductor ETF as the whole sector.
4. Compare each symbol's pre-market and pre-close observations. Use paired changes as confirmation evidence, not as two independent forecasts.
5. Evaluate trend alignment, 252-day position, relative strength versus QQQ, MACD, Bollinger location, ATR/realized volatility, volume effort/result, and deterministic RSI continuation-versus-reversal context.
6. Check scheduled macro and instrument events. Flag nearby earnings or unresolved results as binary risk.
7. Use the deterministic five-session order-size capital-flow projection only as confirmation. Never equate large orders with institutions or small orders with retail accounts. SMH/SOXX agreement strengthens semiconductor breadth evidence; divergence lowers confidence.
8. Mark strict SEPA completeness as `partial` whenever MA150, EPS, revenue, margins, or other required fundamentals are absent. Never substitute MA100 for MA150 without labeling it an Urus-specific proxy.
9. Rank the watchlist and assign one action from `setup_ready`, `watch`, `observe`, `avoid`, or `insufficient_data`.
10. Return exactly one JSON object matching `references/output-contract.md`, with no Markdown or extra text.

## Guardrails

- Do not place orders or present a ranking as personalized financial advice.
- Do not compare cumulative pre-close volume directly with partial pre-market volume as if the windows were equal.
- Keep stale, mock, partial, and inconsistent evidence in each candidate's `risks`.
- Treat missing fundamentals as `unknown`, not as passing or failing values.
- Use explicit field paths in evidence references so decisions can be audited.
- Prefer low confidence or `insufficient_data` over invented context.
