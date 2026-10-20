---
name: u0190-governance-privacy-preserving-data-broker
description: Build and operate the "Governance Privacy Preserving Data Broker" capability for Safety and Governance. Trigger when this exact capability is needed in mission execution.
---

# Governance Privacy Preserving Data Broker

## Why This Skill Exists
We need this skill because high-speed autonomy needs enforceable guardrails to stay aligned. This specific skill enables collaboration while minimizing raw data exposure.

## When To Use
Use this skill when the request explicitly needs "Governance Privacy Preserving Data Broker" outcomes in the Safety and Governance domain.

## Step-by-Step Implementation Guide
1. Define the scope and success metrics for `Governance Privacy Preserving Data Broker`, including at least three measurable KPIs tied to unsafe actions and policy drift.
2. Design and version the input/output contract for policies, violations, and mitigation actions, then add schema validation and failure-mode handling.
3. Implement the core capability using policy-scoped data mediation, and produce privacy-scoped exchanges with deterministic scoring.
4. Integrate the skill into swarm orchestration: task routing, approval gates, retry strategy, and rollback controls.
5. Add unit, integration, and simulation tests that explicitly cover unsafe actions and policy drift, then run regression baselines.
6. Deploy behind a feature flag, monitor telemetry/alerts for two release cycles, and iterate thresholds based on observed outcomes.

## Required Deliverables
- Capability contract: input schema, deterministic scoring, output schema, and failure modes.
- Runtime profile: collaboration-mediator using policy-scoped data mediation to produce privacy-scoped exchanges.
- Orchestration integration: safety-and-governance:collaboration-mediator routing, approval gates, retries, and rollback controls.
- Validation evidence: unit, integration, simulation, regression-baseline suites and rollout telemetry.

## Operational Runbook
### Preflight
- Confirm the Governance Privacy Preserving Data Broker request scope, source evidence, and measurable success criteria before execution.
- Verify feature flag skill_0190_governance-privacy-preserving-da, approval gates, and rollback owner before autonomous use.

### Execution
- Execute policy-scoped data mediation with deterministic scoring and reproducible trace capture.
- Produce privacy-scoped exchanges plus scorecard, assumptions, and unresolved-risk notes.

### Recovery
- Fail closed when required signals, evidence, or approval gates are missing.
- Rollback to the last stable baseline when posture is critical or validation fails.

### Handoff
- Publish privacy-scoped exchanges, validation evidence, and telemetry links to downstream owners.
- Queue follow-up tasks for unresolved risks, threshold tuning, or approval review.

## Guardrails
- [quality] Require deterministic scoring and validation evidence before promotion.
- [reliability] Preserve retries, rollback controls, and failure-mode evidence for every run.
- [safety] Route critical posture or missing approval gates to human review before autonomous action.
