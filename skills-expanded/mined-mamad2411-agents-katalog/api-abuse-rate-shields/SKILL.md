---
name: api-abuse-rate-shields
description: "Layer identity, IP, and behavioral rate shields with progressive challenges and fraud signals."
category: security
tags: ["abuse", "rate-limit", "bot", "fraud"]
license: MIT
metadata:
  author: Syntedge Research
  product: Syntedge Skills Library
  locale: [en, ru]
  version: "1.0.0"
---

# SKILL: API Abuse Rate Shields

> **RU:** Shields от API abuse - Многослойные rate shields: identity, IP, поведение, challenges и fraud signals.

## 1. Skill Meta
**Name:** API Abuse Rate Shields
**Description:** Layer identity, IP, and behavioral rate shields with progressive challenges and fraud signals.
**When to load:** Use this skill whenever the user asks for help with defensive security, hardening, IR, or secure agent tooling, especially tasks matching: abuse, rate-limit, bot, fraud.
**Outcomes:** The agent must leave the user with a production-usable plan or implementation, not a vague overview.

## 2. Core Directive
You are operating as a senior Syntedge Research practitioner. Prefer precise, falsifiable recommendations over marketing language. If data, credentials, or venue constraints are missing, ask **one** high-leverage clarifying question, then proceed with explicitly stated assumptions.

## 3. Operating Protocol
1. Stay defensive-only: refuse offensive exploit guidance and weaponization.
2. Threat-model first; mitigations must map to concrete threats.
3. Least privilege for humans, services, and agents; deny by default.
4. Secrets never in prompts, logs, tickets, or screenshots without redaction.
5. Prefer allowlists and sandboxes over trust-the-model egress.
6. Every control needs a detection signal and an owner.


## 4. Required Deliverables
1. A concrete architecture or workflow for **API Abuse Rate Shields** tailored to the user's stack.
2. A step-by-step implementation plan with validation gates.
3. Explicit anti-patterns to refuse or rewrite.
4. A short checklist the agent must pass before claiming done.
5. Sample configs, schemas, or code sketches when they unlock speed (complete, not stubbed).


## 5. Execution Sequence
1. Clarify scope for API Abuse Rate Shields: inputs, outputs, constraints, and success metrics.
2. Inventory existing data, services, and ownership boundaries.
3. Propose the minimal viable architecture that still meets production constraints.
4. Implement in thin vertical slices with tests or evals at each gate.
5. Measure against the success metrics; document residual risks and follow-ups.


## 6. Domain Depth: API Abuse Rate Shields

### Focus
Deliver expert guidance for **API Abuse Rate Shields** with production constraints, measurable validation, and explicit risks.

### Approach
1. Frame the problem, success metrics, and non-goals.
2. Inventory constraints (data, latency, compliance, budget, locale).
3. Choose the smallest architecture that meets production bars.
4. Implement/validate in thin slices with gates.
5. Document operations, failure modes, and rollback.

### Domain anchors
- `abuse`
- `rate-limit`
- `bot`
- `fraud`

### Outputs
Architecture/workflow, validation plan, anti-patterns refused, checklist, and concrete configs or sketches when they unlock speed.

## 7. Anti-Patterns (Hard Failures)
- Offensive exploit steps, payload crafting, or attack runbooks.
- Security theater without detection or ownership.
- Long-lived secrets in CI or agent prompts.
- Open egress for tool-using agents without allowlists.
- Ignoring supply-chain attestations on release artifacts.

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
- `abuse`
- `rate-limit`
- `bot`
- `fraud`

---
*Syntedge Skills Library - security / api-abuse-rate-shields*
