---
name: plan-first-mini-adr
description: Create a short design record before implementation for architecture-touching changes or edits over 5 files. Use to capture why, options, risk, and rollback.
---

# Plan First / Mini ADR

## Goal
Lock rationale before coding.

## Workflow
1. Read `../_shared/PROTOCOL.md` and align with task objective.
2. Read `../_shared/skill-usage-policy.md` and apply activation/escalation rules.
3. Collect repository evidence from source-of-truth files before proposing edits.
4. Produce required artifact for this skill.
5. Add explicit verify step and fail condition.
6. Stop and escalate if verify fails after two hypothesis changes.
7. Finish with summary from `../_shared/artifact-summary-template.md`.

## Required Output
Mini ADR using `../_shared/mini-adr-template.md` with two options and explicit decision.

## Verify Gate
Ensure every ADR includes Problem, Constraints, Options, Decision, Risks, and Rollback.

## Safety Rules
- Fail closed for risky work: architecture, refactor, release, config, or dependency changes.
- Do not exceed change budget without explicit escalation note.
- Do not repeat failing command without changing approach.
