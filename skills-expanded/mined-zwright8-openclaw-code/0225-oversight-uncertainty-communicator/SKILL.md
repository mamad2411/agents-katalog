---
name: u0225-oversight-uncertainty-communicator
description: Build and operate the "Oversight Uncertainty Communicator" capability for Human Oversight and Operator UX. Trigger when this exact capability is needed in mission execution.
---

# Oversight Uncertainty Communicator

## Why This Skill Exists
We need this skill because human teams need fast, legible control when stakes are high. This specific skill prevents overstatement by explicitly framing uncertainty.

## When To Use
Use this skill when the request explicitly needs "Oversight Uncertainty Communicator" outcomes in the Human Oversight and Operator UX domain.

## Step-by-Step Implementation Guide
1. Define the scope and success metrics for `Oversight Uncertainty Communicator`, including at least three measurable KPIs tied to slow interventions and approval bottlenecks.
2. Design and version the input/output contract for approval queues, operator workload, and intervention history, then add schema validation and failure-mode handling.
3. Implement the core capability using confidence-bound communication templates, and produce uncertainty briefs with deterministic scoring.
4. Integrate the skill into swarm orchestration: task routing, approval gates, retry strategy, and rollback controls.
5. Add unit, integration, and simulation tests that explicitly cover slow interventions and approval bottlenecks, then run regression baselines.
6. Deploy behind a feature flag, monitor telemetry/alerts for two release cycles, and iterate thresholds based on observed outcomes.

## Required Deliverables
- Capability contract: input schema, deterministic scoring, output schema, and failure modes.
- Runtime profile: communication-engine using confidence-bound communication templates to produce uncertainty briefs.
- Orchestration integration: human-oversight-and-operator-ux:communication-engine routing, approval gates, retries, and rollback controls.
- Validation evidence: unit, integration, simulation, regression-baseline suites and rollout telemetry.

## Operational Runbook
### Preflight
- Confirm the Oversight Uncertainty Communicator request scope, source evidence, and measurable success criteria before execution.
- Verify feature flag skill_0225_oversight-uncertainty-communicat, approval gates, and rollback owner before autonomous use.

### Execution
- Execute confidence-bound communication templates with deterministic scoring and reproducible trace capture.
- Produce uncertainty briefs plus scorecard, assumptions, and unresolved-risk notes.

### Recovery
- Fail closed when required signals, evidence, or approval gates are missing.
- Rollback to the last stable baseline when posture is critical or validation fails.

### Handoff
- Publish uncertainty briefs, validation evidence, and telemetry links to downstream owners.
- Queue follow-up tasks for unresolved risks, threshold tuning, or approval review.

## Guardrails
- [quality] Require deterministic scoring and validation evidence before promotion.
- [reliability] Preserve retries, rollback controls, and failure-mode evidence for every run.
- [safety] Route critical posture or missing approval gates to human review before autonomous action.
