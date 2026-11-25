---
name: check-flaky-tests
description: Detect flaky tests — re-run analysis, CI history, quarantine — then route to fixes
argument-hint: "[scope]"
related:
  - improve
  - run-test
  - follow-test
  - deep-test
  - deep-review-codebase
  - report
  - suggest-next-action
  - ask-me
---

## Goal

Answer the question "which tests are flaky, and how do we handle them" — scan re-run/CI history for non-deterministic tests, quarantine them with evidence, then route findings to fixes via `/improve tests` / `/optimize test-suite`

## Scope

Use when you suspect flakiness in a test suite — a direct check workflow (not a thin review entry); governs detection + quarantine policy only, never fixes assertions itself

- Detection: re-run N times and compare results, CI-history failure rate per test, time-of-day/parallelism correlation
- Quarantine policy: mark + issue + owner + expiry — never quarantine permanently
- Common root causes: shared state, timing/race, wall-clock dependence, external services — aligned with `/follow-test`
- Tests that genuinely assert wrong (not flaky) → `/deep-test test-correctness`; slow suite → `/optimize test-suite`

## Execute

### 1. Detect

> Goal: prove which tests are flaky with rerun or CI-history evidence

1. Take `scope` from the argument — if absent, use the current project; if unclear → `/ask-me`
2. Re-run the suspected tests (e.g. 10–20 iterations via `/run-test` or `--repeat`) and record inverted results (pass↔fail)
3. Check CI history via `/check-git-logs` / `gh run list` — failures not tied to a diff = flaky candidates

### 2. Report + Quarantine

> Goal: list flaky tests with evidence and quarantine them so CI stays green

1. Produce a `/report` table: Test, Fail rate, Correlation (parallel/time/deps), Quarantine decision
2. Quarantine only tests proven non-deterministic — add tag/skip with reason + issue + expiry date
3. Never quarantine just to unblock CI without re-run evidence

### 3. Route Fixes

> Goal: send each flaky test to its owner fix skill

1. Flakiness from test design (shared state, sleep) → `/improve tests`
2. Flakiness from infra/parallelism across the whole suite → `/optimize test-suite`
3. Flakiness from a product-code race → `/improve correctness`; close with `/suggest-next-action`

## Rules

- Every flaky verdict requires re-run/CI evidence — never guess from a single failure
- Quarantines always have an owner + expiry
- Do not fix tests in this skill — route on to the skill that owns the fix

## Expected Outcome

- A list of flaky tests with fail rates and evidence
- Manageable quarantines (never leaking into permanent ignores)
- Every finding routed to the correct fix skill
