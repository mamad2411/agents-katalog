---
name: les-discovery
description: Clarify an ambiguous engineering request before design or implementation when outcome, constraints, or acceptance are unsettled.
invocation: model
maturity: stable
route: discovery
profile: core
bootstrap: skills/les-bootstrap/SKILL.md
loads: ["../les-bootstrap/SKILL.md","../../policies/workflows/task-lifecycle.md","../../policies/rules/context-loading.md","../../policies/rules/technical-decisions.md","../../policies/rules/change-scope.md"]
---

# Discovery

## Invoke

Inherit `../les-bootstrap/SKILL.md` and load declared policy dependencies.

## Inputs

Ambiguous request, known constraints, and relevant project context.

## Procedure

1. Restate the requested outcome, user, scope, non-goals, and success signal. Done when: ambiguity is explicit rather than hidden in implementation language.
2. Inspect the smallest relevant context and affected flow. Done when: options are evidence-backed and project conventions are known.
3. Separate reversible defaults from choices only the human can make. Done when: authority, risk, and cost impact are named.
4. Produce a bounded interpretation or ask for a decision. Done when: next action is safe and acceptance has one meaning.

## Output

Decision record with assumptions, alternatives, and terminal status.

## Guardrails

Do not implement, select a project-owned technology, or infer missing authority.

## Verification

Record the evidence behind each resolved assumption, near-miss interpretation, and
any `PENDING_USER_ACTION`. Do not create implementation files while material
ambiguity remains.

Bootstrap LES. Inspect the existing system, separate known constraints from open
choices, and resolve only questions that change the solution. Output a bounded
problem statement, acceptance conditions, exclusions, and remaining decisions.
Stop before implementation until material ambiguity is resolved; verify every
stated constraint against the request or repository.
