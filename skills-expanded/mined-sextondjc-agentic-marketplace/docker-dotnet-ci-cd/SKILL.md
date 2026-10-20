---
name: docker-dotnet-ci-cd
description: Use when implementing CI/CD pipelines for .NET container workflows including build, scan, SBOM, tag strategy, publish gates, and release evidence.
---

# Docker .NET CI/CD

## Specialization

Define deterministic CI/CD workflows for .NET container delivery, from build and security gates to publish and release evidence.

## Trigger Conditions

- Teams need standardized container pipeline flow.
- Build/scan/publish rules must be codified as reusable templates.
- Releases require explicit evidence and rollback references.

## Scope Boundaries

In scope:

- Build, scan, and publish sequencing.
- Tagging and artifact strategy guidance.
- Gate criteria and release evidence templates.

Out of scope:

- Environment-specific deployment topology design.
- Runtime incident response playbooks.

## Required Inputs

- Registry target and authentication method.
- Promotion policy and gate thresholds.
- Branch/tag strategy for release candidates.

## Required Outputs

- CI/CD workflow contract and template.
- Tagging strategy and gate checklist.
- Reusable scripts and sample configuration with evidence linkage points.

## Deterministic Workflow

1. Build and tag image with traceable metadata.
2. Run security and SBOM gates.
3. Enforce threshold-based pass/fail rules.
4. Publish image only when gates pass.
5. Record release evidence and rollback reference.

## Decision Rules

- Use immutable image tags for release artifacts.
- Require security scans and SBOM before publish.
- Fail closed when gate evidence is missing.

## Anti-Pattern Checks

- Publish step runs before security gates.
- Mutable latest-only tagging without immutable release tag.
- Missing release evidence linkage.

## Self-Contained Assets

- Sample code: [github-actions-workflow.example.yml](./references/examples/github-actions-workflow.example.yml)
- Sample configuration: [tagging-policy.sample.yaml](./references/templates/config/tagging-policy.sample.yaml)
- Template: [pipeline-gate-checklist-template.md](./references/templates/pipeline-gate-checklist-template.md)
- Script: [run-ci-gates.ps1](./references/scripts/run-ci-gates.ps1)

## Done Criteria

- Pipeline sequencing is explicit.
- Tagging and evidence policy is reusable.
- Self-contained assets are complete.

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
