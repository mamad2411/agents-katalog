---
name: u0086-memory-counterfactual-simulator
description: Build and operate the "Memory Counterfactual Simulator" capability for Memory and Knowledge Operations. Trigger when this exact capability is needed in mission execution.
---

# Memory Counterfactual Simulator

## Why This Skill Exists
We need this skill because agents lose performance when lessons are not retained and reused. This specific skill tests alternatives before costly commitments.

## When To Use
Use this skill when the request explicitly needs "Memory Counterfactual Simulator" outcomes in the Memory and Knowledge Operations domain.

## Step-by-Step Implementation Guide
1. Define the scope and success metrics for `Memory Counterfactual Simulator`, including at least three measurable KPIs tied to repeated mistakes and context loss.
2. Design and version the input/output contract for episodic logs, knowledge nodes, and retrieval metadata, then add schema validation and failure-mode handling.
3. Implement the core capability using counterfactual replay, and produce scenario comparison reports with deterministic scoring.
4. Integrate the skill into swarm orchestration: task routing, approval gates, retry strategy, and rollback controls.
5. Add unit, integration, and simulation tests that explicitly cover repeated mistakes and context loss, then run regression baselines.
6. Deploy behind a feature flag, monitor telemetry/alerts for two release cycles, and iterate thresholds based on observed outcomes.

## Required Deliverables
- Capability contract: input schema, deterministic scoring, output schema, and failure modes.
- Runtime profile: simulation-lab using counterfactual replay to produce scenario comparison reports.
- Orchestration integration: memory-and-knowledge-operations:simulation-lab routing, approval gates, retries, and rollback controls.
- Validation evidence: unit, integration, simulation, regression-baseline suites and rollout telemetry.

## Operational Runbook
### Preflight
- Confirm the Memory Counterfactual Simulator request scope, source evidence, and measurable success criteria before execution.
- Verify feature flag skill_0086_memory-counterfactual-simulator, approval gates, and rollback owner before autonomous use.

### Execution
- Execute counterfactual replay with deterministic scoring and reproducible trace capture.
- Produce scenario comparison reports plus scorecard, assumptions, and unresolved-risk notes.

### Recovery
- Fail closed when required signals, evidence, or approval gates are missing.
- Rollback to the last stable baseline when posture is critical or validation fails.

### Handoff
- Publish scenario comparison reports, validation evidence, and telemetry links to downstream owners.
- Queue follow-up tasks for unresolved risks, threshold tuning, or approval review.

## Guardrails
- [quality] Require deterministic scoring and validation evidence before promotion.
- [reliability] Preserve retries, rollback controls, and failure-mode evidence for every run.
- [safety] Route critical posture or missing approval gates to human review before autonomous action.
