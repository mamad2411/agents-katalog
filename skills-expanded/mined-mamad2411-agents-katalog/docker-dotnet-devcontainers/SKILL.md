---
name: docker-dotnet-devcontainers
description: Use when defining VS Code devcontainer workflows for .NET repositories including containerized toolchains, feature selection, bind-mount strategy, onboarding parity, and inner-loop validation.
---

# Docker .NET Devcontainers

## Specialization

Provide deterministic devcontainer guidance for .NET repositories so development environments are portable, reproducible, and aligned with the expected local toolchain.

## Trigger Conditions

- Teams want containerized onboarding for .NET repositories.
- Local setup drift causes inconsistent developer environments.
- VS Code devcontainer configuration needs reusable defaults and validation rules.

## Scope Boundaries

In scope:

- Devcontainer structure and containerized toolchain guidance.
- Feature, mount, and workspace configuration patterns.
- Validation rules for onboarding and inner-loop parity.

Out of scope:

- Production Dockerfile and runtime release flows.
- IDE-specific guidance outside devcontainer-backed development.

## Required Inputs

- Repository type and expected .NET SDK/tooling surface.
- Local debugging, test, and package-manager expectations.
- Host/container mount and performance constraints.

## Required Outputs

- Devcontainer configuration recommendation.
- Feature and mount strategy guidance.
- Validation template, sample configuration, and setup script.

## Deterministic Workflow

1. Identify required SDK, CLI, and supporting toolchain components.
2. Define base image, features, and workspace mount strategy.
3. Configure post-create and validation steps for the .NET inner loop.
4. Validate debugging, restore, build, and test commands inside the container.
5. Publish onboarding notes and known host-specific constraints.

## Decision Rules

- Keep devcontainer configuration repository-portable and source-controlled.
- Prefer explicit features and setup commands over hidden manual prerequisites.
- Record mount or filesystem-performance exceptions when they affect the inner loop.
- Validate build and test basics inside the container before adopting the configuration.

## Anti-Pattern Checks

- Devcontainer requires undocumented host-side tools to function.
- Configuration depends on local absolute paths or personal credentials.
- Onboarding flow is declared complete without in-container build/test validation.

## Self-Contained Assets

- Sample code: [devcontainer.example.json](./references/examples/devcontainer.example.json)
- Sample configuration: [devcontainer-features.sample.yaml](./references/templates/config/devcontainer-features.sample.yaml)
- Template: [devcontainer-validation-checklist-template.md](./references/templates/devcontainer-validation-checklist-template.md)
- Script: [validate-devcontainer.ps1](./references/scripts/validate-devcontainer.ps1)

## Done Criteria

- Devcontainer structure and toolchain requirements are explicit.
- Validation covers restore, build, and test basics inside the container.
- Reusable onboarding assets are present.

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
