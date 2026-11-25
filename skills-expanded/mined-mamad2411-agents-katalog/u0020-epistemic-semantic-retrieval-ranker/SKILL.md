---
name: u0020-epistemic-semantic-retrieval-ranker
description: Build and operate the "Epistemic Semantic Retrieval Ranker" capability for Truth-Seeking and Epistemics. Trigger when this exact capability is needed in mission execution.
---

# Epistemic Semantic Retrieval Ranker

## Why This Skill Exists
We need this skill because decisions drift when claims are accepted without verification. This specific skill improves recall precision for downstream decision quality.

## When To Use
Use this skill when the request explicitly needs "Epistemic Semantic Retrieval Ranker" outcomes in the Truth-Seeking and Epistemics domain.

## Step-by-Step Implementation Guide
1. Define the scope and success metrics for `Epistemic Semantic Retrieval Ranker`, including at least three measurable KPIs tied to false certainty and unverified assumptions.
2. Design and version the input/output contract for claims, evidence, and confidence traces, then add schema validation and failure-mode handling.
3. Implement the core capability using semantic relevance scoring, and produce ranked retrieval results with deterministic scoring.
4. Integrate the skill into swarm orchestration: task routing, approval gates, retry strategy, and rollback controls.
5. Add unit, integration, and simulation tests that explicitly cover false certainty and unverified assumptions, then run regression baselines.
6. Deploy behind a feature flag, monitor telemetry/alerts for two release cycles, and iterate thresholds based on observed outcomes.

## Required Deliverables
- Capability contract: input schema, deterministic scoring, output schema, and failure modes.
- Runtime profile: planning-router using semantic relevance scoring to produce ranked retrieval results.
- Orchestration integration: truth-seeking-and-epistemics:planning-router routing, approval gates, retries, and rollback controls.
- Validation evidence: unit, integration, simulation, regression-baseline suites and rollout telemetry.

## Operational Runbook
### Preflight
- Confirm the Epistemic Semantic Retrieval Ranker request scope, source evidence, and measurable success criteria before execution.
- Verify feature flag skill_0020_epistemic-semantic-retrieval-ran, approval gates, and rollback owner before autonomous use.

### Execution
- Execute semantic relevance scoring with deterministic scoring and reproducible trace capture.
- Produce ranked retrieval results plus scorecard, assumptions, and unresolved-risk notes.

### Recovery
- Fail closed when required signals, evidence, or approval gates are missing.
- Rollback to the last stable baseline when posture is critical or validation fails.

### Handoff
- Publish ranked retrieval results, validation evidence, and telemetry links to downstream owners.
- Queue follow-up tasks for unresolved risks, threshold tuning, or approval review.

## Guardrails
- [quality] Require deterministic scoring and validation evidence before promotion.
- [reliability] Preserve retries, rollback controls, and failure-mode evidence for every run.
- [safety] Route critical posture or missing approval gates to human review before autonomous action.
