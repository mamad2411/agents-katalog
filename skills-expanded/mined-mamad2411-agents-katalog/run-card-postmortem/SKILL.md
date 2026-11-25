---
name: run-card-postmortem
description: "Standardize Run Cards and lightweight postmortems for agent failures, regressions, and near-misses."
category: agents
pack: agent-ops
tags: ["run-card", "postmortem", "ops", "quality"]
license: MIT
metadata:
  author: Syntedge Research
  product: Syntedge Agent Ops
  locale: [en, ru]
  version: "1.0.0"
---

# SKILL: Run Card Postmortem

> **RU:** Run card и postmortem - Стандартизация Run Cards и лёгких postmortem для сбоев, регрессий и near-miss агентов.

## 1. Skill Meta
**Name:** Run Card Postmortem
**Description:** Standardize Run Cards and lightweight postmortems for agent failures, regressions, and near-misses.
**When to load:** agents tasks matching run-card, postmortem, ops, quality.
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
1. Scoped plan for **Run Card Postmortem**
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

## 6. Domain Depth: Run Card Postmortem

### Template
Goal → changes → metrics → risks → next actions.

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
Part of **Syntedge Agent Ops**.

## 10. Reference Vocabulary
- `run-card`
- `postmortem`
- `ops`
- `quality`

---
*Syntedge Research - agent-ops / run-card-postmortem*
