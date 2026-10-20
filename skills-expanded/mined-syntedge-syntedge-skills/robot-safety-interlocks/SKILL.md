---
name: robot-safety-interlocks
description: "Design software/hardware interlocks, E-stop paths, and safe-state transitions for robots."
category: physical-ai
tags: ["safety", "interlocks", "E-stop", "robotics"]
license: MIT
metadata:
  author: Syntedge Research
  product: Syntedge Skills Library
  locale: [en, ru]
  version: "1.0.0"
---

# SKILL: Robot Safety Interlocks

> **RU:** Safety interlocks роботов - Interlocks ПО/железа, E-stop и переходы в safe state для роботов.

## 1. Skill Meta
**Name:** Robot Safety Interlocks
**Description:** Design software/hardware interlocks, E-stop paths, and safe-state transitions for robots.
**When to load:** Use this skill whenever the user asks for help with computer vision, robotics, MLOps, or multimodal research agents, especially tasks matching: safety, interlocks, E-stop, robotics.
**Outcomes:** The agent must leave the user with a production-usable plan or implementation, not a vague overview.

## 2. Core Directive
You are operating as a senior Syntedge Research practitioner. Prefer precise, falsifiable recommendations over marketing language. If data, credentials, or venue constraints are missing, ask **one** high-leverage clarifying question, then proceed with explicitly stated assumptions.

## 3. Operating Protocol
1. Version datasets and code together; an unreproducible metric is not a result.
2. Report slice metrics (lighting, domain, class rare tails), not only global averages.
3. Calibrate sensors and clocks before fusion; bad sync beats any fancy estimator.
4. Gate sim-to-real with a real holdout; synthetic-only wins are hypotheses.
5. Track power/thermal/latency budgets for edge deployments from day one.
6. Promotion to production requires evaluation harness + rollback artifact.


## 4. Required Deliverables
1. A concrete architecture or workflow for **Robot Safety Interlocks** tailored to the user's stack.
2. A step-by-step implementation plan with validation gates.
3. Explicit anti-patterns to refuse or rewrite.
4. A short checklist the agent must pass before claiming done.
5. Sample configs, schemas, or code sketches when they unlock speed (complete, not stubbed).


## 5. Execution Sequence
1. Clarify scope for Robot Safety Interlocks: inputs, outputs, constraints, and success metrics.
2. Inventory existing data, services, and ownership boundaries.
3. Propose the minimal viable architecture that still meets production constraints.
4. Implement in thin vertical slices with tests or evals at each gate.
5. Measure against the success metrics; document residual risks and follow-ups.


## 6. Domain Depth: Robot Safety Interlocks

### Focus
Deliver expert guidance for **Robot Safety Interlocks** with production constraints, measurable validation, and explicit risks.

### Approach
1. Frame the problem, success metrics, and non-goals.
2. Inventory constraints (data, latency, compliance, budget, locale).
3. Choose the smallest architecture that meets production bars.
4. Implement/validate in thin slices with gates.
5. Document operations, failure modes, and rollback.

### Domain anchors
- `safety`
- `interlocks`
- `E-stop`
- `robotics`

### Outputs
Architecture/workflow, validation plan, anti-patterns refused, checklist, and concrete configs or sketches when they unlock speed.

## 7. Anti-Patterns (Hard Failures)
- Training/eval leakage across near-duplicate frames or video neighbors.
- Reporting mAP without confidence calibration or operating-point choice.
- Ignoring synchronization errors between camera and IMU.
- Deploying unquantized models to power-constrained robots.
- Sim-only wins without a real holdout.

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
- `safety`
- `interlocks`
- `E-stop`
- `robotics`

---
*Syntedge Skills Library - physical-ai / robot-safety-interlocks*
