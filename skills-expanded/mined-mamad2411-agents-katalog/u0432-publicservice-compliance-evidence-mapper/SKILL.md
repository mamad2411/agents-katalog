---
name: u0432-publicservice-compliance-evidence-mapper
description: Build and operate the "PublicService Compliance Evidence Mapper" capability for Healthcare and Public Services. Trigger when this exact capability is needed in mission execution.
---

# PublicService Compliance Evidence Mapper

## Why This Skill Exists
We need this skill because public-facing workflows require strict safety and reliability controls. This specific skill keeps proof of control coverage continuously current.

## When To Use
Use this skill when the request explicitly needs "PublicService Compliance Evidence Mapper" outcomes in the Healthcare and Public Services domain.

## Step-by-Step Implementation Guide
1. Define the scope and success metrics for `PublicService Compliance Evidence Mapper`, including at least three measurable KPIs tied to service harm and procedural violations.
2. Design and version the input/output contract for protocol checks, service queues, and compliance flags, then add schema validation and failure-mode handling.
3. Implement the core capability using requirement-to-evidence mapping, and produce compliance evidence matrices with deterministic scoring.
4. Integrate the skill into swarm orchestration: task routing, approval gates, retry strategy, and rollback controls.
5. Add unit, integration, and simulation tests that explicitly cover service harm and procedural violations, then run regression baselines.
6. Deploy behind a feature flag, monitor telemetry/alerts for two release cycles, and iterate thresholds based on observed outcomes.

## Required Deliverables
- Capability contract: input schema, deterministic scoring, output schema, and failure modes.
- Runtime profile: normalization-engine using requirement-to-evidence mapping to produce compliance evidence matrices.
- Orchestration integration: healthcare-and-public-services:normalization-engine routing, approval gates, retries, and rollback controls.
- Validation evidence: unit, integration, simulation, regression-baseline suites and rollout telemetry.

## Operational Runbook
### Preflight
- Confirm the PublicService Compliance Evidence Mapper request scope, source evidence, and measurable success criteria before execution.
- Verify feature flag skill_0432_publicservice-compliance-evidenc, approval gates, and rollback owner before autonomous use.

### Execution
- Execute requirement-to-evidence mapping with deterministic scoring and reproducible trace capture.
- Produce compliance evidence matrices plus scorecard, assumptions, and unresolved-risk notes.

### Recovery
- Fail closed when required signals, evidence, or approval gates are missing.
- Rollback to the last stable baseline when posture is critical or validation fails.

### Handoff
- Publish compliance evidence matrices, validation evidence, and telemetry links to downstream owners.
- Queue follow-up tasks for unresolved risks, threshold tuning, or approval review.

## Guardrails
- [quality] Require deterministic scoring and validation evidence before promotion.
- [reliability] Preserve retries, rollback controls, and failure-mode evidence for every run.
- [safety] Route critical posture or missing approval gates to human review before autonomous action.
