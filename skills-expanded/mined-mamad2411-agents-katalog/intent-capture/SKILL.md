---
name: intent-capture
description: Record a rare accepted durable non-testable decision, move a governing route, or create, renew, or remove an accepted temporary exception. Do not use for task summaries, progress, evidence logs, or read receipts.
---

# intent-capture

Capture semantic state transitions, not completed work. Most invocations should report
`captured 0`.

## Invocation

```text
/intent-capture [unit]
/intent-capture [unit] --proposal
/intent-capture [unit] --exception
/intent-capture [unit] --route
```

## Decision admission

Write only when all answers are yes:

1. Would missing it materially change a future agent's behavior?
2. Can no executable contract or test enforce it adequately?
3. Could a capable future agent plausibly re-derive it incorrectly?
4. Must it survive beyond the current branch?
5. Is carrying it cheaper than rediscovering it?
6. Is its authority backed by an inspectable source?

One unit normally creates zero decisions and never more than three. Implementation progress,
temporary assumptions, rejected alternatives, explanations, commands, results, and ADR summaries
fail the test.

## Write target

- Ordinary accepted decision: `.intent/decisions/<scope-root>/<id>.yml`, one entry per file.
- Genuinely concurrent candidate: `.intent/proposals/<unit>/<id>.yml`.
- Accepted temporary underdelivery: `.intent/exceptions/<unit>.yml`.
- Moved governing entry point: edit the matching row in `.intent/ROUTES.yml`.

Do not create a proposal merely because work is on a feature branch. Use one only when parallel
units can decide the same property, equal-domain directions conflict, supersession crosses
concurrently landing branches, or integration must compose candidates.

## Decision rules

Use `kind: product_direction`, `architectural_constraint`, or `implementation_choice`. Authority
describes the source domain; it is not a universal precedence rank. Product direction and
architectural feasibility must be composed. Implementation-authority choices remain proposals.

Resolve provenance before wording. Keep the decision to one sentence and 140 characters. Use
full `HEAD` for `introduced`, derive `id` as `<short-introduced>-<n>`, and name the file after the
id. Add `observed_ids` only as evidence that a superseded or conflicting decision was actually
read; add `supersedes` only for replacement.

## Exception rules

An exception requires an inspectable requirement, short substitute, accepted source, and
inspectable exit; add an expiry when time-bounded. Never use an exception to hide an unaccepted
mock or broken contract. There are no unit notes or `brief_ids`.

## Finish

Run `sh ci/check-intent.sh`, leave changes unstaged unless the invoking task explicitly owns
staging, and report exactly what semantic transition was recorded. Never switch an unrelated
worktree to write intent and never treat repository execution mode as permission to push or
mutate an external system.
