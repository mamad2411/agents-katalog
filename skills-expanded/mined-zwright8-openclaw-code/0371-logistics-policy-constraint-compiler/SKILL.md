---
name: u0371-logistics-policy-constraint-compiler
description: Build and operate the "Logistics Policy Constraint Compiler" capability for Resource Allocation and Logistics. Trigger when this exact capability is needed in mission execution.
---

# Logistics Policy Constraint Compiler

## Why This Skill Exists
We need this skill because impact work fails when scarce resources are not routed intelligently. This specific skill turns governance language into enforceable runtime checks.

## When To Use
Use this skill when the request explicitly needs "Logistics Policy Constraint Compiler" outcomes in the Resource Allocation and Logistics domain.

## Step-by-Step Implementation Guide
1. Define the scope and success metrics for `Logistics Policy Constraint Compiler`, including at least three measurable KPIs tied to supply shortfalls and fairness gaps.
2. Design and version the input/output contract for capacity, bottlenecks, and distribution plans, then add schema validation and failure-mode handling.
3. Implement the core capability using rule compilation, and produce executable policy bundles with deterministic scoring.
4. Integrate the skill into swarm orchestration: task routing, approval gates, retry strategy, and rollback controls.
5. Add unit, integration, and simulation tests that explicitly cover supply shortfalls and fairness gaps, then run regression baselines.
6. Deploy behind a feature flag, monitor telemetry/alerts for two release cycles, and iterate thresholds based on observed outcomes.

## Required Deliverables
- Capability contract: input schema, deterministic scoring, output schema, and failure modes.
- Runtime profile: contract-compiler using rule compilation to produce executable policy bundles.
- Orchestration integration: resource-allocation-and-logistics:contract-compiler routing, approval gates, retries, and rollback controls.
- Validation evidence: unit, integration, simulation, regression-baseline suites and rollout telemetry.

## Operational Runbook
### Preflight
- Confirm the Logistics Policy Constraint Compiler request scope, source evidence, and measurable success criteria before execution.
- Verify feature flag skill_0371_logistics-policy-constraint-comp, approval gates, and rollback owner before autonomous use.

### Execution
- Execute rule compilation with deterministic scoring and reproducible trace capture.
- Produce executable policy bundles plus scorecard, assumptions, and unresolved-risk notes.

### Recovery
- Fail closed when required signals, evidence, or approval gates are missing.
- Rollback to the last stable baseline when posture is critical or validation fails.

### Handoff
- Publish executable policy bundles, validation evidence, and telemetry links to downstream owners.
- Queue follow-up tasks for unresolved risks, threshold tuning, or approval review.

## Guardrails
- [quality] Require deterministic scoring and validation evidence before promotion.
- [reliability] Preserve retries, rollback controls, and failure-mode evidence for every run.
- [safety] Route critical posture or missing approval gates to human review before autonomous action.
