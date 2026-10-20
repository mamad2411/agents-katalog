---
name: design-token-migration-pipeline
description: "Migrate legacy CSS/theme values into semantic tokens with codemods, visual diffs, and a freeze window for product UI."
category: frontend
tags: ["tokens","migration","design-system","codemod"]
license: MIT
metadata:
  author: Syntedge Research
  product: Syntedge Skills Library
  locale: [en, ru]
  version: "1.0.0"
---

# SKILL: Design Token Migration Pipeline

> **RU:** Миграция design tokens - Миграция legacy CSS/theme в semantic tokens: codemod, visual diff и freeze-окно для продуктового UI.

## 1. Skill Meta
**Name:** Design Token Migration Pipeline
**Description:** Migrate legacy CSS/theme values into semantic tokens with codemods, visual diffs, and a freeze window for product UI.
**When to load:** Use this skill whenever the user asks for help matching: tokens, migration, design-system, codemod.
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
1. A concrete architecture or workflow for **Design Token Migration Pipeline** tailored to the user's stack.
2. A step-by-step implementation plan with validation gates.
3. Explicit anti-patterns to refuse or rewrite.
4. A short checklist the agent must pass before claiming done.
5. Sample configs, schemas, or code sketches when they unlock speed (complete, not stubbed).

## 5. Execution Sequence
1. Clarify scope for Design Token Migration Pipeline: inputs, outputs, constraints, and success metrics.
2. Inventory existing systems, ownership, and failure modes.
3. Propose the minimal viable architecture that still meets production constraints.
4. Implement in thin vertical slices with tests or evals at each gate.
5. Measure against the success metrics; document residual risks and follow-ups.

## 6. Domain Depth: Design Token Migration Pipeline

### Focus
Inventory raw colors/spacing; define semantic layers; automate replacements; gate on screenshot CI.

### Practical moves
1. Write the success metric and kill criteria first.
2. Inventory current state vs desired state with explicit gaps.
3. Implement the smallest change that moves the metric.
4. Add observability and a rollback path before widening rollout.
5. Capture a Run Card: what changed, how verified, what remains.

### Outputs
Architecture notes, configs/schemas as needed, validation evidence, and residual risks.

## 7. Anti-Patterns (Hard Failures)
- Renaming tokens without updating consumers in the same PR.
- Mixing hard-coded hex with tokens in new components.
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
- `tokens`
- `migration`
- `design-system`
- `codemod`

---
*Syntedge Research Skills Library - frontend / design-token-migration-pipeline*
