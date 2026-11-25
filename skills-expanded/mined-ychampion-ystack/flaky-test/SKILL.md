---
name: flaky-test
description: >-
  Hunt down a test that passes sometimes and fails sometimes: measure its failure rate by rerunning,
  then isolate the cause (test order, shared state, time, randomness, concurrency, network, the
  machine) one factor at a time, fix the cause and prove the rate is zero. Use for "flaky test",
  "intermittent failure", "fails in CI but passes locally", "passes on retry", or before adding a retry
  or skip to a test.
---

# Flaky test

A retry hides a flaky test; it doesn't fix it, and sometimes the flake is a real bug users hit. Turn
"sometimes" into a number, then move that number to zero.

## When it applies

- A test fails without any related code change, then passes on rerun.
- It fails in CI and never locally, or the other way round.
- Someone proposes a retry, a longer timeout or a skip.

## Procedure

### 1. Measure the rate

Run the single test in a loop, at least 50 times, and count failures. If the runner can't pick one
test, loop the whole suite. Save each failure's output in a scratch folder, not the repo.

```bash
for i in $(seq 1 50); do <test command> > "$TMP/run-$i.log" 2>&1 || echo "fail $i"; done
```

Zero failures alone? Run it inside its whole file, then the whole suite, then with CI's parallelism.
Now you know which context makes it flake. Compare the failure messages: one message or several?
Note which test fails; the cause is often a different test that ran before it.

### 2. Isolate one factor at a time

Check each, changing only that factor, and rerun the loop:

| Factor | How to test it |
| --- | --- |
| Test order / shared state | Run with a random or reversed order, or the test alone vs after its neighbour. Leftover globals, singletons, DB rows, temp files, env vars, mocks not restored. |
| Time | Freeze or shift the clock; run near midnight, month end, DST, another timezone. |
| Randomness | Seed the generator; try several seeds and find one that fails every time. |
| Concurrency / async | Missing `await`, sleeps used as waits, a race between two tasks. Add load (`-j` high, CPU stress) and the rate should rise. |
| Network / external | Cut the network or stub the service; real calls, DNS, ports already in use. |
| Machine | Slower machine, other OS, path separators, file ordering from the disk, locale. |

To pin order when the runner has no option for it, wrap the runner and replace its shuffle with a
fixed order; for a small suite, try every order. Stop as soon as one factor turns the flake on and off
reliably; you don't need to test the rest. A seed or order that fails every time is the best
reproduction you can get; keep it.

### 3. Fix the cause

- Shared state: reset it in setup or teardown, or give each test its own copy.
- Time: inject a clock.
- Randomness: seed it in the test.
- Async: wait for the actual condition or event, never a fixed sleep.
- Network: stub it at the boundary.
- If the test is right and the code races, the bug is in the code. Fix the code.

### 4. Prove it

Rerun the step 1 loop in the context that flaked, with the failing seed or order if you found one.
Report 0 of N, with N at least 50 and at least 3 times the step 1 loop size you needed to see a
failure. Also run the failing seed or order directly: it must pass every time.

## Report

```
Test: <name that failed>   Polluter: <test or event that set it up, if any>
Before: <k>/<n> failed (<context>)   After: 0/<n>
Cause: <factor, file:line>   Fix: <what changed>
```

## Rules

- No retry, skip or longer timeout as the fix unless the user agrees, and then label it as a mask.
- Change one factor per run of the loop.
- Keep the failing seed or order as a deterministic test that sets up the bad state itself, so it
  doesn't depend on runner order.
