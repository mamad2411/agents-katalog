---
name: docker-dotnet-runtime-diagnostics
description: Use when diagnosing .NET container startup, health, configuration, logging, networking, or filesystem failures with deterministic evidence capture and recovery guidance.
---

# Docker .NET Runtime Diagnostics

## Specialization

Diagnose .NET container runtime failures with deterministic evidence capture so startup, healthcheck, configuration, port-binding, permission, and process issues can be isolated quickly.

## Trigger Conditions

- A .NET container fails to start, stay healthy, or respond as expected.
- Teams need a repeatable evidence-capture flow for runtime issues.
- Container logs, inspect output, or health state need structured interpretation.

## Scope Boundaries

In scope:

- Runtime failure triage and evidence capture.
- Healthcheck, environment, networking, and filesystem diagnostics.
- Structured recovery guidance and residual-risk reporting.

Out of scope:

- Product code debugging unrelated to container execution context.
- Cluster-level observability or orchestration debugging.

## Required Inputs

- Failing container name, image tag, or compose service.
- Observed failure mode and available logs.
- Local, CI, or remote reproduction context.

## Required Outputs

- Diagnostics evidence set and failure summary.
- Likely root-cause classification.
- Recovery steps, validation checklist, and evidence script.

## Deterministic Workflow

1. Capture failure mode, reproduction context, and last-known-good state.
2. Gather logs, inspect output, health status, and environment evidence.
3. Classify failure into startup, config, network, permission, or dependency buckets.
4. Propose recovery steps and validate the chosen fix path.
5. Publish residual risks and follow-up checks.

## Decision Rules

- Evidence capture must precede conclusion or remediation claims.
- Healthcheck failures require both container-state and dependency-state inspection.
- Environment or secret mismatches must be reported without exposing sensitive values.
- If reproduction is non-deterministic, record the ambiguity explicitly.

## Anti-Pattern Checks

- Root-cause claim without logs or inspect evidence.
- Secret values copied into diagnostics artifacts.
- Startup issue declared fixed without rerunning the failing container path.

## Self-Contained Assets

- Sample code: [runtime-diagnostics-report.example.md](./references/examples/runtime-diagnostics-report.example.md)
- Sample configuration: [diagnostics-capture.sample.yaml](./references/templates/config/diagnostics-capture.sample.yaml)
- Template: [runtime-diagnostics-checklist-template.md](./references/templates/runtime-diagnostics-checklist-template.md)
- Script: [collect-runtime-diagnostics.ps1](./references/scripts/collect-runtime-diagnostics.ps1)

## Done Criteria

- Evidence set is explicit and reproducible.
- Failure classification and recovery path are documented.
- Validation confirms the runtime path after remediation.

## Inputs

- Request objective and scope boundary.
- Applicable constraints and risk context.

## Workflow

1. Capture inputs and constraints.
2. Execute this skill's deterministic steps.
3. Publish outputs with status and next actions.

## Execution Context
### Input Context

- Request objective and scope boundary.
- Applicable constraints and required outputs.

### Process Context

- Follow this skill's deterministic workflow from intake to closure.
- Record ownership and decisions for required outputs.

### Output Context

- Deliverables with explicit completion status.
- Residual risks and next actions.

## References Assets

- [Reference assets](./references/README.md)
