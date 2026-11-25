---
name: implement
description: Implement a piece of work from a spec or set of tickets using TDD, regular typechecking, a final full test run, code review, and a commit. Use when the user supplies a spec/tickets to implement. Not for writing the spec itself or for large multi-ticket graphs (use implement-spec).
disable-model-invocation: true
---
Implement the work described by the user in the spec or tickets.

Use /tdd where possible, at pre-agreed seams.

Run typechecking regularly, single test files regularly, and the full test suite once at the end.

Once done, use /code-review to review the work.

Commit your work to the current branch.

## Purpose
Turn a spec or tickets into committed, reviewed, tested code on the current branch.

## When to use
A spec or small set of tickets exists and the user asks to implement it.

## When NOT to use
- No spec exists -> create one first (to-spec).
- A large spec with a ticket dependency graph -> implement-spec.

## Inputs
The spec or ticket references, the repository, and the project's test and typecheck commands.

## Core workflow
1. Read the spec/tickets and agree the test seams.
2. Implement with /tdd at the agreed seams.
3. Typecheck often; run single test files often.
4. Run the full suite once at the end.
5. Review with /code-review and fix findings.
6. Commit to the current branch.

## Edge cases and failure handling
- Typecheck or tests fail at the end -> fix before reviewing; do not commit red.
- Spec is ambiguous -> ask or record the assumption in the commit/PR.

## Validation
- Full test suite and typecheck pass; review findings resolved; diff matches the spec.

## Output requirements
Committed implementation with a short summary: what was built, tests run, assumptions.

## Example
```text
Spec: "Add CSV export" -> tests for export format -> implement -> typecheck -> full suite -> review -> commit "feat: CSV export".
```

## Related skills
tdd, code-review, implement-spec, to-spec
