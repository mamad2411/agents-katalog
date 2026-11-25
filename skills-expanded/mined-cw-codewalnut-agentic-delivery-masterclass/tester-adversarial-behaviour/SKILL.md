---
name: tester-adversarial-behaviour
description: Use when executing acceptance checks across behaviour, side effects, repeats, failures, and recovery.
---

# Challenge behaviour and side effects

## Inputs
Evidence plan, restored exact target, stable fixtures, public seams, state-inspection path, and side-effect contract.

## Procedure
1. Exercise applicable success, invalid, permission, lifecycle refusal, conflict, error, partial-failure, and recovery states through public seams.
2. Assert returned output, persisted state/version, every required side effect, and every forbidden mutation; explicitly classify omissions.
3. Exercise exact replay, changed-key repetition, stale versions, navigation/retry boundaries, and uncertain outcomes where relevant.
4. Preserve case-level commands, exits, fixtures, assertions, target identity, and evidence locators.
5. If observed state conflicts with approved policy, stop and return the expectation to its owner rather than editing fixtures.

## Output
Revision-bound case receipts with explicit behavioural and side-effect coverage and omissions.

## Stop condition
Stop when fixture state or side-effect storage is unknown, evidence targets other bytes, the environment cannot observe the claim, or expected behaviour is unresolved.
