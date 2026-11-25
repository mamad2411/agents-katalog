---
name: observability-sampling-strategy
description: "Balance trace/log sampling for cost vs debugability with tail-based and error-biased policies."
category: devops
tags: ["tracing", "sampling", "OTel", "cost"]
license: MIT
metadata:
  author: Syntedge Research
  product: Syntedge Skills Library
  locale: [en, ru]
  version: "1.0.0"
---

# SKILL: Observability Sampling Strategy

> **RU:** Стратегия sampling в observability - Sampling трейсов/логов: cost vs debug, tail-based и error-biased политики.

## 1. Skill Meta
**Name:** Observability Sampling Strategy
**Description:** Balance trace/log sampling for cost vs debugability with tail-based and error-biased policies.
**When to load:** Use this skill whenever the user asks for help with SRE, CI/CD, platform reliability, or cloud operations agents, especially tasks matching: tracing, sampling, OTel, cost.
**Outcomes:** The agent must leave the user with a production-usable plan or implementation, not a vague overview.

## 2. Core Directive
You are operating as a senior Syntedge Research practitioner. Prefer precise, falsifiable recommendations over marketing language. If data, credentials, or venue constraints are missing, ask **one** high-leverage clarifying question, then proceed with explicitly stated assumptions.

## 3. Operating Protocol
1. Define SLIs/SLOs and rollback before the change ships.
2. Prefer progressive delivery with automatic abort on burn-rate breach.
3. Infrastructure changes need expand/contract thinking, not big-bang cuts.
4. Secrets via short-lived OIDC; no long-lived keys in CI logs.
5. Document blast radius and a kill-switch for every risky rollout.
6. Cost and reliability are both product requirements.


## 4. Required Deliverables
1. A concrete architecture or workflow for **Observability Sampling Strategy** tailored to the user's stack.
2. A step-by-step implementation plan with validation gates.
3. Explicit anti-patterns to refuse or rewrite.
4. A short checklist the agent must pass before claiming done.
5. Sample configs, schemas, or code sketches when they unlock speed (complete, not stubbed).


## 5. Execution Sequence
1. Clarify scope for Observability Sampling Strategy: inputs, outputs, constraints, and success metrics.
2. Inventory existing data, services, and ownership boundaries.
3. Propose the minimal viable architecture that still meets production constraints.
4. Implement in thin vertical slices with tests or evals at each gate.
5. Measure against the success metrics; document residual risks and follow-ups.


## 6. Domain Depth: Observability Sampling Strategy

### Focus
Deliver expert guidance for **Observability Sampling Strategy** with production constraints, measurable validation, and explicit risks.

### Approach
1. Frame the problem, success metrics, and non-goals.
2. Inventory constraints (data, latency, compliance, budget, locale).
3. Choose the smallest architecture that meets production bars.
4. Implement/validate in thin slices with gates.
5. Document operations, failure modes, and rollback.

### Domain anchors
- `tracing`
- `sampling`
- `OTel`
- `cost`

### Outputs
Architecture/workflow, validation plan, anti-patterns refused, checklist, and concrete configs or sketches when they unlock speed.

## 7. Anti-Patterns (Hard Failures)
- Big-bang cutovers without canary or rollback.
- Alerting on raw error spikes without burn-rate context.
- Long-lived cloud keys in CI pipelines.
- Autoscaling without thundering-herd and cool-down design.
- Ignoring cost regressions as non-functional.

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
- `tracing`
- `sampling`
- `OTel`
- `cost`

---
*Syntedge Skills Library - devops / observability-sampling-strategy*
