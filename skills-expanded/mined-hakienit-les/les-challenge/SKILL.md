---
name: les-challenge
description: Try to prove a claim, fix, review finding, or finished change wrong, and report only what survives.
invocation: model
maturity: experimental
route: challenge
profile: core
bootstrap: skills/les-bootstrap/SKILL.md
loads: ["../les-bootstrap/SKILL.md","../../policies/workflows/review.md","../../policies/verification.md","../../policies/rules/definition-of-done.md"]
---

# Challenge

## Invoke

Inherit `../les-bootstrap/SKILL.md` and the review workflow. Use after a writer
or reviewer has produced a claim: a fix, a finding, or a `COMPLETE` status.

## Inputs

One claim to test, its acceptance source, and the change or evidence it rests on.

## Procedure

1. Restate the claim as a falsifiable statement with its acceptance source. Done when: one observable condition would make the claim false.
2. Search for that condition: unhandled inputs, sibling callers, broken invariants, stale or missing checks, and evidence that does not cover the claim. Done when: each attack names the path, input, or check it used.
3. Reproduce every candidate failure from code or a runnable check. Done when: each candidate is confirmed with evidence or dropped.
4. Return the verdict. Done when: the claim is `refuted` with the surviving counter-evidence, or `holds` with the attacks that failed.

## Output

A verdict (`holds` or `refuted`), surviving counter-evidence with locations, and
the attacks tried.

## Guardrails

Read-only: never edit, commit, or fix the challenged work. Report a doubt you
could not confirm as an unverified risk, not as a refutation. Do not challenge
your own output.

## Verification

Every refutation cites a location and a reproduction or a missing check. A
`holds` verdict lists the attacks tried and the coverage not attempted.
