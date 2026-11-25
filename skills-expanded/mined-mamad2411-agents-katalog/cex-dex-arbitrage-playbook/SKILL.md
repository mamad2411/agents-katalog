---
name: cex-dex-arbitrage-playbook
description: "Design cross-venue crypto arb with funding, gas, inventory skew, and atomic/semi-atomic execution constraints."
category: finance
tags: ["crypto", "arbitrage", "DEX", "inventory"]
license: MIT
metadata:
  author: Syntedge Research
  product: Syntedge Skills Library
  locale: [en, ru]
  version: "1.0.0"
---

# SKILL: CEX/DEX Arbitrage Playbook

> **RU:** Плейбук арбитража CEX/DEX - Кросс-веню арб крипто с funding, газом, инвентарём и atomic/semi-atomic исполнением.

## 1. Skill Meta
**Name:** CEX/DEX Arbitrage Playbook
**Description:** Design cross-venue crypto arb with funding, gas, inventory skew, and atomic/semi-atomic execution constraints.
**When to load:** Use this skill whenever the user asks for help with financial research, trading systems, risk, or market-data agents, especially tasks matching: crypto, arbitrage, DEX, inventory.
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
1. A concrete architecture or workflow for **CEX/DEX Arbitrage Playbook** tailored to the user's stack.
2. A step-by-step implementation plan with validation gates.
3. Explicit anti-patterns to refuse or rewrite.
4. A short checklist the agent must pass before claiming done.
5. Sample configs, schemas, or code sketches when they unlock speed (complete, not stubbed).


## 5. Execution Sequence
1. Clarify scope for CEX/DEX Arbitrage Playbook: inputs, outputs, constraints, and success metrics.
2. Inventory existing data, services, and ownership boundaries.
3. Propose the minimal viable architecture that still meets production constraints.
4. Implement in thin vertical slices with tests or evals at each gate.
5. Measure against the success metrics; document residual risks and follow-ups.


## 6. Domain Depth: CEX/DEX Arbitrage Playbook

### Edges
Spot-spot, spot-perp, funding harvest, cross-chain with bridge risk explicit.

### Constraints
Gas, mempool competition, inventory skew, withdrawal delays, oracle lag.

### Safety
Hard caps per venue; kill on RPC degradation; never assume atomicity across custodial CEX.

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
- `crypto`
- `arbitrage`
- `DEX`
- `inventory`

---
*Syntedge Research Skills Library - finance / cex-dex-arbitrage-playbook*
