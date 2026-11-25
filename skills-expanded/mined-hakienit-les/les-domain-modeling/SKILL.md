---
name: les-domain-modeling
description: Establish or sharpen shared project language, domain boundaries, invariants, and decision records before complex engineering work.
invocation: model
maturity: stable
route: domain-modeling
profile: core
bootstrap: skills/les-bootstrap/SKILL.md
loads: ["../les-bootstrap/SKILL.md","../../policies/workflows/task-lifecycle.md","../../policies/rules/technical-decisions.md","../../policies/rules/documentation.md","../../policies/memory-model.md"]
---

# Domain Modeling

## Invoke

Bootstrap LES when terms, boundaries, or invariants are unclear enough to cause
misaligned implementation or repeated explanation.

## Inputs

Observed vocabulary, affected flows, domain examples, current project context,
and the decision or behavior that needs shared language.

## Procedure

1. Collect terms from users, code, data, and existing decisions. Done when: synonyms, overloaded terms, and missing definitions are visible.
2. Test the model against normal, edge, and failure scenarios. Done when: each important term has an invariant or boundary.
3. Record the smallest durable vocabulary and ownership. Done when: the record has a project location and expiry/update trigger.
4. Apply the model to the requested decision. Done when: the next implementation or clarification uses the same terms.

## Output

Domain record with terms, definitions, boundaries, invariants, examples, open
questions, owner, and promotion decision.

## Guardrails

Do not invent business rules from naming alone. Do not promote temporary shorthand
or unverified inference into project-wide context.

## Verification

Confirm the model explains the affected flow and does not contradict existing
project decisions. Mark unresolved terms `PENDING_USER_ACTION`.
