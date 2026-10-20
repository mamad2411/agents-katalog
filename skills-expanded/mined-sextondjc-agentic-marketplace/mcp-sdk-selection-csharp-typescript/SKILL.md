---
name: mcp-sdk-selection-csharp-typescript
description: Use when MCP implementation must choose between C# and TypeScript SDKs using deterministic runtime and delivery criteria.
---

# MCP SDK Selection (C# and TypeScript)

## Specialization

Produce deterministic SDK selection decisions for MCP server implementation across C# and TypeScript only.

## Trigger Conditions

- A team needs to select the MCP SDK before implementation.
- Multiple runtime and hosting constraints exist.
- A cross-project standard needs a reusable selection rubric.

## Hard Constraints

- Only C# and TypeScript SDKs are in scope.
- Use official sources only.

## Inputs

- Target runtime environment.
- Hosting model and deployment constraints.
- Team language proficiency and existing platform stack.
- Operability and CI/CD constraints.

## Required Outputs

- Decision matrix with weighted criteria.
- Recommended SDK with rationale.
- Rejected option notes and risk impacts.

## Deterministic Workflow

1. Capture runtime and hosting requirements.
2. Score C# and TypeScript options by criteria.
3. Identify blockers per option.
4. Select one recommendation.
5. Publish fallback path and migration risks.

## Selection Matrix Template

| Criterion | Weight | C# Score | TypeScript Score | Notes |
|---|---:|---:|---:|---|
| Platform fit | 5 | <1-5> | <1-5> | <notes> |
| Team capability | 4 | <1-5> | <1-5> | <notes> |
| Deployment model fit | 4 | <1-5> | <1-5> | <notes> |
| CI/CD compatibility | 3 | <1-5> | <1-5> | <notes> |

## Done Criteria

- Matrix is complete and evidence-backed.
- One SDK recommendation is explicit.
- Rejected option risks are documented.
