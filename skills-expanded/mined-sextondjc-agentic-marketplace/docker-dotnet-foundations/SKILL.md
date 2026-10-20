---
name: docker-dotnet-foundations
description: Use when establishing baseline Docker and OCI patterns for .NET services, including Dockerfile defaults, dockerignore hygiene, runtime hardening, and portability constraints.
---

# Docker .NET Foundations

## Specialization

Provide baseline containerization guidance for .NET services that is secure-by-default, portable, and reusable across projects.

## Trigger Conditions

- A .NET service needs first-time Dockerization.
- Existing Dockerfiles need baseline hardening and standardization.
- Teams need reusable foundation templates before optimization work.

## Scope Boundaries

In scope:

- Baseline Dockerfile structure for .NET workloads.
- Runtime hardening defaults for containers.
- Docker context hygiene and portability baseline.

Out of scope:

- Advanced BuildKit tuning.
- Deep CI/CD orchestration.
- Cluster orchestration design.

## Required Inputs

- .NET workload type (ASP.NET, worker, console, AOT).
- Target runtime and base image policy.
- Security expectations for runtime user and secrets handling.

## Required Outputs

- Baseline Dockerfile recommendation and rationale.
- Docker context and ignore strategy.
- Security baseline checks.
- Reusable templates and script for baseline validation.

## Deterministic Workflow

1. Identify workload shape and runtime target.
2. Select base image and multi-stage baseline.
3. Apply non-root runtime and secret-hygiene rules.
4. Apply dockerignore and context minimization checks.
5. Output baseline artifacts and validation script result.

## Decision Rules

- Prefer official .NET runtime images and pinned major/minor tags.
- Require multi-stage builds for production images.
- Require non-root runtime unless a justified exception is recorded.
- Never embed secrets in Dockerfile layers.

## Anti-Pattern Checks

- Single-stage production image that includes SDK toolchain.
- Runtime container executes as root without documented exception.
- Broad copy context without dockerignore controls.
- Hardcoded secrets or credentials in build layers.

## Self-Contained Assets

- Sample code: [aspnet-api.Dockerfile](./references/examples/aspnet-api.Dockerfile)
- Sample configuration: [dockerignore.template](./references/templates/config/dockerignore.template)
- Template: [docker-baseline-checklist-template.md](./references/templates/docker-baseline-checklist-template.md)
- Script: [validate-docker-baseline.ps1](./references/scripts/validate-docker-baseline.ps1)

## Done Criteria

- Baseline Dockerfile guidance is output.
- Hardening checks are explicit.
- Self-contained assets are provided.
- Source references are current.

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
