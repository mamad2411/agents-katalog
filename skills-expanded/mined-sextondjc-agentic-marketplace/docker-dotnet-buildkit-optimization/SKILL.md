---
name: docker-dotnet-buildkit-optimization
description: Use when optimizing Docker build performance for .NET workloads using BuildKit, cache strategy, layer design, and reproducible build controls.
---

# Docker .NET BuildKit Optimization

## Specialization

Optimize .NET container build performance and repeatability through BuildKit features, layer strategy, and cache-aware Dockerfile design.

## Trigger Conditions

- Docker builds are slow or unstable.
- Teams need reproducible cache behavior across local and CI environments.
- Build pipelines require lower image build latency.

## Scope Boundaries

In scope:

- BuildKit adoption and cache strategy for .NET builds.
- Layer ordering and invalidation controls.
- Buildx usage patterns for reproducibility.

Out of scope:

- Baseline container hardening rules not specific to build performance.
- Registry release workflows and promotion governance.

## Required Inputs

- Build environment (local, CI, both).
- Current Dockerfile and cache pain points.
- Target optimization metric (build time, cache hit rate, image size).

## Required Outputs

- Optimized Dockerfile pattern.
- BuildKit and buildx configuration example.
- Cache strategy recommendation.
- Validation script and checklist template.

## Deterministic Workflow

1. Measure current build timing and identify layer invalidation hotspots.
2. Enable BuildKit and choose cache strategy.
3. Reorder Dockerfile layers for stable cache hits.
4. Add buildx command pattern for repeatable builds.
5. Validate improvement and record optimization evidence.

## Decision Rules

- Always separate restore and publish layers where possible.
- Use BuildKit cache mounts for package restore workloads.
- Avoid copying full source tree before dependency restore when unnecessary.
- Record baseline versus optimized metrics before promotion.

## Anti-Pattern Checks

- Layer ordering that invalidates cache on minor source changes.
- No BuildKit usage in CI despite high build frequency.
- Build optimization claims without baseline comparison evidence.

## Self-Contained Assets

- Sample code: [buildkit-optimized.Dockerfile](./references/examples/buildkit-optimized.Dockerfile)
- Sample configuration: [buildx-command.sample.yaml](./references/templates/config/buildx-command.sample.yaml)
- Template: [build-optimization-checklist-template.md](./references/templates/build-optimization-checklist-template.md)
- Script: [measure-build-time.ps1](./references/scripts/measure-build-time.ps1)

## Done Criteria

- BuildKit optimization path is explicit.
- Cache strategy and layer ordering guidance are output.
- Validation artifact for before/after timing exists.
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
