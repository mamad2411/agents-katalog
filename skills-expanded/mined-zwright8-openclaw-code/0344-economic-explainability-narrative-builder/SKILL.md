---
name: u0344-economic-explainability-narrative-builder
description: Build and operate the "Economic Explainability Narrative Builder" capability for Economic Optimization. Trigger when this exact capability is needed in mission execution.
---

# Economic Explainability Narrative Builder

## Why This Skill Exists
We need this skill because missions need explicit tradeoff logic for cost, speed, and impact. This specific skill translates technical decisions into operator-usable narratives.

## When To Use
Use this skill when the request explicitly needs "Economic Explainability Narrative Builder" outcomes in the Economic Optimization domain.

## Step-by-Step Implementation Guide
1. Define the scope and success metrics for `Economic Explainability Narrative Builder`, including at least three measurable KPIs tied to overspending and low-impact allocation.
2. Design and version the input/output contract for budgets, costs, benefits, and opportunity values, then add schema validation and failure-mode handling.
3. Implement the core capability using reason synthesis and abstraction, and produce decision narratives with deterministic scoring.
4. Integrate the skill into swarm orchestration: task routing, approval gates, retry strategy, and rollback controls.
5. Add unit, integration, and simulation tests that explicitly cover overspending and low-impact allocation, then run regression baselines.
6. Deploy behind a feature flag, monitor telemetry/alerts for two release cycles, and iterate thresholds based on observed outcomes.

## Required Deliverables
- Capability contract: input schema, deterministic scoring, output schema, and failure modes.
- Runtime profile: communication-engine using reason synthesis and abstraction to produce decision narratives.
- Orchestration integration: economic-optimization:communication-engine routing, approval gates, retries, and rollback controls.
- Validation evidence: unit, integration, simulation, regression-baseline suites and rollout telemetry.

## Operational Runbook
### Preflight
- Confirm the Economic Explainability Narrative Builder request scope, source evidence, and measurable success criteria before execution.
- Verify feature flag skill_0344_economic-explainability-narrativ, approval gates, and rollback owner before autonomous use.

### Execution
- Execute reason synthesis and abstraction with deterministic scoring and reproducible trace capture.
- Produce decision narratives plus scorecard, assumptions, and unresolved-risk notes.

### Recovery
- Fail closed when required signals, evidence, or approval gates are missing.
- Rollback to the last stable baseline when posture is critical or validation fails.

### Handoff
- Publish decision narratives, validation evidence, and telemetry links to downstream owners.
- Queue follow-up tasks for unresolved risks, threshold tuning, or approval review.

## Guardrails
- [quality] Require deterministic scoring and validation evidence before promotion.
- [reliability] Preserve retries, rollback controls, and failure-mode evidence for every run.
- [safety] Route critical posture or missing approval gates to human review before autonomous action.
