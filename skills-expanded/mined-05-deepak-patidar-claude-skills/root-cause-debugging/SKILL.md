---
name: root-cause-debugging
description: Systematic debugging and incident diagnosis — finding the actual cause instead of patching symptoms. Use when investigating a bug, a production incident, flaky behavior, "works on my machine", data corruption, or when the user says "debug", "why is this happening", "broken", "investigate", "root cause", or pastes an error/stack trace.
---

# Root-Cause Debugging

Debugging is not staring at code hoping for insight; it is running experiments against hypotheses until only one survives. The cardinal sin is **fixing the symptom while the cause survives** — that bug returns wearing a different coat.

## The loop

1. **Reproduce first.** A bug you can trigger on demand is 80% solved. Capture: exact input, environment, frequency (always? sometimes? one tenant?). If you can't reproduce, your job changes: add instrumentation to catch it in the act, don't guess-fix.
2. **State the expected vs actual precisely.** "It's broken" → "POST /payments returns 500 for amounts > 999 since Tuesday's deploy". The precision itself often reveals the cause.
3. **Find what changed.** Bugs that appear have causes that arrived: last deploy (check the version fingerprint, not assumptions), dependency bump, config/env change, data shape change (first tenant with 10k products), date rollover (month/FY boundaries), certificate/token expiry. `git log` and deploy history before code-reading.
4. **Bisect the path.** Split the request's journey (client → network → handler → service → DB → response) and test the midpoint: is the data wrong *entering* the service or *leaving* it? Halving beats reading everything. `git bisect` when "which commit" is the question.
5. **One hypothesis, one experiment, one variable.** Write the hypothesis down ("the total is wrong because line discounts apply twice"), design the cheapest experiment that could *disprove* it, run it. Changing three things and seeing improvement teaches you nothing.
6. **Confirm the mechanism before fixing.** You've found root cause when you can (a) explain the mechanism end-to-end, (b) predict how to trigger AND how to prevent it, and (c) explain any weird details (why only Tuesdays? why only that tenant?). Unexplained details mean an unfound second cause — the fix that "works but I don't know why" is a time bomb.

## Reading evidence properly

- **Read the actual error, all of it, slowly.** The answer is in the stack trace's *first* frame in *your* code and the message's exact wording, more often than pride admits. The error you see may be downstream wreckage — find the *first* error in the timeline.
- Logs: reconstruct the timeline around one failing request via its correlation ID (observability-readiness). Compare against one *succeeding* request — the diff between them is the clue.
- Trust evidence over models: if the logs say the function received X and your mental model says impossible, the model is wrong. Print/log the actual values at the boundary in dispute; don't re-read code that "obviously" can't do that. It did.

## The usual suspects (check cheap ones first)

Environment/config diff (env var, version, timezone) · stale state (cache, build artifact, browser cache, connection pool holding old schema) · concurrency (double-click, race, retry duplicates — anything "intermittent" is concurrency or environment until proven otherwise) · boundary data (null, empty, zero, negative, unicode, DST, first-of-month, exactly-at-limit) · silent exception swallowed upstream leaving corrupt state · the transaction rolled back more than you thought (mutations lost with the error — see the tenant_session pattern) · it's not your code (dependency bug, platform outage — check status pages after 30 fruitless minutes).

## During a live incident, order inverts

**Stabilize first, understand later**: roll back the deploy / flip the flag / restart the thing — *after* snapshotting evidence (logs, metrics screenshots, a copy of bad data) so the crime scene survives the cleanup. Root-cause analysis happens on the stable system. Never debug forward on production under user pain when rollback exists (deployment-safety).

## Closing the loop — the part that compounds

A bug isn't fixed until:
1. The fix addresses the mechanism, not the symptom (deleting the bad row is cleanup, not a fix — what wrote it?).
2. A regression test exists that fails without the fix (testing-strategy rule: mandatory, not aspirational).
3. You've grepped for the same pattern elsewhere — bugs travel in families (the same missing tenant-filter, the same unhandled None).
4. For incidents: a 5-line blameless note — timeline, cause, fix, detection gap (why didn't monitoring catch it → fix that too), prevention.
