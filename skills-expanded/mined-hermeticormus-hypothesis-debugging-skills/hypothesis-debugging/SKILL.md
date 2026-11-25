---
name: hypothesis-debugging
description: Hypothesis-driven debugging protocol — reproduce, isolate, hypothesize, test, fix, document. Use when debugging a failure, a failing test, a flaky CI run, or a production error. Write a ranked hypothesis table before any fix; find the root cause, not a workaround. The operational form of the vibe-engineer-skills principle "hypothesis before help."
license: MIT
---

# Hypothesis debugging

A six-phase protocol for debugging. Do not write a fix until you have a ranked hypothesis table and a confirmed root cause.

**Tradeoff**: bias toward finding the cause over shipping a fast patch. For an obvious one-line typo, use judgment.

## 1. Reproduce

Make the failure happen on demand. Capture the exact error and stack trace, the repro steps, and expected versus actual. Consistent or intermittent? Intermittent points at state, timing, or environment.

## 2. Isolate

Narrow the scope. Check recent commits (`git log --oneline -10`) and diffs, then reduce to the smallest input that still fails.

## 3. Hypothesize

Write a ranked hypothesis table BEFORE touching the code.

| # | Hypothesis | Likelihood | How to test |
|---|-----------|------------|-------------|
| 1 | Most likely cause, stated specifically | High | A cheap yes/no test |
| 2 | Second possibility | Medium | A specific test |
| 3 | Less likely cause | Low | A specific test |

Each row names a concrete cause and has a test that can run.

## 4. Test

Work the table top to bottom. Confirm or refute each row. A confirmed hypothesis is the root cause; a refuted one is removed. Do not skip to a fix on a hunch.

## 5. Fix

With the cause confirmed: the smallest change that addresses it, traced for side effects, verified against the Phase 1 reproduction, plus a regression test that fails on the old code.

Root cause, not workaround. Reject try/catch swallowing, defensive masking checks, renamed symptom variables, mocked broken dependencies, and asserting the bug away. A workaround that passes tests hides the bug and propagates it.

## 6. Document

Record the root cause, the fix and why it addresses the cause, and the prevention: the regression test, the bug category, and how to catch this class faster next time.

---

See full content and worked examples at https://github.com/HermeticOrmus/hypothesis-debugging-skills.
