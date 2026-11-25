---
name: u0279-collab-self-reflection-error-taxonomist
description: Build and operate the "Collab Self-Reflection Error Taxonomist" capability for Collaboration and Negotiation. Trigger when this exact capability is needed in mission execution.
---

# Collab Self-Reflection Error Taxonomist

## Why This Skill Exists
We need this skill because multi-agent systems underperform without explicit conflict resolution. This specific skill classifies recurrent reasoning failures for targeted fixes.

## When To Use
Use this skill when the request explicitly needs "Collab Self-Reflection Error Taxonomist" outcomes in the Collaboration and Negotiation domain.

## Step-by-Step Implementation Guide
1. Define the scope and success metrics for `Collab Self-Reflection Error Taxonomist`, including at least three measurable KPIs tied to deadlocks and degraded trust.
2. Design and version the input/output contract for proposals, contention signals, and negotiated outcomes, then add schema validation and failure-mode handling.
3. Implement the core capability using failure-type clustering, and produce error taxonomies with deterministic scoring.
4. Integrate the skill into swarm orchestration: task routing, approval gates, retry strategy, and rollback controls.
5. Add unit, integration, and simulation tests that explicitly cover deadlocks and degraded trust, then run regression baselines.
6. Deploy behind a feature flag, monitor telemetry/alerts for two release cycles, and iterate thresholds based on observed outcomes.

## Required Deliverables
- Capability contract: input schema, deterministic scoring, output schema, and failure modes.
- Runtime profile: general-capability using failure-type clustering to produce error taxonomies.
- Orchestration integration: collaboration-and-negotiation:general-capability routing, approval gates, retries, and rollback controls.
- Validation evidence: unit, integration, simulation, regression-baseline suites and rollout telemetry.

## Operational Runbook
### Preflight
- Confirm the Collab Self-Reflection Error Taxonomist request scope, source evidence, and measurable success criteria before execution.
- Verify feature flag skill_0279_collab-self-reflection-error-tax, approval gates, and rollback owner before autonomous use.

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
