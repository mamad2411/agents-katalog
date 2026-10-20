---
name: qa-triage
version: 1.0.0
description: Decision framework for classifying a test failure as a real bug, a bad test, or a flake, plus clustering related failures and recognizing when one root cause is inflating the count. Load whenever a test run comes back with failures to interpret, before filing anything.
---

# QA Triage

A red test is a signal, not a verdict. Before acting on a failure, classify it.

Every classification here feeds Sentinel's (`qa-engineer`) §10 defect-triage step: a confirmed bug becomes a **drafted** defect (repro steps, expected vs. actual, severity, linked requirement/oracle tier) presented for review — never auto-filed into a tracker.

## Bug vs. bad test vs. flake

Ask in this order:

1. **Reproduce it.** Run the failing test in isolation, then run it again immediately. If it passes on repeat with no code change, it's a flake candidate — go to the flake branch below, don't file it as a bug yet.
2. **Check the assertion against the requirement, using the Oracle Hierarchy** (regulatory/legal → spec/contract → acceptance criteria → documented behavior → design artifact → historical implementation → stated expectation → your own inference) — not against what the code currently does. If the test asserts something no tier of the hierarchy actually specifies, or asserts an implementation detail rather than a behavior, it's a bad test — fix the test, and say so explicitly (never silently loosen it — see `engineering-integrity`).
3. **If it reproduces reliably and the assertion is checking a real requirement**, it's a bug. Move to root-causing it (reproduce → isolate → hypothesize → gather evidence → identify root cause), not just to reporting the symptom.

## Flake diagnosis (don't just retry and move on)

A flaky test is worse than no test — it trains people to ignore red. Common causes, roughly in order of likelihood:

- **Timing/race**: assertion runs before an async operation finishes. Fix: wait on the actual condition (network idle, element state, DB write ack), never a fixed `sleep`.
- **Shared state**: tests pass in isolation but fail in a suite because of order dependency or leaked state (DB rows, global singletons, shared ports). Fix: isolate fixtures per test.
- **Environment/external dependency**: network flakiness, third-party service, clock skew. Fix: mock the boundary, or explicitly mark as an integration test with its own retry policy — don't let it erode confidence in the unit suite.
- **Non-determinism in the code itself**: unseeded randomness, unordered collection iteration relied on for output order. This is a real bug in the code, not just the test.

Never mark a flaky test as skipped/quarantined without a tracked follow-up — quarantine without a ticket is how flakes become permanent blind spots.

## Clustering failures

When a run returns many failures, don't triage each independently before checking for a shared cause:

- Group by error message/stack trace signature first — 40 failures with the same root exception are one bug, not 40.
- Group by recently changed file/module — correlate failures against the diff, not just against the test names.
- Check for a single upstream dependency change (schema migration, API contract change, config default) that would explain a cluster across unrelated-looking tests.

Report the cluster as one root cause with N symptoms, not N separate findings — this is what separates a useful triage report from a noisy one.

## Multiplication awareness

One bug often shows up as many failures — e.g. a broken shared fixture fails every test that uses it, or a broken date-formatting util fails every feature touching dates. Before escalating "47 tests are failing" as 47 problems:

1. Find the smallest reproducing case.
2. Verify the same root cause explains the rest (don't assume — spot check a sample across the cluster).
3. Report severity by root cause impact (what breaks in production if this ships), not by failure count — a single root cause with 47 symptoms and a single root cause with 1 symptom can have very different real-world severity in either direction.

## Output

A triage result should state, per cluster: classification (bug/bad test/flake), reproduction evidence, root cause (or "not yet isolated" if genuinely still open — don't guess a cause you haven't verified), and suggested owner (engineering fix vs. test fix). Hand bugs to `software-engineer` with enough reproduction detail that they don't have to re-derive it from scratch.
