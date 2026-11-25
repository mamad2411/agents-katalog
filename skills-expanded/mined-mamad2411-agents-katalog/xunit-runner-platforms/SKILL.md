---
name: xunit-runner-platforms
description: Use when xUnit execution must be standardized across local and CI environments with deterministic runner selection, adapter behavior, and result contracts.
---

# xUnit Runner Platforms

## Specialization

Use this skill to choose and standardize xUnit test runner strategy across .NET CLI, IDEs, and CI pipelines.

This skill is specialized for runner/platform decisions and parity checks. It does not author product tests.

## Objective

Produce one deterministic runner-platform contract that defines platform choice, configuration posture, discovery behavior, and result-output compatibility.

## Trigger Conditions

- Test runs differ between local machines and CI.
- Teams are choosing between Microsoft.Testing.Platform and VSTest.
- Test discovery, filtering, or result formats are inconsistent.

## Scope Boundaries

In scope:

- Runner platform decision and rationale.
- xUnit adapter and discovery behavior expectations.
- Local/CI parity checks for filters, categories, and outputs.
- Result format contract for downstream gates.

Out of scope:

- CI provider-specific deployment workflows.
- Framework migration implementation beyond runner posture.
- Non-.NET test platform operations.

## Inputs

- Target repository runtime and SDK constraints.
- Current local and CI test commands.
- Required result consumers (dashboards, gates, reporting).
- Evaluation date in ISO format (`YYYY-MM-DD`) for source freshness checks.

## Required Outputs

- Runner-platform decision record.
- Command parity matrix (local vs CI).
- Discovery/filter compatibility checklist.
- Result-output contract and known limitations.
- Final recommendation with residual risk notes.

## Deterministic Workflow

1. Collect current execution commands and result consumers.
2. Evaluate platform options against compatibility and maintainability needs.
3. Select one primary runner strategy and one fallback posture.
4. Define command parity rules for local and CI usage.
5. Define result-output contract and validation checks.
6. Publish one recommendation and unresolved compatibility risks.

## Decision Rules

- Prefer one primary platform per repository to reduce execution ambiguity.
- Require explicit parity checks for discovery, filtering, and output formats.
- Fail closed when result consumers cannot parse emitted artifacts.

## L4 Coverage Matrix

| Requested Outcome | Skill Section |
|---|---|
| Expert runner selection | Deterministic Workflow |
| Deterministic platform parity | Required Outputs |
| Stable evidence outputs | Decision Rules + Required Outputs |
| Cross-project reusability | Scope Boundaries + Pragmatic Stop Rule |

## Reasoning Package

Assumptions:

- A single runner strategy lowers long-term maintenance overhead.
- Evidence contracts are as important as command success.

Trade-offs:

- Newer platforms improve forward compatibility but may require migration effort.
- Legacy compatibility can reduce short-term friction but preserve inconsistency risk.

Open blockers:

- Unknown reporting consumers may invalidate output decisions.
- Mixed SDK constraints can force temporary dual-path support.

Recommendation:

- Standardize on one primary runner strategy and encode a strict parity contract for local and CI execution.

## Source Governance Summary

- Active sources and evaluation status are tracked in [source-catalog.md](./references/source-catalog.md).
- Execution contract template is provided in [runner-platform-contract-template.md](./references/runner-platform-contract-template.md).

## Pragmatic Stop Rule

Stop when one primary runner is selected, parity checks are explicit, and result outputs are contract-validated.

## Done Criteria

- Trigger conditions are satisfied.
- Required outputs are complete.
- Platform and output decisions are explicit.
- Source catalog is current for this evaluation cycle.
