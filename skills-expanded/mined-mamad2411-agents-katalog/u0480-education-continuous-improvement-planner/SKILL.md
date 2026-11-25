---
name: u0480-education-continuous-improvement-planner
description: Build and operate the "Education Continuous Improvement Planner" capability for Education and Upskilling. Trigger when this exact capability is needed in mission execution.
---

# Education Continuous Improvement Planner

## Why This Skill Exists
We need this skill because human capability growth requires targeted planning under constraints. This specific skill turns findings into sustained upgrade cycles.

## When To Use
Use this skill when the request explicitly needs "Education Continuous Improvement Planner" outcomes in the Education and Upskilling domain.

## Step-by-Step Implementation Guide
1. Define the scope and success metrics for `Education Continuous Improvement Planner`, including at least three measurable KPIs tied to persistent skill gaps and poor learning outcomes.
2. Design and version the input/output contract for skill profiles, learning paths, and support resources, then add schema validation and failure-mode handling.
3. Implement the core capability using closed-loop prioritization, and produce improvement roadmaps with deterministic scoring.
4. Integrate the skill into swarm orchestration: task routing, approval gates, retry strategy, and rollback controls.
5. Add unit, integration, and simulation tests that explicitly cover persistent skill gaps and poor learning outcomes, then run regression baselines.
6. Deploy behind a feature flag, monitor telemetry/alerts for two release cycles, and iterate thresholds based on observed outcomes.

## Required Deliverables
- Capability contract: input schema, deterministic scoring, output schema, and failure modes.
- Runtime profile: planning-router using closed-loop prioritization to produce improvement roadmaps.
- Orchestration integration: education-and-upskilling:planning-router routing, approval gates, retries, and rollback controls.
- Validation evidence: unit, integration, simulation, regression-baseline suites and rollout telemetry.

## Operational Runbook
### Preflight
- Confirm the Education Continuous Improvement Planner request scope, source evidence, and measurable success criteria before execution.
- Verify feature flag skill_0480_education-continuous-improvement, approval gates, and rollback owner before autonomous use.

### Execution
- Execute closed-loop prioritization with deterministic scoring and reproducible trace capture.
- Produce improvement roadmaps plus scorecard, assumptions, and unresolved-risk notes.

### Recovery
- Fail closed when required signals, evidence, or approval gates are missing.
- Rollback to the last stable baseline when posture is critical or validation fails.

### Handoff
- Publish improvement roadmaps, validation evidence, and telemetry links to downstream owners.
- Queue follow-up tasks for unresolved risks, threshold tuning, or approval review.

## Guardrails
- [quality] Require deterministic scoring and validation evidence before promotion.
- [reliability] Preserve retries, rollback controls, and failure-mode evidence for every run.
- [safety] Route critical posture or missing approval gates to human review before autonomous action.
