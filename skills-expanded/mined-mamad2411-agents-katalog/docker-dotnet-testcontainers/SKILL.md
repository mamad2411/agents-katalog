---
name: docker-dotnet-testcontainers
description: Use when implementing containerized integration tests for .NET services with Testcontainers, including fixture lifecycle, deterministic startup, and CI execution patterns.
---

# Docker .NET Testcontainers

## Specialization

Provide repeatable Testcontainers guidance for .NET integration tests so containerized dependencies are deterministic across local and CI runs.

## Trigger Conditions

- .NET integration tests require ephemeral container dependencies.
- Existing integration tests are flaky due to manual service setup.
- CI needs deterministic containerized test behavior.

## Scope Boundaries

In scope:

- Testcontainers fixture and lifecycle patterns.
- Deterministic startup and readiness checks.
- CI execution guidance for containerized tests.

Out of scope:

- Full application functional test strategy.
- Non-.NET test frameworks.

## Required Inputs

- Test target dependencies (database, queue, service emulators).
- Test runner and CI environment details.
- Timing and stability constraints.

## Required Outputs

- Integration test fixture pattern.
- Container lifecycle and readiness guidance.
- Reusable example, template, and script.

## Deterministic Workflow

1. Define dependency containers and readiness checks.
2. Implement shared fixture lifecycle.
3. Isolate test state and cleanup deterministically.
4. Run tests locally and in CI with consistent settings.
5. Capture flake and startup timing observations.

## Decision Rules

- Prefer shared fixtures per test class/collection for expensive dependencies.
- Require explicit readiness checks before test execution.
- Ensure cleanup paths are deterministic.

## Anti-Pattern Checks

- Tests depend on ambient locally installed services.
- Container startup is assumed without readiness validation.
- Cleanup is skipped on failures.

## Self-Contained Assets

- Sample code: [postgres-fixture.example.cs](./references/examples/postgres-fixture.example.cs)
- Sample configuration: [testcontainers-ci.sample.yaml](./references/templates/config/testcontainers-ci.sample.yaml)
- Template: [integration-test-checklist-template.md](./references/templates/integration-test-checklist-template.md)
- Script: [run-testcontainers-tests.ps1](./references/scripts/run-testcontainers-tests.ps1)

## Done Criteria

- Fixture pattern and lifecycle guidance are explicit.
- Deterministic startup and cleanup checks exist.
- Reusable assets are included.

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
