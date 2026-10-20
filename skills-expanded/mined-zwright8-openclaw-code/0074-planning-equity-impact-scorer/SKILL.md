---
name: u0074-planning-equity-impact-scorer
description: Build and operate the "Planning Equity Impact Scorer" capability for Strategic Planning and Decomposition. Trigger when this exact capability is needed in mission execution.
---

# Planning Equity Impact Scorer

## Why This Skill Exists
We need this skill because large goals fail when decomposition is inconsistent or incomplete. This specific skill exposes uneven benefit/harm distribution before rollout.

## When To Use
Use this skill when the request explicitly needs "Planning Equity Impact Scorer" outcomes in the Strategic Planning and Decomposition domain.

## Step-by-Step Implementation Guide
1. Define the scope and success metrics for `Planning Equity Impact Scorer`, including at least three measurable KPIs tied to execution stalls and hidden dependency failures.
2. Design and version the input/output contract for goals, dependencies, milestones, and constraints, then add schema validation and failure-mode handling.
3. Implement the core capability using group-level impact scoring, and produce equity impact profiles with deterministic scoring.
4. Integrate the skill into swarm orchestration: task routing, approval gates, retry strategy, and rollback controls.
5. Add unit, integration, and simulation tests that explicitly cover execution stalls and hidden dependency failures, then run regression baselines.
6. Deploy behind a feature flag, monitor telemetry/alerts for two release cycles, and iterate thresholds based on observed outcomes.

## Required Deliverables
- Capability contract: input schema, deterministic scoring, output schema, and failure modes.
- Runtime profile: general-capability using group-level impact scoring to produce equity impact profiles.
- Orchestration integration: strategic-planning-and-decomposition:general-capability routing, approval gates, retries, and rollback controls.
- Validation evidence: unit, integration, simulation, regression-baseline suites and rollout telemetry.

## Operational Runbook
### Preflight
- Confirm the Planning Equity Impact Scorer request scope, source evidence, and measurable success criteria before execution.
- Verify feature flag skill_0074_planning-equity-impact-scorer, approval gates, and rollback owner before autonomous use.

### Execution
- Execute group-level impact scoring with deterministic scoring and reproducible trace capture.
- Produce equity impact profiles plus scorecard, assumptions, and unresolved-risk notes.

### Recovery
- Fail closed when required signals, evidence, or approval gates are missing.
- Rollback to the last stable baseline when posture is critical or validation fails.

### Handoff
- Publish equity impact profiles, validation evidence, and telemetry links to downstream owners.
- Queue follow-up tasks for unresolved risks, threshold tuning, or approval review.

## Guardrails
- [quality] Require deterministic scoring and validation evidence before promotion.
- [reliability] Preserve retries, rollback controls, and failure-mode evidence for every run.
- [safety] Route critical posture or missing approval gates to human review before autonomous action.
