---
name: u0484-research-contradiction-detector
description: Build and operate the "Research Contradiction Detector" capability for Scientific Research Systems. Trigger when this exact capability is needed in mission execution.
---

# Research Contradiction Detector

## Why This Skill Exists
We need this skill because research throughput degrades without reproducibility and prioritization. This specific skill catches internal and external claim conflicts early.

## When To Use
Use this skill when the request explicitly needs "Research Contradiction Detector" outcomes in the Scientific Research Systems domain.

## Step-by-Step Implementation Guide
1. Define the scope and success metrics for `Research Contradiction Detector`, including at least three measurable KPIs tied to non-reproducible results and wasted cycles.
2. Design and version the input/output contract for hypotheses, experiments, and replication evidence, then add schema validation and failure-mode handling.
3. Implement the core capability using cross-claim consistency checks, and produce contradiction alerts with deterministic scoring.
4. Integrate the skill into swarm orchestration: task routing, approval gates, retry strategy, and rollback controls.
5. Add unit, integration, and simulation tests that explicitly cover non-reproducible results and wasted cycles, then run regression baselines.
6. Deploy behind a feature flag, monitor telemetry/alerts for two release cycles, and iterate thresholds based on observed outcomes.

## Required Deliverables
- Capability contract: input schema, deterministic scoring, output schema, and failure modes.
- Runtime profile: detection-guard using cross-claim consistency checks to produce contradiction alerts.
- Orchestration integration: scientific-research-systems:detection-guard routing, approval gates, retries, and rollback controls.
- Validation evidence: unit, integration, simulation, regression-baseline suites and rollout telemetry.

## Operational Runbook
### Preflight
- Confirm the Research Contradiction Detector request scope, source evidence, and measurable success criteria before execution.
- Verify feature flag skill_0484_research-contradiction-detector, approval gates, and rollback owner before autonomous use.

### Execution
- Execute cross-claim consistency checks with deterministic scoring and reproducible trace capture.
- Produce contradiction alerts plus scorecard, assumptions, and unresolved-risk notes.

### Recovery
- Fail closed when required signals, evidence, or approval gates are missing.
- Rollback to the last stable baseline when posture is critical or validation fails.

### Handoff
- Publish contradiction alerts, validation evidence, and telemetry links to downstream owners.
- Queue follow-up tasks for unresolved risks, threshold tuning, or approval review.

## Guardrails
- [quality] Require deterministic scoring and validation evidence before promotion.
- [reliability] Preserve retries, rollback controls, and failure-mode evidence for every run.
- [safety] Route critical posture or missing approval gates to human review before autonomous action.
