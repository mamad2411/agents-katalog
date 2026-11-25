---
name: data-contracts-dto-mapping-policy
description: Separate domain models from transport/persistence DTOs and centralize mappings with versioned contracts. Use for API/schema evolution and boundary cleanup.
---

# Data Contracts and DTO Mapping Policy

## Goal
Avoid model leakage across layers.

## Workflow
1. Read `../_shared/PROTOCOL.md` and align with task objective.
2. Read `../_shared/skill-usage-policy.md` and apply activation/escalation rules.
3. Collect repository evidence from source-of-truth files before proposing edits.
4. Produce required artifact for this skill.
5. Add explicit verify step and fail condition.
6. Stop and escalate if verify fails after two hypothesis changes.
7. Finish with summary from `../_shared/artifact-summary-template.md`.

## Required Output
Contract version policy (v1/v2), mapper placement, and naming conventions.

## Verify Gate
Check each boundary crossing has explicit mapper path and tests.

## Safety Rules
- Fail closed for risky work: architecture, refactor, release, config, or dependency changes.
- Do not exceed change budget without explicit escalation note.
- Do not repeat failing command without changing approach.
