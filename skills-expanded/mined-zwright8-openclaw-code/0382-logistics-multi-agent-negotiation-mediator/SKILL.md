---
name: u0382-logistics-multi-agent-negotiation-mediator
description: Build and operate the "Logistics Multi-Agent Negotiation Mediator" capability for Resource Allocation and Logistics. Trigger when this exact capability is needed in mission execution.
---

# Logistics Multi-Agent Negotiation Mediator

## Why This Skill Exists
We need this skill because impact work fails when scarce resources are not routed intelligently. This specific skill resolves resource and strategy conflicts with explicit tradeoffs.

## When To Use
Use this skill when the request explicitly needs "Logistics Multi-Agent Negotiation Mediator" outcomes in the Resource Allocation and Logistics domain.

## Step-by-Step Implementation Guide
1. Define the scope and success metrics for `Logistics Multi-Agent Negotiation Mediator`, including at least three measurable KPIs tied to supply shortfalls and fairness gaps.
2. Design and version the input/output contract for capacity, bottlenecks, and distribution plans, then add schema validation and failure-mode handling.
3. Implement the core capability using structured bargaining protocols, and produce negotiated agreement sets with deterministic scoring.
4. Integrate the skill into swarm orchestration: task routing, approval gates, retry strategy, and rollback controls.
5. Add unit, integration, and simulation tests that explicitly cover supply shortfalls and fairness gaps, then run regression baselines.
6. Deploy behind a feature flag, monitor telemetry/alerts for two release cycles, and iterate thresholds based on observed outcomes.

## Required Deliverables
- Capability contract: input schema, deterministic scoring, output schema, and failure modes.
- Runtime profile: collaboration-mediator using structured bargaining protocols to produce negotiated agreement sets.
- Orchestration integration: resource-allocation-and-logistics:collaboration-mediator routing, approval gates, retries, and rollback controls.
- Validation evidence: unit, integration, simulation, regression-baseline suites and rollout telemetry.

## Operational Runbook
### Preflight
- Confirm the Logistics Multi-Agent Negotiation Mediator request scope, source evidence, and measurable success criteria before execution.
- Verify feature flag skill_0382_logistics-multi-agent-negotiatio, approval gates, and rollback owner before autonomous use.

### Execution
- Execute structured bargaining protocols with deterministic scoring and reproducible trace capture.
- Produce negotiated agreement sets plus scorecard, assumptions, and unresolved-risk notes.

### Recovery
- Fail closed when required signals, evidence, or approval gates are missing.
- Rollback to the last stable baseline when posture is critical or validation fails.

### Handoff
- Publish negotiated agreement sets, validation evidence, and telemetry links to downstream owners.
- Queue follow-up tasks for unresolved risks, threshold tuning, or approval review.

## Guardrails
- [quality] Require deterministic scoring and validation evidence before promotion.
- [reliability] Preserve retries, rollback controls, and failure-mode evidence for every run.
- [safety] Route critical posture or missing approval gates to human review before autonomous action.
