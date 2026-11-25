---
name: web-vitals-gate
description: "Enforce LCP/INP/CLS budgets with image strategy, font loading, RUM, and CI regression gates."
category: frontend
pack: frontend-systems
tags: ["LCP", "INP", "CLS", "RUM"]
license: MIT
metadata:
  author: Syntedge Research
  product: Syntedge Frontend Systems
  locale: [en, ru]
  version: "1.0.0"
---

# SKILL: Web Vitals Gate

> **RU:** Гейт Web Vitals - Бюджеты LCP/INP/CLS: изображения, шрифты, RUM и CI regression gates.

## 1. Skill Meta
**Name:** Web Vitals Gate
**Description:** Enforce LCP/INP/CLS budgets with image strategy, font loading, RUM, and CI regression gates.
**When to load:** Tasks matching LCP, INP, CLS, RUM in the frontend domain.
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
1. Scoped plan for **Web Vitals Gate**
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

## 6. Domain Depth: Web Vitals Gate

### Targets
LCP < 2.5s, INP < 200ms, CLS < 0.1. Fail CI on p75 regressions.

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
Part of **Syntedge Frontend Systems**. Load sibling pack skills when the task spans related frontend workflows.

## 10. Reference Vocabulary
- `LCP`
- `INP`
- `CLS`
- `RUM`

---
*Syntedge Research - frontend-systems / web-vitals-gate*
