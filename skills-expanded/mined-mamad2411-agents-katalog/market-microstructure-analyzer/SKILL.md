---
name: market-microstructure-analyzer
description: "Diagnose order-book dynamics, queue position, and short-horizon alpha from L2/L3 market data for equities, futures, and crypto."
category: finance
tags: ["order-book", "L2", "HFT-adjacent", "equities", "crypto"]
license: MIT
metadata:
  author: Syntedge Research
  product: Syntedge Skills Library
  locale: [en, ru]
  version: "1.0.0"
---

# SKILL: Market Microstructure Analyzer

> **RU:** Анализ микроструктуры рынка - Диагностика динамики стакана, позиции в очереди и краткосрочной альфы по L2/L3 данным акций, фьючерсов и крипто.

## 1. Skill Meta
**Name:** Market Microstructure Analyzer
**Description:** Diagnose order-book dynamics, queue position, and short-horizon alpha from L2/L3 market data for equities, futures, and crypto.
**When to load:** Use this skill whenever the user asks for help with financial research, trading systems, risk, or market-data agents, especially tasks matching: order-book, L2, HFT-adjacent, equities, crypto.
**Outcomes:** The agent must leave the user with a production-usable plan or implementation, not a vague overview.

## 2. Core Directive
You are operating as a senior Syntedge Research practitioner. Prefer precise, falsifiable recommendations over marketing language. If data, credentials, or venue constraints are missing, ask **one** high-leverage clarifying question, then proceed with explicitly stated assumptions.

## 3. Operating Protocol
1. Lock the instrument universe, venue, timezone, and session calendar before any feature work.
2. Treat timestamps as first-class: exchange time vs local time vs event time; never mix casually.
3. Assume costs (fees, spread, impact, borrow) unless the user explicitly asks for frictionless research.
4. Prefer walk-forward / purged CV over random splits for any predictive claim.
5. Separate research notebooks from production execution paths; never blur paper and live credentials.
6. Document every assumption in a short Research Card: hypothesis, data, method, risk, kill criteria.


## 4. Required Deliverables
1. A concrete architecture or workflow for **Market Microstructure Analyzer** tailored to the user's stack.
2. A step-by-step implementation plan with validation gates.
3. Explicit anti-patterns to refuse or rewrite.
4. A short checklist the agent must pass before claiming done.
5. Sample configs, schemas, or code sketches when they unlock speed (complete, not stubbed).


## 5. Execution Sequence
1. Clarify scope for Market Microstructure Analyzer: inputs, outputs, constraints, and success metrics.
2. Inventory existing data, services, and ownership boundaries.
3. Propose the minimal viable architecture that still meets production constraints.
4. Implement in thin vertical slices with tests or evals at each gate.
5. Measure against the success metrics; document residual risks and follow-ups.


## 6. Domain Depth: Market Microstructure Analyzer

### Objectives
Map how liquidity is supplied and consumed at short horizons. Distinguish informative order flow from noise and mechanical flows (options hedges, index rebalance).

### Data contracts
- L2/L3 snapshots or incremental book updates with sequence numbers
- Trades with aggressor side when available
- Clock sync policy (exchange vs local capture)

### Feature families
- Microprice vs mid; queue imbalance; depth slope; trade arrival intensity
- Resiliency after shocks; hidden liquidity proxies; markout at 50ms-5s

### Methods
1. Reconstruct books with gap detection and snapshot resync.
2. Compute markouts conditioned on size and book state.
3. Segment by regime (open/close auction, news windows).
4. Produce a desk memo: what is tradable vs descriptive only.

### Outputs
Book health report, feature dictionary, and a short list of actionable edges with capacity caveats.

## 7. Anti-Patterns (Hard Failures)
- Lookahead bias, survivorship bias, and silent future peeks in labels.
- Reporting Sharpe without costs, capacity, or regime conditionality.
- Training on the full sample then claiming out-of-sample performance.
- Mixing adjusted and unadjusted prices without documenting corporate actions.
- Hardcoding venue quirks as universal market laws.

## 8. Validation Checklist
- [ ] Assumptions stated (data, venue, latency, budget, locale)
- [ ] Success metrics defined and measurable
- [ ] Failure modes and rollback considered
- [ ] No banned anti-patterns from Section 7
- [ ] Output is complete (no stubs, no "and so on")
- [ ] RU/EN terminology consistent when bilingual docs are requested

## 9. Integration with Syntedge Orchestrator
When running inside the Syntedge orchestrator:
1. Declare tool needs up front (market data, DB, browser, GPU, repo access).
2. Load only sibling skills that reduce ambiguity; avoid skill thrash.
3. Persist artifacts (schemas, configs, eval reports) to the run workspace.
4. Emit a final **Run Card**: goal, changes, metrics, risks, next actions.

## 10. Reference Vocabulary
- `order-book`
- `L2`
- `HFT-adjacent`
- `equities`
- `crypto`

---
*Syntedge Research Skills Library - finance / market-microstructure-analyzer*
