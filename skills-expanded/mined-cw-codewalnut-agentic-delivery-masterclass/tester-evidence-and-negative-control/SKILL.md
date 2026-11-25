---
name: tester-evidence-and-negative-control
description: Use when planning independent evidence and proving that the chosen checks can detect wrong behaviour.
---

# tester-evidence-and-negative-control

## Inputs
Exact target, approved criteria/risks, Builder receipt, environment topology, fixtures, and baseline.

## Procedure
1. Reject incomplete or mismatched target identity before execution.
2. Map each claim to observable output, persisted state, side effects, forbidden mutations, and environment needs.
3. Run a disposable semantic negative control that changes the behaviour under test and must fail at the intended assertion.
4. Restore and verify target identity before normal execution.

## Output
An evidence plan and negative-control receipt that distinguishes semantic failure from harness failure.

## Stop condition
Stop on target drift, policy-conflicting fixtures, wrong-cause failure, or a check that cannot detect the claimed defect.
