---
name: builder-verification-and-deviation
description: Use when an increment needs exact verification, deviation disposition, and Tester intake.
---

# Verify the exact change and route deviations

## Inputs
Exact base/result identity, complete diff, focused evidence, baseline, agreed broader checks, evidence location, and deviation list.

## Procedure
1. Run fresh focused and broader checks on the exact result; record commands, exits, environment, and evidence locators.
2. Reconcile the complete changed-file inventory with authority and remove unrelated generated churn.
3. Classify deviations by policy, Design, contract/invariant, migration/configuration, or authority; record locator, consequence, owner, and re-entry point.
4. Stop on every material deviation until the named owner supplies a revision-bound decision; rerun from the revised plan and authority.
5. Record baseline failures, confidence limits, and unexecuted checks without turning green into approval.

## Output
A `built_for_test|blocked` receipt with exact target/diff, changed behaviour, RED/GREEN evidence, deviations, and limits.

## Stop condition
Do not emit success for stale or different bytes, incomplete inventory, unrecoverable evidence, missing commands, unexplained failures, or an unaccepted material deviation.
