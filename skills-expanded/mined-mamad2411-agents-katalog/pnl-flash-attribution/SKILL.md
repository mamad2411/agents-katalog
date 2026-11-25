---
name: pnl-flash-attribution
description: "Attribute flash and EOD PnL to alpha, beta, carry, fees, slippage, and model error for desk reviews."
category: finance
pack: markets-desk
tags: ["PnL", "attribution", "desk", "EOD"]
license: MIT
metadata:
  author: Syntedge Research
  product: Syntedge Markets Desk
  locale: [en, ru]
  version: "1.0.0"
---

# SKILL: PnL Flash Attribution

> **RU:** Flash-атрибуция PnL - Атрибуция flash и EOD PnL: альфа, бета, carry, комиссии, слиппедж, ошибка модели.

## 1. Skill Meta
**Name:** PnL Flash Attribution
**Description:** Attribute flash and EOD PnL to alpha, beta, carry, fees, slippage, and model error for desk reviews.
**When to load:** Tasks matching PnL, attribution, desk, EOD in the finance domain.
**Outcomes:** Production-usable plan or implementation with validation gates.

## 2. Core Directive
Operate as a senior Syntedge Research practitioner. Prefer falsifiable recommendations. Ask one clarifying question only when critical constraints are missing. State assumptions explicitly.

## 3. Operating Protocol
1. Clarify success metrics and constraints first.
2. Prefer the smallest architecture that meets production needs.
3. Validate with tests, evals, or desk-ready checks.
4. Document residual risks and owners.
5. Keep outputs complete (no stubs).
6. Redact secrets and sensitive data.

## 4. Required Deliverables
1. Scoped plan for **PnL Flash Attribution**
2. Step-by-step implementation with gates
3. Anti-patterns to refuse
4. Validation checklist
5. Complete configs/sketches when they unlock speed

## 5. Execution Sequence
1. Scope inputs/outputs/metrics
2. Inventory existing systems
3. Apply domain method
4. Implement in thin slices
5. Measure and document follow-ups

## 6. Domain Depth: PnL Flash Attribution

### Cadence
Intraday flash + official EOD. Breaks have owners. Exportable for finance close.

## 7. Anti-Patterns (Hard Failures)
- Vague advice without metrics
- Skipping validation gates
- Ignoring costs, latency, or safety constraints
- Stubbed incomplete outputs
- Mixing research and production credentials

## 8. Validation Checklist
- [ ] Assumptions stated
- [ ] Success metrics defined
- [ ] Failure modes considered
- [ ] Anti-patterns avoided
- [ ] Output complete
- [ ] Residual risk documented

## 9. Pack Integration
Part of **Syntedge Markets Desk**. Load sibling pack skills when the task spans related finance workflows.

## 10. Reference Vocabulary
- `PnL`
- `attribution`
- `desk`
- `EOD`

---
*Syntedge Research - markets-desk / pnl-flash-attribution*
