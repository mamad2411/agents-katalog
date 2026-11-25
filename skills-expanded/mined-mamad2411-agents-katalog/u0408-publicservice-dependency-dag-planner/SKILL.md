---
name: u0408-publicservice-dependency-dag-planner
description: Build and operate the "PublicService Dependency DAG Planner" capability for Healthcare and Public Services. Trigger when this exact capability is needed in mission execution.
---

# PublicService Dependency DAG Planner

## Why This Skill Exists
We need this skill because public-facing workflows require strict safety and reliability controls. This specific skill prevents sequencing errors and hidden blockers.

## When To Use
Use this skill when the request explicitly needs "PublicService Dependency DAG Planner" outcomes in the Healthcare and Public Services domain.

## Step-by-Step Implementation Guide
1. Define the scope and success metrics for `PublicService Dependency DAG Planner`, including at least three measurable KPIs tied to service harm and procedural violations.
2. Design and version the input/output contract for protocol checks, service queues, and compliance flags, then add schema validation and failure-mode handling.
3. Implement the core capability using dependency graph compilation, and produce validated workflow DAGs with deterministic scoring.
4. Integrate the skill into swarm orchestration: task routing, approval gates, retry strategy, and rollback controls.
5. Add unit, integration, and simulation tests that explicitly cover service harm and procedural violations, then run regression baselines.
6. Deploy behind a feature flag, monitor telemetry/alerts for two release cycles, and iterate thresholds based on observed outcomes.

## Required Deliverables
- Capability contract: input schema, deterministic scoring, output schema, and failure modes.
- Runtime profile: planning-router using dependency graph compilation to produce validated workflow DAGs.
- Orchestration integration: healthcare-and-public-services:planning-router routing, approval gates, retries, and rollback controls.
- Validation evidence: unit, integration, simulation, regression-baseline suites and rollout telemetry.

## Operational Runbook
### Preflight
- Confirm the PublicService Dependency DAG Planner request scope, source evidence, and measurable success criteria before execution.
- Verify feature flag skill_0408_publicservice-dependency-dag-pla, approval gates, and rollback owner before autonomous use.

### Execution
- Execute dependency graph compilation with deterministic scoring and reproducible trace capture.
- Produce validated workflow DAGs plus scorecard, assumptions, and unresolved-risk notes.

### Recovery
- Fail closed when required signals, evidence, or approval gates are missing.
- Rollback to the last stable baseline when posture is critical or validation fails.

### Handoff
- Publish validated workflow DAGs, validation evidence, and telemetry links to downstream owners.
- Queue follow-up tasks for unresolved risks, threshold tuning, or approval review.

## Guardrails
- [quality] Require deterministic scoring and validation evidence before promotion.
- [reliability] Preserve retries, rollback controls, and failure-mode evidence for every run.
- [safety] Route critical posture or missing approval gates to human review before autonomous action.
