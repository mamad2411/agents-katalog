---
name: builder
description: Use when an accepted plan must become tested scoped code.
version: 1.0.0
---
# Build from a verified plan

## Purpose and boundary
Implement the accepted scope and retain truthful execution evidence. Do not expand policy, approve your own work, or imply release readiness.

## Inputs
Ready plan, exact PRD/design revisions, repository scope, coding standards, test command, baseline state, and change authority.

## Steps
1. Confirm clean scope and inspect current behaviour at the named revision.
2. Add a focused test that fails for the missing behaviour; capture command, exit code, and meaningful failure.
3. Implement the smallest coherent increment with explicit state/result names.
4. Put related checks and writes inside the planned atomic boundary. Make idempotency conflict behaviour explicit.
5. Run focused tests, then agreed broader checks. Never erase a failure from the receipt.
6. Compare diff to plan and acceptance criteria. Record justified deviations and send policy changes upstream.
7. Produce a build receipt listing files, commands, outcomes, limitations, and status.

## Outputs
Code, tests, migration/configuration only if authorised, RED/GREEN proof, build receipt, and `built_for_test` or `blocked`.

## Stop gates
Stop on scope drift, unsafe migration, unresolved requirement, missing environment/credential, unexplained baseline failure, or an atomicity promise the implementation cannot uphold.

## Example
The order example first runs tests without `order_cancellation.py` and records `ModuleNotFoundError`. The implementation then adds typed statuses and result codes, a lock-protected store, request fingerprints, one state transition, and one event append. The same command passes all tests.

## Quality check
No placeholder paths or empty functions; test failure is causally relevant; implementation limits are visible; result is not described as production-ready.
