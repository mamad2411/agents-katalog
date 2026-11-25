---
name: dataset-drift-monitor
description: "Monitor production vision drift: embedding shifts, label skew, and retraining triggers."
category: physical-ai
pack: physical-ai-lab
tags: ["drift", "monitoring", "CV", "retrain"]
license: MIT
metadata:
  author: Syntedge Research
  product: Syntedge Physical AI Lab
  locale: [en, ru]
  version: "1.0.0"
---

# SKILL: Dataset Drift Monitor

> **RU:** Мониторинг drift датасета - Мониторинг drift vision в prod: сдвиги эмбеддингов, label skew и триггеры retrain.

## 1. Skill Meta
**Name:** Dataset Drift Monitor
**Description:** Monitor production vision drift: embedding shifts, label skew, and retraining triggers.
**When to load:** physical-ai tasks matching drift, monitoring, CV, retrain.
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
1. Scoped plan for **Dataset Drift Monitor**
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

## 6. Domain Depth: Dataset Drift Monitor

### Alert
Slice metrics falling below promotion baseline.

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
Part of **Syntedge Physical AI Lab**.

## 10. Reference Vocabulary
- `drift`
- `monitoring`
- `CV`
- `retrain`

---
*Syntedge Research - physical-ai-lab / dataset-drift-monitor*
