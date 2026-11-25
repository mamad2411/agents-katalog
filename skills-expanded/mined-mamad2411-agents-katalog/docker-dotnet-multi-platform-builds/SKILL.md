---
name: docker-dotnet-multi-platform-builds
description: Use when building and publishing .NET container images for multiple CPU architectures using buildx, manifest lists, RID alignment, and reproducible multi-platform release controls.
---

# Docker .NET Multi-Platform Builds

## Specialization

Define deterministic multi-platform container build patterns for .NET workloads so images for linux/amd64 and linux/arm64 are reproducible, traceable, and release-ready.

## Trigger Conditions

- Teams need one image tag to support multiple CPU architectures.
- Release pipelines must publish buildx manifest lists instead of single-arch images.
- .NET RID, native dependency, or AOT behavior changes across target platforms need explicit guidance.

## Scope Boundaries

In scope:

- buildx and manifest-list workflow design.
- Platform matrix and RID alignment for .NET workloads.
- Validation rules for multi-arch publish evidence.

Out of scope:

- Cluster scheduling and runtime placement policy.
- General BuildKit cache optimization not specific to multi-platform outputs.

## Required Inputs

- Target platform list.
- .NET workload type and RID constraints.
- Registry and release-tagging expectations.

## Required Outputs

- Multi-platform build workflow and command pattern.
- Platform matrix guidance with RID notes.
- Validation template, sample configuration, and publish script.

## Deterministic Workflow

1. Confirm required target platforms and release tag strategy.
2. Map workload type to platform-specific RID or native dependency constraints.
3. Define buildx builder and manifest-list publish flow.
4. Validate per-platform build success and merged manifest integrity.
5. Publish evidence showing platform coverage and residual risks.

## Decision Rules

- Publish immutable tags backed by manifest lists for release artifacts.
- Record platform support explicitly; do not imply unsupported architectures.
- Treat RID or native-library mismatch as a blocker until documented or fixed.
- Validate both build success and manifest inspection before release promotion.

## Anti-Pattern Checks

- Release tag points to a single-arch image when multi-platform support is expected.
- Platform claims are made without manifest inspection evidence.
- Native dependency or AOT constraints are ignored for non-amd64 builds.

## Self-Contained Assets

- Sample code: [github-actions-multi-platform.example.yml](./references/examples/github-actions-multi-platform.example.yml)
- Sample configuration: [platform-matrix.sample.yaml](./references/templates/config/platform-matrix.sample.yaml)
- Template: [multi-platform-release-checklist-template.md](./references/templates/multi-platform-release-checklist-template.md)
- Script: [build-multi-platform-image.ps1](./references/scripts/build-multi-platform-image.ps1)

## Done Criteria

- Platform matrix and manifest strategy are explicit.
- RID and native dependency constraints are captured.
- Validation assets exist for release evidence.

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
