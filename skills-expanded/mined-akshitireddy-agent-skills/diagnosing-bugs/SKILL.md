---
name: diagnosing-bugs
description: Diagnose a reported defect or performance regression through reproduction, targeted probes, and causal verification.
---

# Diagnose the reported defect

Adapted from Matt Pocock's diagnosing-bugs skill; see LICENSE.txt.

Establish the actual symptom and a useful feedback loop at the seam where the
failure occurs. Prefer an existing test, command, trace, or real interaction
that can distinguish the reported bug from nearby failures.

## Build evidence without blocking discovery

Read relevant code and logs to locate the failing path and construct a probe.
Confirm that the probe can expose the reported symptom before trusting its pass.
Reduce irrelevant inputs when that improves diagnosis, without requiring every
remaining input to be proven minimal before continuing.

For intermittent failures, record reproduction frequency and conditions. Use
bounded repetition, stress, or timing probes suited to the defect. A device or
production-only bug may need captured evidence or a longer-running probe; it
need not become a deterministic seconds-fast unit test.

If reproduction is unavailable, state the gap and continue evidence-led source
inspection or targeted diagnostics. Keep hypotheses tentative. Request only
the specific missing artifact, access, or decision that enables further work.
Do not add production instrumentation or access without authorization.

## Distinguish causes

Rank plausible explanations and define an observable prediction for each.
Choose the next probe by how well it separates those explanations. Change one
relevant variable at a time when possible; use a debugger, narrow logs, or
profiling appropriate to the failure. Performance work needs comparable
baseline measurements rather than adjectives.

Communicate findings that affect the user's decisions. A fixed number of
hypotheses or a checkpoint before every experiment is unnecessary.

## Protect diagnostic data

Inspect and share only the necessary redacted excerpts. Logs, HARs, URLs, dumps,
and screenshots can contain credentials and personal data. Keep authentication
in the user's normal application flow; never request passwords or tokens in a
diagnostic transcript. If human observation is necessary, ask for the relevant
action and symptom directly rather than requiring an interactive shell script.

## Complete the requested diagnosis or fix

For a diagnosis-only request, return the supported cause or ranked findings,
the evidence, and the exact unresolved question. Code changes are outside that
deliverable unless the user also requests a fix.

When fixing is in scope, correct the demonstrated cause. Where a durable regression test
can exercise the real failure pattern, make it fail before the fix and pass
afterward. Otherwise preserve the useful reproduction or explain the coverage
gap. Recheck the original scenario and run the affected project checks.

Remove task-owned temporary instrumentation and probes when no longer needed;
preserve user work and useful evidence. Report the cause, observed outcome, and
remaining uncertainty. A non-reproduction is not proof that a live fault is gone.
