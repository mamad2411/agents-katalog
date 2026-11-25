---
name: u0140-tooling-semantic-retrieval-ranker
description: Build and operate the "Tooling Semantic Retrieval Ranker" capability for Tool Reliability and Execution Quality. Trigger when this exact capability is needed in mission execution.
---

# Tooling Semantic Retrieval Ranker

## Why This Skill Exists
We need this skill because automation collapses when tools are flaky and failure modes are opaque. This specific skill improves recall precision for downstream decision quality.

## When To Use
Use this skill when the request explicitly needs "Tooling Semantic Retrieval Ranker" outcomes in the Tool Reliability and Execution Quality domain.

## Step-by-Step Implementation Guide
1. Define the scope and success metrics for `Tooling Semantic Retrieval Ranker`, including at least three measurable KPIs tied to silent failures and cascading retries.
2. Design and version the input/output contract for tool runs, error signatures, and retry outcomes, then add schema validation and failure-mode handling.
3. Implement the core capability using semantic relevance scoring, and produce ranked retrieval results with deterministic scoring.
4. Integrate the skill into swarm orchestration: task routing, approval gates, retry strategy, and rollback controls.
5. Add unit, integration, and simulation tests that explicitly cover silent failures and cascading retries, then run regression baselines.
6. Deploy behind a feature flag, monitor telemetry/alerts for two release cycles, and iterate thresholds based on observed outcomes.

## Required Deliverables
- Capability contract: input schema, deterministic scoring, output schema, and failure modes.
- Runtime profile: planning-router using semantic relevance scoring to produce ranked retrieval results.
- Orchestration integration: tool-reliability-and-execution-quality:planning-router routing, approval gates, retries, and rollback controls.
- Validation evidence: unit, integration, simulation, regression-baseline suites and rollout telemetry.

## Operational Runbook
### Preflight
- Confirm the Tooling Semantic Retrieval Ranker request scope, source evidence, and measurable success criteria before execution.
- Verify feature flag skill_0140_tooling-semantic-retrieval-ranke, approval gates, and rollback owner before autonomous use.

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
