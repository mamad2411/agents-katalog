---
name: typing-upgrade-guardrails
description: Introduce typing improvements incrementally without destabilizing delivery. Use when raising type coverage or strictness.
---

# Typing Upgrade Guardrails

## Goal
Improve typing quality with controlled rollout and clear constraints.

## Workflow
1. Read `../_shared/PROTOCOL.md` and align with task objective.
2. Read `../_shared/skill-usage-policy.md` and apply activation/escalation rules.
3. Collect repository evidence from source-of-truth files before proposing edits.
4. Produce required artifact for this skill.
5. Add explicit verify step and fail condition.
6. Stop and escalate if verify fails after two hypothesis changes.
7. Finish with summary from `../_shared/artifact-summary-template.md`.

## Required Output
Typing migration plan using `../_shared/python-typing-ladder.md`, including where to use Protocol, TypedDict, and dataclass(slots=True).

## Verify Gate
Type checker passes at chosen strictness level for targeted modules.

## Safety Rules
- Fail closed for risky work: architecture, refactor, release, config, or dependency changes.
- Do not exceed change budget without explicit escalation note.
- Do not repeat failing command without changing approach.
