---
name: u0311-federation-security-threat-modeler
description: Build and operate the "Federation Security Threat Modeler" capability for Federation and Interoperability. Trigger when this exact capability is needed in mission execution.
---

# Federation Security Threat Modeler

## Why This Skill Exists
We need this skill because cross-org collaboration fails without shared contracts and trust primitives. This specific skill anticipates attack paths before adversaries exploit them.

## When To Use
Use this skill when the request explicitly needs "Federation Security Threat Modeler" outcomes in the Federation and Interoperability domain.

## Step-by-Step Implementation Guide
1. Define the scope and success metrics for `Federation Security Threat Modeler`, including at least three measurable KPIs tied to integration breakage and trust boundary violations.
2. Design and version the input/output contract for envelopes, tenant boundaries, and protocol bridges, then add schema validation and failure-mode handling.
3. Implement the core capability using attack-surface modeling, and produce threat models with deterministic scoring.
4. Integrate the skill into swarm orchestration: task routing, approval gates, retry strategy, and rollback controls.
5. Add unit, integration, and simulation tests that explicitly cover integration breakage and trust boundary violations, then run regression baselines.
6. Deploy behind a feature flag, monitor telemetry/alerts for two release cycles, and iterate thresholds based on observed outcomes.

## Required Deliverables
- Capability contract: input schema, deterministic scoring, output schema, and failure modes.
- Runtime profile: detection-guard using attack-surface modeling to produce threat models.
- Orchestration integration: federation-and-interoperability:detection-guard routing, approval gates, retries, and rollback controls.
- Validation evidence: unit, integration, simulation, regression-baseline suites and rollout telemetry.

## Operational Runbook
### Preflight
- Confirm the Federation Security Threat Modeler request scope, source evidence, and measurable success criteria before execution.
- Verify feature flag skill_0311_federation-security-threat-model, approval gates, and rollback owner before autonomous use.

### Execution
- Execute attack-surface modeling with deterministic scoring and reproducible trace capture.
- Produce threat models plus scorecard, assumptions, and unresolved-risk notes.

### Recovery
- Fail closed when required signals, evidence, or approval gates are missing.
- Rollback to the last stable baseline when posture is critical or validation fails.

### Handoff
- Publish threat models, validation evidence, and telemetry links to downstream owners.
- Queue follow-up tasks for unresolved risks, threshold tuning, or approval review.

## Guardrails
- [quality] Require deterministic scoring and validation evidence before promotion.
- [reliability] Preserve retries, rollback controls, and failure-mode evidence for every run.
- [safety] Route critical posture or missing approval gates to human review before autonomous action.
