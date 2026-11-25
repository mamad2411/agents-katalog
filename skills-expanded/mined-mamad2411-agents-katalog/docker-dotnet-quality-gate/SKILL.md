---
name: docker-dotnet-quality-gate
description: Use when Docker .NET changes need an evidence-first quality decision covering correctness, security, performance, testability, and release readiness before merge or promotion.
---

# Docker .NET Quality Gate

## Specialization

Provide a deterministic, severity-based quality decision process for Docker .NET changes before merge or promotion.

## Trigger Conditions

- A Docker .NET implementation is ready for review.
- Promotion decisions need explicit go or no-go evidence.
- Findings must be severity-tagged with remediation ownership.

## Scope Boundaries

In scope:

- Gate evaluation rubric and required evidence references.
- Severity-tagged findings and disposition output.
- Rollback and release evidence checks.

Out of scope:

- Implementing product fixes directly.
- Full platform release orchestration beyond container scope.

## Required Inputs

- Changed Docker skill/artifact set.
- Test, scan, and build evidence bundle.
- Release and rollback references.

## Required Outputs

- Findings table with severity and ownership.
- Quality decision: pass, conditional pass, fail.
- Explicit remediation actions for unresolved findings.

## Deterministic Workflow

1. Validate evidence bundle completeness.
2. Evaluate artifacts against gate checklist.
3. Record findings with severity and owner.
4. Determine disposition using decision rules.
5. Publish closure status and next actions.

## Decision Rules

- Fail when any unresolved High finding exists.
- Conditional pass only when Medium findings have approved remediation owners and due dates.
- Pass only when no unresolved High findings remain and evidence is complete.

## Anti-Pattern Checks

- Gate decision without evidence references.
- Findings without owner or due date.
- Implicit approval from chat history without artifact evidence.

## Self-Contained Assets

- Sample code: [findings-table.example.md](./references/examples/findings-table.example.md)
- Sample configuration: [quality-thresholds.sample.yaml](./references/templates/config/quality-thresholds.sample.yaml)
- Template: [quality-gate-report-template.md](./references/templates/quality-gate-report-template.md)
- Script: [validate-quality-evidence.ps1](./references/scripts/validate-quality-evidence.ps1)

## Done Criteria

- Findings are severity-tagged and owned.
- Disposition is explicit and traceable to evidence artifacts.
- Remediation actions are traceable.

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
