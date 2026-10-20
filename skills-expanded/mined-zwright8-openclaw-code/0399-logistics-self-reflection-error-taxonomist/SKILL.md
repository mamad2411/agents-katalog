---
name: u0399-logistics-self-reflection-error-taxonomist
description: Build and operate the "Logistics Self-Reflection Error Taxonomist" capability for Resource Allocation and Logistics. Trigger when this exact capability is needed in mission execution.
---

# Logistics Self-Reflection Error Taxonomist

## Why This Skill Exists
We need this skill because impact work fails when scarce resources are not routed intelligently. This specific skill classifies recurrent reasoning failures for targeted fixes.

## When To Use
Use this skill when the request explicitly needs "Logistics Self-Reflection Error Taxonomist" outcomes in the Resource Allocation and Logistics domain.

## Step-by-Step Implementation Guide
1. Define the scope and success metrics for `Logistics Self-Reflection Error Taxonomist`, including at least three measurable KPIs tied to supply shortfalls and fairness gaps.
2. Design and version the input/output contract for capacity, bottlenecks, and distribution plans, then add schema validation and failure-mode handling.
3. Implement the core capability using failure-type clustering, and produce error taxonomies with deterministic scoring.
4. Integrate the skill into swarm orchestration: task routing, approval gates, retry strategy, and rollback controls.
5. Add unit, integration, and simulation tests that explicitly cover supply shortfalls and fairness gaps, then run regression baselines.
6. Deploy behind a feature flag, monitor telemetry/alerts for two release cycles, and iterate thresholds based on observed outcomes.

## Required Deliverables
- Capability contract: input schema, deterministic scoring, output schema, and failure modes.
- Runtime profile: general-capability using failure-type clustering to produce error taxonomies.
- Orchestration integration: resource-allocation-and-logistics:general-capability routing, approval gates, retries, and rollback controls.
- Validation evidence: unit, integration, simulation, regression-baseline suites and rollout telemetry.

## Operational Runbook
### Preflight
- Confirm the Logistics Self-Reflection Error Taxonomist request scope, source evidence, and measurable success criteria before execution.
- Verify feature flag skill_0399_logistics-self-reflection-error-, approval gates, and rollback owner before autonomous use.

### Execution
- Execute failure-type clustering with deterministic scoring and reproducible trace capture.
- Produce error taxonomies plus scorecard, assumptions, and unresolved-risk notes.

### Recovery
- Fail closed when required signals, evidence, or approval gates are missing.
- Rollback to the last stable baseline when posture is critical or validation fails.

### Handoff
- Publish error taxonomies, validation evidence, and telemetry links to downstream owners.
- Queue follow-up tasks for unresolved risks, threshold tuning, or approval review.

## Guardrails
- [quality] Require deterministic scoring and validation evidence before promotion.
- [reliability] Preserve retries, rollback controls, and failure-mode evidence for every run.
- [safety] Route critical posture or missing approval gates to human review before autonomous action.
