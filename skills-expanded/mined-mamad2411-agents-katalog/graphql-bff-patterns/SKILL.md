---
name: graphql-bff-patterns
description: "Build BFFs for research UIs: DataLoader batching, persisted queries, auth context, and N+1 elimination."
category: backend
tags: ["GraphQL", "BFF", "DataLoader", "API"]
license: MIT
metadata:
  author: Syntedge Research
  product: Syntedge Skills Library
  locale: [en, ru]
  version: "1.0.0"
---

# SKILL: GraphQL BFF Patterns

> **RU:** Паттерны GraphQL BFF - BFF для research UI: DataLoader, persisted queries, auth context, устранение N+1.

## 1. Skill Meta
**Name:** GraphQL BFF Patterns
**Description:** Build BFFs for research UIs: DataLoader batching, persisted queries, auth context, and N+1 elimination.
**When to load:** Use this skill whenever the user asks for help with API, infra, data platform, or agent-orchestrator backend agents, especially tasks matching: GraphQL, BFF, DataLoader, API.
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
1. A concrete architecture or workflow for **GraphQL BFF Patterns** tailored to the user's stack.
2. A step-by-step implementation plan with validation gates.
3. Explicit anti-patterns to refuse or rewrite.
4. A short checklist the agent must pass before claiming done.
5. Sample configs, schemas, or code sketches when they unlock speed (complete, not stubbed).


## 5. Execution Sequence
1. Clarify scope for GraphQL BFF Patterns: inputs, outputs, constraints, and success metrics.
2. Inventory existing data, services, and ownership boundaries.
3. Propose the minimal viable architecture that still meets production constraints.
4. Implement in thin vertical slices with tests or evals at each gate.
5. Measure against the success metrics; document residual risks and follow-ups.


## 6. Domain Depth: GraphQL BFF Patterns

### BFF role
Shape data for UI; do not become a junk drawer business layer.

### Perf
DataLoader; persisted queries; complexity limits.

### Auth
Context per request; field-level auth for sensitive PnL.

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
- `GraphQL`
- `BFF`
- `DataLoader`
- `API`

---
*Syntedge Research Skills Library - backend / graphql-bff-patterns*
