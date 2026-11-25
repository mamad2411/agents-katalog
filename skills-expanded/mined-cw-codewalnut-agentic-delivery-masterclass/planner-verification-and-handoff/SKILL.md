---
name: planner-verification-and-handoff
description: Use when delivery slices need executable proof, operator signals, and exact-revision Engineering acceptance.
---

# Plan proof and issue the handoff

## Inputs
Impact/invariant record, slices, Design states, risks, existing commands, observability standards, environment limits, and Engineering owner.

## Procedure
1. Map every criterion, Design state, invariant, and material risk to a check or explicit gap.
2. Include applicable success, refusal, retry, duplicate, stale-version, concurrency, side-effect, and recovery assertions plus a semantic negative control.
3. Name environment, fixture, command, expected result/exit, and retained evidence artifact.
4. Define logs, metrics, traces, or reconciliation signals needed to detect operational failure.
5. Separate fixture-supported claims from distributed, performance, security, reliability, and operational dimensions still unassessed.
6. Issue the exact plan for Engineering review, preserving assumptions, questions, changed surfaces, risks, checks, rollback, and unproved limits.
7. Record `ready_for_build|changes_requested|blocked` for the exact revision; Builder authority remains separate.

## Output
A criterion/state/risk proof and observability matrix plus a revision-bound Engineering handoff.

## Stop condition
Stop when a critical invariant has no observable check, test data/side effects are unsafe, evidence boundaries exceed the environment, or acceptance is absent or stale.
