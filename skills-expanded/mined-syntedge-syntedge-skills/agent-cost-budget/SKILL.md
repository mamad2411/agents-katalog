---
name: agent-cost-budget
description: "Enforce per-run and per-desk token/tool cost budgets with kill switches and spend reports."
category: agents
pack: agent-ops
tags: ["cost", "budget", "tokens", "ops"]
license: MIT
metadata:
  author: Syntedge Research
  product: Syntedge Agent Ops
  locale: [en, ru]
  version: "1.0.0"
---

# SKILL: Agent Cost Budget

> **RU:** Cost budget агента - Бюджеты token/tool на run и desk: kill switches и отчёты spend.

## 1. Skill Meta
**Name:** Agent Cost Budget
**Description:** Enforce per-run and per-desk token/tool cost budgets with kill switches and spend reports.
**When to load:** agents tasks matching cost, budget, tokens, ops.
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
1. Scoped plan for **Agent Cost Budget**
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

## 6. Domain Depth: Agent Cost Budget

### Gate
Hard stop when budget exceeded; soft warn at 80%.

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
- `cost`
- `budget`
- `tokens`
- `ops`

---
*Syntedge Research - agent-ops / agent-cost-budget*
