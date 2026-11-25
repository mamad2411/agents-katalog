---
name: debugging-and-root-cause
description: Finds the real cause of a defect systematically, including intermittent and production-only failures. Triggers - it worked yesterday and now it doesn't, can't reproduce, crashed with this stack trace, why is this failing, works on my machine, debug this, unexpected result.
---

# Debugging and Root Cause

Debugging by guessing is a random walk with an unbounded cost. Debugging by
method has a predictable shape: preserve evidence, reproduce, narrow, explain,
fix, generalize. The method matters most exactly when pressure says to skip it.

## Sequence

### 1. Stop and preserve

Stop adding features. Capture the evidence **now**, before it disappears:
the exact input, the full error with stack trace, the version/commit, the
environment, the timestamp, correlation ids, relevant log window. Production
state is transient; a screenshot of a dashboard at the moment of failure is
often unrecoverable an hour later.

Save the triggering input as a test fixture immediately.

### 2. Reproduce

A bug you cannot reproduce is a bug you cannot verify fixed. Work down until
you have a single command:

failing in production → failing in staging → failing test with real data →
minimal failing test.

If it will not reproduce, the difference between environments *is* the bug's
neighborhood: configuration, data shape, version, concurrency, locale,
timezone, resource limits.

### 3. Narrow

Bisect the space, do not tour it.

| Axis | Technique |
|---|---|
| Time | `git bisect run` with a test command — minutes, not hours |
| Input | Halve the input until the failure disappears |
| Code path | Assert or log at the midpoint: is the value already wrong here? |
| Layer | Is it wrong entering the function, or produced wrong inside it? |
| Environment | Change one variable at a time between working and failing |

State a falsifiable hypothesis before each experiment ("the timestamp is
already naive when it reaches this function"), then run the experiment that
would disprove it. Changing code to see what happens is not an experiment.

### 4. Explain

You have the root cause when you can state the causal chain and explain **every
observed symptom**, including the odd ones. "Changing this line made it stop"
is correlation; you may have moved the timing rather than fixed the fault.

Unexplained symptom = incomplete diagnosis. Keep going.

### 5. Fix with a test

Reproduction test first, failing for the right reason, then the fix
(`test-driven-development`).

### 6. Generalize

Find the siblings. The same mistake usually exists in adjacent code written by
the same hand on the same day. Grep for the pattern, not just the line. Then
ask the cheap systemic question: what would have caught this earlier — a type,
a constraint, a linter rule, a test at a different level?

## Failure-mode lookup

| Symptom | Look first at |
|---|---|
| Worked yesterday | Dependency update, config change, data growth, expired certificate/token, clock |
| Works locally, fails in CI/prod | Environment variables, timezone/locale, filesystem case sensitivity, parallelism, resource limits, network policy |
| Intermittent | Race on shared state, test order, real clock, unawaited async work, retry masking |
| Slow then failing | Resource exhaustion: pool, memory, file handles, disk |
| Wrong value, no error | Type coercion, floating point, timezone, encoding, silent truncation, wrong default |
| Fails only at scale | N+1, missing index, unbounded collection, lock contention |
| Fails for one user/tenant | Data-dependent path: nulls, unicode, very long values, legacy rows |
| Error swallowed | `catch {}` upstream; add the log, do not add another try |

## Production debugging

- Prefer read-only investigation: logs, metrics, traces, a replica. Do not
  experiment on live data.
- Correlate by id across services — this is why `observability-and-slos`
  requires correlation ids.
- **Mitigate first, diagnose second** when users are affected: roll back, flip
  the flag off, shed load. Mitigation buys diagnosis time; it is not the fix,
  and the issue stays open (`incident-response`).

## Under time pressure

The temptation is to try things. That is the slowest path with the worst
outcomes: fixes that mask, silenced errors, corrupted data. The non-negotiable
minimum is: capture evidence, reproduce, one hypothesis at a time. Never
"fix" by widening a `catch`, deleting the failing test, or adding a retry
around a deterministic failure.

## Exit checklist

- [ ] Evidence captured and saved as a fixture
- [ ] Single-command reproduction exists
- [ ] Causal chain written down; every symptom explained
- [ ] Reproduction test written and observed failing before the fix
- [ ] Siblings of the same mistake searched for
- [ ] If data was corrupted: scope identified and repair planned
- [ ] Prevention noted — what would have caught this earlier
