---
name: mcp-contract-versioning
description: Use when MCP tool, resource, or prompt contracts must evolve with explicit backward-compatibility, deprecation, and promotion rules.
---

# MCP Contract Versioning

## Specialization

Evolve MCP contracts safely with deterministic compatibility and deprecation policy controls.

## Trigger Conditions

- Tool/resource/prompt schemas are changing.
- Backward compatibility risk is present.
- A release includes contract-breaking behavior.

## Hard Constraints

- Compatibility decisions must align with MCP specification behavior.
- Changes must include explicit migration and rollback notes.
- SDK references limited to C# and TypeScript guidance.

## Inputs

- Current and target contract definitions.
- Compatibility target (strict, additive-only, or controlled break).
- Consumer impact assessment.

## Required Outputs

- Contract delta classification.
- Compatibility disposition.
- Migration guidance and deprecation schedule.

## Deterministic Workflow

1. Diff current and target contracts.
2. Classify each change: additive, behavioral, or breaking.
3. Map consumer impact and required migration.
4. Define versioning and deprecation actions.
5. Publish compatibility verdict with evidence.

## Delta Classification Template

| Contract Surface | Change Type | Compatibility Impact | Action |
|---|---|---|---|
| Tool input schema | Additive or Breaking | Low or High | <action> |
| Resource URI behavior | Behavioral | Medium | <action> |
| Prompt argument contract | Additive or Breaking | Low or High | <action> |

## Done Criteria

- Every delta is classified.
- Compatibility verdict is explicit.
- Migration and deprecation actions are complete.
