---
name: test-strategy-generator
description: Generate layered test strategy (unit/integration/e2e), golden tests for generators/parsers, and clear mocking boundaries. Use before major implementation or refactor.
---

# Test Strategy Generator

## Goal
Make testing intentional instead of ad-hoc.

## Workflow
1. Read `../_shared/PROTOCOL.md` and align with task objective.
2. Read `../_shared/skill-usage-policy.md` and apply activation/escalation rules.
3. Collect repository evidence from source-of-truth files before proposing edits.
4. Produce required artifact for this skill.
5. Add explicit verify step and fail condition.
6. Stop and escalate if verify fails after two hypothesis changes.
7. Finish with summary from `../_shared/artifact-summary-template.md`.

## Required Output
Test matrix by component and risk level.

## Verify Gate
Each critical path must map to at least one deterministic test type.

## Safety Rules
- Fail closed for risky work: architecture, refactor, release, config, or dependency changes.
- Do not exceed change budget without explicit escalation note.
- Do not repeat failing command without changing approach.
