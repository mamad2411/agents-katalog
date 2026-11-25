---
name: on-device-watchdog
description: "Design on-device watchdogs for robotics: heartbeat, safe-stop, model rollback, and thermal cutoffs."
category: physical-ai
pack: physical-ai-lab
tags: ["robotics", "watchdog", "safety", "edge"]
license: MIT
metadata:
  author: Syntedge Research
  product: Syntedge Physical AI Lab
  locale: [en, ru]
  version: "1.0.0"
---

# SKILL: On-Device Watchdog

> **RU:** Watchdog на устройстве - On-device watchdog для роботов: heartbeat, safe-stop, rollback модели и thermal cutoff.

## 1. Skill Meta
**Name:** On-Device Watchdog
**Description:** Design on-device watchdogs for robotics: heartbeat, safe-stop, model rollback, and thermal cutoffs.
**When to load:** physical-ai tasks matching robotics, watchdog, safety, edge.
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
1. Scoped plan for **On-Device Watchdog**
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

## 6. Domain Depth: On-Device Watchdog

### Fail-safe
Hardware stop path independent of the model process.

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
- `robotics`
- `watchdog`
- `safety`
- `edge`

---
*Syntedge Research - physical-ai-lab / on-device-watchdog*
