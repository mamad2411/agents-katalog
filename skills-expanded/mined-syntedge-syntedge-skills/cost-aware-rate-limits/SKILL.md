---
name: cost-aware-rate-limits
description: "Defend APIs and agent endpoints with cost-weighted token buckets and graceful degradation."
category: backend
pack: backend-platform
tags: ["rate-limit", "cost", "API", "agents"]
license: MIT
metadata:
  author: Syntedge Research
  product: Syntedge Backend Platform
  locale: [en, ru]
  version: "1.0.0"
---

# SKILL: Cost-Aware Rate Limits

> **RU:** Cost-aware rate limits - Защита API и agent endpoints: cost-weighted token bucket и graceful degradation.

## 1. Skill Meta
**Name:** Cost-Aware Rate Limits
**Description:** Defend APIs and agent endpoints with cost-weighted token buckets and graceful degradation.
**When to load:** backend tasks matching rate-limit, cost, API, agents.
**Outcomes:** Production-usable plan or implementation with validation gates.

## 2. Core Directive
Senior Syntedge Research practitioner. Prefer falsifiable recommendations. Ask one clarifying question only when critical constraints are missing.

## 3. Operating Protocol
1. Clarify success metrics and constraints.
2. Prefer the smallest architecture that meets production needs.
3. Validate with tests, evals, or desk checks.
4. Document residual risks and owners.
5. Keep outputs complete (no stubs).
6. Redact secrets.

## 4. Required Deliverables
1. Scoped plan for **Cost-Aware Rate Limits**
2. Step-by-step implementation with gates
3. Anti-patterns to refuse
4. Validation checklist
5. Complete configs when they unlock speed

## 5. Execution Sequence
1. Scope inputs/outputs/metrics
2. Inventory existing systems
3. Apply domain method
4. Implement in thin slices
5. Measure and document follow-ups

## 6. Domain Depth: Cost-Aware Rate Limits

### UX
Typed 429 + Retry-After. Degrade features before hard outage.

## 7. Anti-Patterns (Hard Failures)
- Vague advice without metrics
- Skipping validation gates
- Ignoring cost, latency, or safety constraints
- Stubbed incomplete outputs

## 8. Validation Checklist
- [ ] Assumptions stated
- [ ] Success metrics defined
- [ ] Failure modes considered
- [ ] Anti-patterns avoided
- [ ] Output complete
- [ ] Residual risk documented

## 9. Pack Integration
Part of **Syntedge Backend Platform**.

## 10. Reference Vocabulary
- `rate-limit`
- `cost`
- `API`
- `agents`

---
*Syntedge Research - backend-platform / cost-aware-rate-limits*
