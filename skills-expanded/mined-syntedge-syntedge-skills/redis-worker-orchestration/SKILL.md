---
name: redis-worker-orchestration
description: "Orchestrate workers with Redis Streams consumer groups, DLQ, claims, and backpressure signals."
category: backend
pack: backend-platform
tags: ["Redis", "streams", "DLQ", "workers"]
license: MIT
metadata:
  author: Syntedge Research
  product: Syntedge Backend Platform
  locale: [en, ru]
  version: "1.0.0"
---

# SKILL: Redis Worker Orchestration

> **RU:** Оркестрация workers на Redis - Workers на Redis Streams: consumer groups, DLQ, claim idle и backpressure.

## 1. Skill Meta
**Name:** Redis Worker Orchestration
**Description:** Orchestrate workers with Redis Streams consumer groups, DLQ, claims, and backpressure signals.
**When to load:** Tasks matching Redis, streams, DLQ, workers in the backend domain.
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
1. Scoped plan for **Redis Worker Orchestration**
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

## 6. Domain Depth: Redis Worker Orchestration

### Pattern
Small payloads; large blobs in object storage with pointers.

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
Part of **Syntedge Backend Platform**. Load sibling pack skills when the task spans related backend workflows.

## 10. Reference Vocabulary
- `Redis`
- `streams`
- `DLQ`
- `workers`

---
*Syntedge Research - backend-platform / redis-worker-orchestration*
