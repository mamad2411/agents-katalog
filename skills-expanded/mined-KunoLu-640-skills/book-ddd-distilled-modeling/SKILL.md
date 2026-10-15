---
name: book-ddd-distilled-modeling
description: Guides lightweight domain modeling with ubiquitous language, bounded contexts, and subdomain focus. Always run after every completed grill-with-docs session as an independent second-pass boundary review; also use before PRD, design, or implementation when domain ambiguity exists.
---

# Book DDD Distilled Modeling

Use this Skill to sharpen domain language before turning a business request into PRD, issues, design, or code.

It is derived from the `mini` rule style of `agent-rules-books` and should run after project evidence is read. It complements `grill-with-docs`, `to-spec`, and task planning.

## Mandatory Post-grill Review

Every fully completed `grill-with-docs` session MUST be followed immediately by this Skill, whether the Agent initiated that session or the user invoked it explicitly. The `domain-modeling` activity embedded in `grill-with-docs` is the active interview-time modeling pass; it does not satisfy or replace this independent second-pass review.

Re-read the completed clarification result and the supporting project facts. Look for boundary errors, hidden term collisions, unsupported invariants, misplaced responsibilities, and unresolved context ownership rather than merely restating the interview.

The review is a gate before requirement confirmation, PRD, design, task creation, or implementation:

- `confirmed`: no unresolved boundary issue prevents the workflow from advancing.
- `needs-clarification`: output the findings, return to one-question-at-a-time clarification, and rerun this Skill after resolution.
- `blocked`: the Skill, required evidence, or relevant context is unavailable; output the exact blocker and do not advance.

Invocation origin, a prior `domain-modeling` pass, or an Agent judgment that the requirement is already clear MUST NOT skip this gate.

## When To Use

- Every completed `grill-with-docs` session, without exception.
- A requirement uses business terms that may mean different things in different parts of the system.
- A change touches domain rules, permissions, lifecycle, workflow state, billing, identity, tenancy, inventory, orders, subscriptions, or similar concepts.
- It is unclear whether two concepts belong in the same model or bounded context.
- A PRD or design needs stable terminology before implementation.

When `grill-with-docs` was not used, do not use this Skill for purely technical refactors, simple UI copy, mechanical dependency updates, or features with no domain ambiguity.

## Workflow

1. Read existing project facts first: README, domain docs, `docs/spec`, ADRs, task artifacts, and relevant code.
2. List the key terms and their current meanings in the project.
3. Identify bounded contexts where the same word may have different meanings.
4. Distinguish core, supporting, and generic subdomains when that affects priority or design.
5. State invariants and business rules in the language used by the project.
6. Feed the agreed language into `prd.md`, `design.md`, or `implement.md`.

## Output

Always output the review visibly and separately from the requirement confirmation summary:

```text
DDD Boundary Review
Status: confirmed | needs-clarification | blocked
Ubiquitous language: ...
Bounded contexts: ...
Invariants and business rules: ...
Core / supporting / generic subdomains: ...
Corrections to the grill-with-docs result: ...
Open conflicts and questions: ...
```

Use `not-applicable` for a subdomain classification only when it has no bearing on the current decision; do not omit the field. A post-grill review must explicitly state whether it corrected the earlier result, even when the answer is `none`.

Only stable, cross-task domain decisions should be promoted to `docs/CONTEXT.md`, ADRs, or `docs/spec`. Keep the complete review in task-level output or the current `prd.md`, `design.md`, or `implement.md`.

## Guardrails

Outside the mandatory post-grill gate, do not force DDD ceremony into small tasks. During the mandatory gate, keep the second pass concise but complete enough to prove the boundaries were independently checked.
