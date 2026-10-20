---
name: docker-dotnet-compose-workflows
description: Use when defining Docker Compose workflows for .NET services across local development and CI parity, including dependency wiring, environment overrides, and validation checks.
---

# Docker .NET Compose Workflows

## Specialization

Define reliable Docker Compose patterns for .NET services so local and CI environments share consistent service topology and startup behavior.

## Trigger Conditions

- .NET services need local multi-container development.
- Teams need consistent compose behavior between local and CI.
- Existing compose files need standardization and environment layering.

## Scope Boundaries

In scope:

- Compose service definitions and dependency wiring.
- Environment overrides and variable strategy.
- Validation commands and workflow scripts.

Out of scope:

- Production orchestrator deployment design.
- Deep security scanning or SBOM policy logic.

## Required Inputs

- Services and dependencies to compose.
- Environment variable and secret handling expectations.
- Local and CI execution constraints.

## Required Outputs

- Compose baseline and override guidance.
- Environment template and validation commands.
- Reusable compose templates and automation script.

## Deterministic Workflow

1. Map service topology and dependency graph.
2. Define base compose contract and optional overrides.
3. Apply environment variable policy without hardcoded secrets.
4. Validate startup and service health behavior.
5. Publish reusable templates and run script.

## Decision Rules

- Keep base compose file environment-agnostic.
- Use override files for local-only variations.
- Keep secrets out of committed compose files.
- Ensure dependency ordering is explicit.

## Anti-Pattern Checks

- One compose file mixing local and CI-only behavior without layering.
- Hardcoded credentials in environment fields.
- Missing health checks for dependent services.

## Self-Contained Assets

- Sample code: [compose.base.yaml](./references/examples/compose.base.yaml)
- Sample configuration: [compose.override.sample.yaml](./references/templates/config/compose.override.sample.yaml)
- Template: [compose-validation-checklist-template.md](./references/templates/compose-validation-checklist-template.md)
- Script: [run-compose-smoke.ps1](./references/scripts/run-compose-smoke.ps1)

## Done Criteria

- Base and override compose strategy is clear.
- Environment and secret policies are explicit.
- Reusable assets are present and source-backed.

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
