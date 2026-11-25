---
name: reviewer
description: Use when a tested change needs an independent decision.
version: 1.0.0
---
# Review a change against evidence

## Purpose and boundary
Decide whether the exact change is a merge candidate and identify remaining release work. Do not rely on status prose when inspectable evidence exists.

## Inputs
Exact revision/diff, approved PRD and design, plan, build receipt, tests/logs, baseline, known limits, and reviewer identity.

## Steps
1. Confirm revision and input versions; material changes invalidate earlier review.
2. Trace every acceptance criterion to code and an observed test. Mark missing links.
3. Inspect security and consistency invariants: ownership, state authorization, stale writes, request-key scope, race behavior, mutation/event atomicity, and error disclosure.
4. Challenge the tests: could they stay green if behaviour broke? Do they inspect state and side effects? Does concurrency setup actually overlap attempts?
5. Separate merge checks from release checks such as integration, configuration, deployment, rollback, monitoring, and external delivery.
6. Record findings with severity, locator, consequence, and precise fix. Recheck resolved blockers.
7. Issue `changes_requested`, `merge_candidate`, or `blocked`, bound to the revision.

## Outputs
Findings, criterion disposition, unsupported-claim list, merge decision, release gap list, and reviewer/revision receipt.

## Stop gates
Stop for missing exact revision, incomplete evidence, inconsistent fixtures, required independence conflict, or unanswered critical security/data-integrity risk.

## Example
Accept the sample as a merge candidate for an educational in-memory program after nine tests pass. Withhold production confidence because one lock does not coordinate processes, state is not durable, and event publication has no outbox or delivery acknowledgement.

## Quality check
No finding is based on inference alone; no passing command is treated as semantic proof beyond its assertions; status names owner and revision.
