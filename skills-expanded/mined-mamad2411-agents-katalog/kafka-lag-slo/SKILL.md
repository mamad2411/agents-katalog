---
name: kafka-lag-slo
description: "Operate Kafka market feeds with partition strategy, compacted refdata, and consumer lag SLOs."
category: backend
pack: backend-platform
tags: ["Kafka", "lag", "SLO", "feeds"]
license: MIT
metadata:
  author: Syntedge Research
  product: Syntedge Backend Platform
  locale: [en, ru]
  version: "1.0.0"
---

# SKILL: Kafka Lag SLO

> **RU:** SLO по lag Kafka - Kafka market feeds: партиции, compacted refdata и SLO по consumer lag.

## 1. Skill Meta
**Name:** Kafka Lag SLO
**Description:** Operate Kafka market feeds with partition strategy, compacted refdata, and consumer lag SLOs.
**When to load:** backend tasks matching Kafka, lag, SLO, feeds.
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
1. Scoped plan for **Kafka Lag SLO**
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

## 6. Domain Depth: Kafka Lag SLO

### Alert
Burn-rate on lag SLO, not raw lag spikes alone.

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
- `Kafka`
- `lag`
- `SLO`
- `feeds`

---
*Syntedge Research - backend-platform / kafka-lag-slo*
