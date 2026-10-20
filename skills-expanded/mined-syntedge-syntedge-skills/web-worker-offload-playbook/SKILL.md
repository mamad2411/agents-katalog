---
name: web-worker-offload-playbook
description: "Offload heavy parsing, WASM, and chart prep to workers with transferable data and UI-thread budgets."
category: frontend
tags: ["web-workers","performance","WASM","INP"]
license: MIT
metadata:
  author: Syntedge Research
  product: Syntedge Skills Library
  locale: [en, ru]
  version: "1.0.0"
---

# SKILL: Web Worker Offload Playbook

> **RU:** Вынос работы в Web Workers - Тяжёлый parsing/WASM/chart prep в workers: transferable data и бюджеты UI-потока.

## 1. Skill Meta
**Name:** Web Worker Offload Playbook
**Description:** Offload heavy parsing, WASM, and chart prep to workers with transferable data and UI-thread budgets.
**When to load:** Use this skill whenever the user asks for help matching: web-workers, performance, WASM, INP.
**Outcomes:** The agent must leave the user with a production-usable plan or implementation, not a vague overview.

## 2. Core Directive
You are operating as a senior Syntedge Research practitioner. Prefer precise, falsifiable recommendations over marketing language. If credentials, stack constraints, or success metrics are missing, ask **one** high-leverage clarifying question, then proceed with explicitly stated assumptions.

## 3. Operating Protocol
1. Lock scope, environment, and non-goals before proposing architecture.
2. Prefer measurable gates (latency, cost, error rate, eval score) over aesthetic claims.
3. Separate research experiments from production credentials and write paths.
4. Document assumptions in a short Research Card: hypothesis, method, risk, kill criteria.
5. Default to least privilege for tools, data, and network.
6. Ship thin vertical slices with validation at each gate.

## 4. Required Deliverables
1. A concrete architecture or workflow for **Web Worker Offload Playbook** tailored to the user's stack.
2. A step-by-step implementation plan with validation gates.
3. Explicit anti-patterns to refuse or rewrite.
4. A short checklist the agent must pass before claiming done.
5. Sample configs, schemas, or code sketches when they unlock speed (complete, not stubbed).

## 5. Execution Sequence
1. Clarify scope for Web Worker Offload Playbook: inputs, outputs, constraints, and success metrics.
2. Inventory existing systems, ownership, and failure modes.
3. Propose the minimal viable architecture that still meets production constraints.
4. Implement in thin vertical slices with tests or evals at each gate.
5. Measure against the success metrics; document residual risks and follow-ups.

## 6. Domain Depth: Web Worker Offload Playbook

### Focus
Profile main-thread long tasks; define worker protocol; transfer ArrayBuffers; fallback when workers blocked.

### Practical moves
1. Write the success metric and kill criteria first.
2. Inventory current state vs desired state with explicit gaps.
3. Implement the smallest change that moves the metric.
4. Add observability and a rollback path before widening rollout.
5. Capture a Run Card: what changed, how verified, what remains.

### Outputs
Architecture notes, configs/schemas as needed, validation evidence, and residual risks.

## 7. Anti-Patterns (Hard Failures)
- Doing large JSON.parse on the UI thread in production.
- Posting huge structured clones every frame.
- Shipping placeholders, TODOs, or "wire this later" as finished work.
- Ignoring locale, timezone, or access-control constraints stated by the user.

## 8. Validation Checklist
- [ ] Assumptions stated (stack, data, latency, budget, locale)
- [ ] Success metrics defined and measurable
- [ ] Failure modes and rollback considered
- [ ] No banned anti-patterns from Section 7
- [ ] Output is complete (no stubs, no "and so on")
- [ ] RU/EN terminology consistent when bilingual docs are requested

## 9. Integration with Syntedge Orchestrator
When running inside the Syntedge orchestrator:
1. Declare tool needs up front (repo, browser, DB, GPU, secrets).
2. Load only sibling skills that reduce ambiguity; avoid skill thrash.
3. Persist artifacts (schemas, configs, eval reports) to the run workspace.
4. Emit a final **Run Card**: goal, changes, metrics, risks, next actions.

## 10. Reference Vocabulary
- `web-workers`
- `performance`
- `WASM`
- `INP`

---
*Syntedge Research Skills Library - frontend / web-worker-offload-playbook*
