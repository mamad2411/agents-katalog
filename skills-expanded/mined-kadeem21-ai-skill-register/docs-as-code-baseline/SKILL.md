---
name: docs-as-code-baseline
description: Enforce minimum docs set (README, ARCHITECTURE, DECISIONS, CONTRIBUTING) and update behavior when code changes. Use as a continuous documentation guardrail.
---

# Docs as Code Baseline

## Goal
Keep documentation synchronized with implementation.

## Workflow
1. Read `../_shared/PROTOCOL.md` and align with task objective.
2. Read `../_shared/skill-usage-policy.md` and apply activation/escalation rules.
3. Collect repository evidence from source-of-truth files before proposing edits.
4. Produce required artifact for this skill.
5. Add explicit verify step and fail condition.
6. Stop and escalate if verify fails after two hypothesis changes.
7. Finish with summary from `../_shared/artifact-summary-template.md`.

## Required Output
Docs update checklist and required file ownership rules.

## Verify Gate
Any architecture or workflow change includes corresponding docs diff.

## Safety Rules
- Fail closed for risky work: architecture, refactor, release, config, or dependency changes.
- Do not exceed change budget without explicit escalation note.
- Do not repeat failing command without changing approach.
