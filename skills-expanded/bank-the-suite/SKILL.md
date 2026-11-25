---
name: bank-the-suite
description: "Use after each unit of work in a repo with a real test suite — before the next task, a compaction, or declaring done. Runs the full suite (backgrounded and parallelized when slow) and banks a verified green: honest counts against a baseline, every failure accounted for by name. Use when only nearby tests were run or failures are called 'probably unrelated'."
---

# Bank the Suite

## The failure mode this fixes

The agent changes a module, runs the three tests next to it, sees green, and moves on. Four tasks later the full suite runs for the first time and 23 tests are red — and now nobody knows *which* of the four changes broke them, the context that would have made the diagnosis cheap is gone, and the "quick fix" becomes an archaeology dig.

The inverse failure is just as common: the suite *is* run, 14 tests fail, and the report says "some pre-existing failures, probably unrelated." Probably. Unverified red is a debt that compounds — every subsequent change hides behind it.

This skill makes the full suite a **bank**: after each unit of work you deposit a verified green state, so the next unit starts from known-good and any new red has exactly one suspect.

## When to Use This Skill

- A feature, fix, or refactor just landed and the next task is queued
- Only the tests adjacent to the change were run
- You're about to compact context, hand off, or end the session — the next session needs a trusted baseline
- The suite is slow and keeps getting skipped because "it takes 20 minutes"
- A report says failures are "pre-existing" or "unrelated" without naming them

**Don't use when:** the repo has no meaningful suite (then the gap *is* the finding — say so), or mid-exploration when nothing has landed yet. Don't block a one-character doc fix on a 20-minute suite — scale the gate to the blast radius.

## Instructions

### 1. Establish the baseline once

Before the first change of the session, know what the suite looks like clean: total collected, passing, and any already-failing tests *by name*. If you skipped this and the suite is now red, check the failing tests against the main branch / pre-change state before assuming your change caused it — but check, don't assume.

### 2. Run the whole thing, not the neighborhood

Tests near the change verify the change; the rest of the suite verifies the *blast radius* — the callers, the shared fixtures, the serialization someone else depends on. The failures that hurt are always in code you didn't think you touched. If a full run is genuinely too slow for every iteration, run the affected subset per iteration and the full suite at the unit boundary — but the unit doesn't close until the full run is green.

### 3. Run it in the background, keep working

A slow suite is not a reason to skip it — it's a reason to parallelize it (`pytest -n auto`, sharded CI, whatever the stack offers) and to kick it off in the background while you write the report or prep the next task. The rule isn't "wait 20 minutes"; it's "don't *start stacking* the next change on an unverified base."

### 4. Account for every red, by name

A finishing run has three acceptable descriptions for a failing test, and "probably unrelated" is not one of them:

1. **Caused by this change** → fix it now, or revert.
2. **Pre-existing** → named, and verified failing before the change (re-run it on the base state if you didn't capture the baseline).
3. **Newly flaky** → demonstrated by re-run, and reported as its own finding — flakiness is a defect, not noise.

### 5. Bank it and say so

Close the unit with an explicit deposit: counts, deltas from baseline, named carve-outs. That line is what lets the next task — or the next session, or another agent — start without re-verifying the world.

## Output format

```
Suite banked: <suite/command>
Result: <passed>/<collected> passed in <time> (baseline: <passed>/<collected>)
New failures: <none | list — each fixed or reverted before closing>
Pre-existing failures (verified, not introduced here): <named list | none>
Flaky: <named list with re-run evidence | none>
Safe to build on: yes / no because <reason>
```

## Anti-Patterns

| Anti-Pattern | Why it defeats the skill |
|---|---|
| Neighborhood green | running only the tests you just wrote and reporting "tests pass." |
| "Probably unrelated" | unverified attribution of red to someone else. Verify or own it. |
| Stacking on red | starting task N+1 while task N's suite status is unknown. One suspect becomes four. |
| Skipping because slow | the suite's runtime is an engineering problem (parallelize, shard, background it), never a waiver. |
| Counts-only reporting | "all green" with no baseline comparison hides the test that silently stopped being collected. |

## Mental Model

> The suite is a bank account: each unit of work ends with a deposit of verified green, and every deposit has a receipt. You can move fast precisely because you never have to wonder whether the last balance was real.
