---
name: docker-dotnet-security-supply-chain
description: Use when hardening .NET container images and enforcing supply-chain controls including non-root runtime, secret hygiene, vulnerability scanning, SBOM generation, and provenance checks.
---

# Docker .NET Security and Supply Chain

## Specialization

Apply security and supply-chain controls to .NET container workflows with deterministic policy gates and reusable evidence artifacts.

## Trigger Conditions

- .NET container workflows require hardened defaults.
- Teams need vulnerability and SBOM gating in CI.
- Promotion requires provenance-aware release evidence.

## Scope Boundaries

In scope:

- Runtime hardening defaults and anti-pattern checks.
- Vulnerability scanning and SBOM generation workflows.
- Provenance and release evidence guidance.

Out of scope:

- Full threat-modeling outside container delivery scope.
- Cluster-level runtime policy design.

## Required Inputs

- Risk tolerance and severity thresholds.
- Build and release pipeline context.
- Registry and artifact retention expectations.

## Required Outputs

- Security baseline controls for container images.
- Scan and SBOM workflow with pass/fail criteria.
- Reusable templates and scripts for evidence collection.

## Deterministic Workflow

1. Apply runtime hardening baseline.
2. Run vulnerability and misconfiguration scans.
3. Generate SBOM and attach to build evidence.
4. Evaluate gate thresholds and disposition.
5. Record provenance and release readiness notes.

## Decision Rules

- Require non-root runtime unless exception is documented.
- Treat critical vulnerabilities as fail by default.
- Generate SBOM for every release candidate image.
- Keep secrets out of images, layers, and logs.

## Anti-Pattern Checks

- Security gate bypass without approved exception.
- Scan run without artifact retention.
- Promotion decision without SBOM evidence.

## Self-Contained Assets

- Sample code: [trivy-scan-output.example.md](./references/examples/trivy-scan-output.example.md)
- Sample configuration: [trivy-policy.sample.yaml](./references/templates/config/trivy-policy.sample.yaml)
- Template: [security-gate-checklist-template.md](./references/templates/security-gate-checklist-template.md)
- Script: [run-security-gates.ps1](./references/scripts/run-security-gates.ps1)

## Done Criteria

- Security and supply-chain controls are explicit.
- Gate thresholds and evidence artifacts are defined.
- Reusable templates and scripts are available.

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
