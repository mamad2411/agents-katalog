---
name: u0493-research-task-handoff-contractor
description: Build and operate the "Research Task Handoff Contractor" capability for Scientific Research Systems. Trigger when this exact capability is needed in mission execution.
---

# Research Task Handoff Contractor

## Why This Skill Exists
We need this skill because research throughput degrades without reproducibility and prioritization. This specific skill standardizes handoffs between agents and humans.

## When To Use
Use this skill when the request explicitly needs "Research Task Handoff Contractor" outcomes in the Scientific Research Systems domain.

## Step-by-Step Implementation Guide
1. Define the scope and success metrics for `Research Task Handoff Contractor`, including at least three measurable KPIs tied to non-reproducible results and wasted cycles.
2. Design and version the input/output contract for hypotheses, experiments, and replication evidence, then add schema validation and failure-mode handling.
3. Implement the core capability using contracted payload schemas, and produce typed handoff artifacts with deterministic scoring.
4. Integrate the skill into swarm orchestration: task routing, approval gates, retry strategy, and rollback controls.
5. Add unit, integration, and simulation tests that explicitly cover non-reproducible results and wasted cycles, then run regression baselines.
6. Deploy behind a feature flag, monitor telemetry/alerts for two release cycles, and iterate thresholds based on observed outcomes.

## Required Deliverables
- Capability contract: input schema, deterministic scoring, output schema, and failure modes.
- Runtime profile: contract-compiler using contracted payload schemas to produce typed handoff artifacts.
- Orchestration integration: scientific-research-systems:contract-compiler routing, approval gates, retries, and rollback controls.
- Validation evidence: unit, integration, simulation, regression-baseline suites and rollout telemetry.

## Operational Runbook
### Preflight
- Confirm the Research Task Handoff Contractor request scope, source evidence, and measurable success criteria before execution.
- Verify feature flag skill_0493_research-task-handoff-contractor, approval gates, and rollback owner before autonomous use.

### Execution
- Execute contracted payload schemas with deterministic scoring and reproducible trace capture.
- Produce typed handoff artifacts plus scorecard, assumptions, and unresolved-risk notes.

### Recovery
- Fail closed when required signals, evidence, or approval gates are missing.
- Rollback to the last stable baseline when posture is critical or validation fails.

### Handoff
- Publish typed handoff artifacts, validation evidence, and telemetry links to downstream owners.
- Queue follow-up tasks for unresolved risks, threshold tuning, or approval review.

## Guardrails
- [quality] Require deterministic scoring and validation evidence before promotion.
- [reliability] Preserve retries, rollback controls, and failure-mode evidence for every run.
- [safety] Route critical posture or missing approval gates to human review before autonomous action.
