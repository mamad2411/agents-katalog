---
name: les-technical-research
description: Research technical facts, APIs, standards, or project constraints when implementation depends on evidence outside the current code path.
invocation: model
maturity: stable
route: research
profile: core
bootstrap: skills/les-bootstrap/SKILL.md
loads: ["../les-bootstrap/SKILL.md","../../policies/workflows/task-lifecycle.md","../../policies/rules/context-loading.md","../../policies/rules/technical-decisions.md","../../policies/rules/documentation.md"]
---

# Technical Research

## Invoke

Bootstrap LES and use this skill when a decision requires external or repository
evidence that cannot be safely inferred from the affected code.

## Inputs

Research question, decision boundary, trusted source constraints, time/cost limit,
and the acceptance condition the research must unblock.

## Procedure

1. Bound the question and source authority. Done when: the decision, exclusions, and evidence bar are explicit.
2. Gather the smallest sufficient primary evidence. Done when: claims have source, date/version, and supporting excerpt or observation.
3. Compare options against project constraints. Done when: facts, inferences, and recommendations are separated.
4. Return the decision record and next action. Done when: implementation can proceed, a choice is pending, or the task is blocked truthfully.

## Output

Research record with question, sources, verified facts, uncertainty, options,
recommendation, expiry, and next safe action.

## Guardrails

Do not treat search snippets or memory as proof. Do not introduce a dependency,
standard, or provider assumption without recording the decision boundary.

## Verification

Check every cited fact against its source and record unavailable or conflicting
evidence. Research itself does not authorize implementation or external mutation.
