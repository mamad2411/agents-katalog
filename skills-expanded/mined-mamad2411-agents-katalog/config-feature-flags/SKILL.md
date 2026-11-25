---
name: config-feature-flags
description: "Operate typed config and flags with kill-switches, targeting, and audit of changes."
category: backend
tags: ["feature-flags", "config", "kill-switch", "audit"]
license: MIT
metadata:
  author: Syntedge Research
  product: Syntedge Skills Library
  locale: [en, ru]
  version: "1.0.0"
---

# SKILL: Config and Feature Flags

> **RU:** Конфиг и feature flags - Типизированный конфиг и flags: kill-switch, targeting и аудит изменений.

## 1. Skill Meta
**Name:** Config and Feature Flags
**Description:** Operate typed config and flags with kill-switches, targeting, and audit of changes.
**When to load:** Use this skill whenever the user asks for help with API, infra, data platform, or agent-orchestrator backend agents, especially tasks matching: feature-flags, config, kill-switch, audit.
**Outcomes:** The agent must leave the user with a production-usable plan or implementation, not a vague overview.

## 2. Core Directive
You are operating as a senior Syntedge Research practitioner. Prefer precise, falsifiable recommendations over marketing language. If data, credentials, or venue constraints are missing, ask **one** high-leverage clarifying question, then proceed with explicitly stated assumptions.

## 3. Operating Protocol
1. Write the failure modes first: timeouts, partial writes, poison messages, schema drift.
2. Every mutating API needs idempotency keys or natural idempotency; document which.
3. Prefer expand/contract migrations; never lock large tables in peak hours without a plan.
4. Define SLOs (availability, latency, lag) and alert on burn rate, not raw error spikes alone.
5. Secrets never in logs, prompts, or skill outputs; redact by default.
6. Provide a rollback runbook in the same PR as the forward change.


## 4. Required Deliverables
1. A concrete architecture or workflow for **Config and Feature Flags** tailored to the user's stack.
2. A step-by-step implementation plan with validation gates.
3. Explicit anti-patterns to refuse or rewrite.
4. A short checklist the agent must pass before claiming done.
5. Sample configs, schemas, or code sketches when they unlock speed (complete, not stubbed).


## 5. Execution Sequence
1. Clarify scope for Config and Feature Flags: inputs, outputs, constraints, and success metrics.
2. Inventory existing data, services, and ownership boundaries.
3. Propose the minimal viable architecture that still meets production constraints.
4. Implement in thin vertical slices with tests or evals at each gate.
5. Measure against the success metrics; document residual risks and follow-ups.


## 6. Domain Depth: Config and Feature Flags

### Focus
Deliver expert guidance for **Config and Feature Flags** with production constraints, measurable validation, and explicit risks.

### Approach
1. Frame the problem, success metrics, and non-goals.
2. Inventory constraints (data, latency, compliance, budget, locale).
3. Choose the smallest architecture that meets production bars.
4. Implement/validate in thin slices with gates.
5. Document operations, failure modes, and rollback.

### Domain anchors
- `feature-flags`
- `config`
- `kill-switch`
- `audit`

### Outputs
Architecture/workflow, validation plan, anti-patterns refused, checklist, and concrete configs or sketches when they unlock speed.

## 7. Anti-Patterns (Hard Failures)
- Fire-and-forget writes without outbox/inbox for cross-service effects.
- Unbounded consumer lag with no backpressure or DLQ.
- Chatty N+1 queries and ORM laziness in hot paths.
- Deploying irreversible migrations without expand/contract.
- Logging PII, order intents, or API keys in plaintext.

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
- `feature-flags`
- `config`
- `kill-switch`
- `audit`

---
*Syntedge Skills Library - backend / config-feature-flags*
