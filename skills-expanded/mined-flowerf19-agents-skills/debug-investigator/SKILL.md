---
name: debug-investigator
description: Investigates why a failure happens, isolates the confirmed root cause, and captures a reusable reproduction artifact. Use when asked to diagnose or debug a bug, failing test, build error, slow behavior, or unexpected result. Do not use to edit production code without separate approval.
license: MIT
---

# Debug investigator

Find the confirmed root cause, save a reusable reproduction artifact, and identify the smallest valid fix.

**Read-only lock:** Keep the repository unchanged for diagnosis-only requests; verify with [check-readonly.sh](../scripts/checks/check-readonly.sh). Use read-only inspection, existing tests, or isolated `/tmp` checks. Never touch production data or expose secrets.

## Step 1: Capture Failure & Reproduction Artifact

1. Record expected vs actual behavior, inputs, error output, and environment.
2. Build the smallest reliable reproduction and save a **Reproduction Artifact** (failing command/script, log, trace, or capture in `/tmp` or the task artifacts dir). State whether it reproduced.
3. Check live code against accepted requirements; never trust mocks or stale docs as proof of the real bug.

## Step 2: Trace the Cause

1. Follow data and calls through real modules from entrypoint to returned result.
2. Locate the first point where behavior diverges from accepted requirements.
3. Compare recent commits or a working sibling flow when useful without copying unrelated business rules.
4. For async or stored state, inspect event ordering, cancellation, locks, retries, and logs; an HTTP 200 or green mock does not prove completion.

## Step 3: Test Hypotheses

1. State a falsifiable hypothesis and what would disprove it.
2. Run the smallest isolated check separating competing causes.
3. Record what was confirmed or ruled out; never make blind edits or label guesses as confirmed.
4. For intermittent failures, collect evidence at the failure point instead of adding sleeps, retries, or larger timeouts. If evidence stalls, stop and report missing access or telemetry.

## Step 4: Return Diagnosis & Handoff

Lead with the confirmed root cause, then report:

- **Reproduction Artifact:** exact path and command for `thoughtful-coder` to reuse as "before" proof in [templates/verification-artifacts.md](../templates/verification-artifacts.md).
- **Evidence:** `path:line`, logs, traces, and ruled-out explanations (unconfirmed theories separately).
- **Fix scope:** affected callers/data, smallest clean fix location, and required regression + live checks.
- **Tier 1 Guardrail Candidate:** if caused by a recurring mechanical agent error, recommend a Tier 1 lint rule or hard-ban with 3-part diagnostic ([lint-rules/README.md](../lint-rules/README.md)).
- **Approval status:** whether implementation is approved.

Stop after diagnosis unless coding is approved.
