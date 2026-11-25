---
name: debugging-and-error-recovery
description: >-
  Systematic five-step triage for diagnosing, isolating, and fixing software
  defects. Covers everything from initial reproduction to post-mortem
  documentation. Designed to replace guesswork with a repeatable forensic
  process.
---

# Debugging & Error Recovery

## Overview

Debugging is applied scientific method. When a defect surfaces, engineers
default to one of three modes: (1) staring at the code hoping for insight,
(2) peppering the codebase with speculative `print()` statements, or (3) a
structured five-step triage that converges on root cause in minimum steps.

This skill enforces mode (3). Every bug deserves a reproducible test case,
a bounded search space, a minimal diff, a targeted fix, and a guard that
prevents re-introduction. Anything less is gambling.

## When to Use

- A test fails and the reason is not immediately obvious
- A production incident produces unexpected behavior
- A flaky test needs deterministic root-causing
- A regression is introduced between two known-good commits
- Error rates, latency, or crash counts exhibit unexplained changes
- A user reports behavior that cannot be reproduced locally
- A dependency upgrade introduces subtle breakage

## Process

### Step 1: Stop the Line & Reproduce

The **stop-the-line rule**: when a defect is confirmed, all non-critical work
pauses until either (a) the bug is fixed, or (b) a deliberate decision is made
to defer with a tracked issue. This prevents the common failure mode of
stacking work on top of broken foundations.

**Actions:**
1. Create a fresh, minimal reproduction environment (new checkout, clean
   dependencies, no local state) — eliminate the "works on my machine" class
   of error before proceeding.
2. Write a test that fails with the observed behavior. If the bug is
   intermittent, run the test 100+ times to establish a baseline failure rate.
3. Capture the exact error message, stack trace, input data, and environment
   (OS, runtime version, dependency versions, locale, timezone).
4. If the bug originates in production: snapshot the request, response,
   relevant logs, and any tracing context. Attach these to the bug tracker
   entry before touching any code.

**Exit criteria:** A failing automated test or a documented, repeatable
manual procedure that produces the unwanted behavior every time.

### Step 2: Localize — Binary Search the Search Space

Narrow the defect to a single module, function, or line. Use systematic
elimination, not intuition.

**Actions:**
1. Identify the **independent variable** — what changed? Recent commit,
   config toggle, input data, dependency version, environment.
2. If the culprit is a recent change: use `git bisect` with a script that
   tests for the defect. Automate the check so it runs unattended.
3. If the culprit is input-dependent: binary-search the input space. Halve
   the input, check if the bug reproduces, recurse on the failing half.
4. If the culprit is a configuration change: diff the config before/after
   and test each diff hunk independently.
5. Insert logging probes using the **divide-and-conquer** pattern: log at
   module boundaries first, then zoom into the failing module, then the
   failing function, then the failing branch.
6. Use `rr` (record and replay), time-travel debuggers, or replay frameworks
   to step backwards from the crash site.

**Anti-pattern:** Adding 50 log statements at once. Add one, re-run, interpret.

**Exit criteria:** A single function or expression identified as the root
cause, demonstrable by toggling it on/off.

### Step 3: Reduce — Minimal Reproduction

Strip away everything that is not directly involved in the failure. The
goal is the shortest path from start to defect.

**Actions:**
1. Remove unrelated setup code, mock out dependencies, delete test code that
   does not contribute to the failure.
2. Reduce input data to the smallest possible payload that still triggers
   the bug (Delta Debugging).
3. If the bug depends on state: identify the minimum sequence of operations
   that creates the offending state.
4. If the bug is a race condition or timing issue: add explicit synchronization
   to prove the race exists, then remove synchronization one piece at a time
   to find the critical section.

**Exit criteria:** A self-contained test case under 50 lines (or equivalent
simplicity in the target language) that fails with the original error.

### Step 4: Fix — Surgical Correction

Apply the minimum change that eliminates the defect. Every fix is a hypothesis:
"I believe this change resolves the root cause without breaking existing
behavior."

**Actions:**
1. Write the fix. The diff should be as small as possible — ideally under
   20 lines changed. If the diff exceeds 100 lines, the fix is too invasive
   and likely introduces new defects.
2. Run the reproduction test: it must pass.
3. Run the full test suite: no regressions.
4. Add a **guard** — a test that explicitly covers the defect scenario so
   that a future regression is caught at commit time, not deploy time.
5. Consider whether the same defect class exists elsewhere (`grep` for the
   same pattern) and file follow-up issues for any matches found.

**Safe fallback patterns:**
- **Feature flag:** Ship the fix behind a flag so it can be toggled off
  instantly if something goes wrong.
- **Defensive copy:** Clone inputs before mutating rather than mutating in
  place, then reconcile later.
- **Canary deploy:** Roll the fix to a small percentage of traffic before
  full rollout.
- **Rollback commit:** Ensure the fix is a single commit that can be reverted
  atomically.

**Exit criteria:** Fix merged with passing guard test and clean CI.

### Step 5: Post-Mortem — Learn & Prevent

Document what happened, why, and how the process will prevent recurrence.

**Post-mortem template:**

```
## Summary
- Severity: P0/P1/P2/P3
- Duration: start_time → end_time
- Impact: users affected, revenue impact, data loss (yes/no)

## Timeline
- Detection: how was it found? (alert, user report, CI failure)
- Response: who responded, when, what actions taken
- Resolution: exact commit that fixed it, time of deploy

## Root Cause
- What was the defect? (one-line description)
- Why was it introduced? (process gap, misunderstood API, insufficient testing)
- Why was it not caught? (missing test, insufficient review, environmental diff)

## Corrective Actions
- Guard test added: path to test file
- Process change: what will be done differently
- Monitoring: any new alerts or dashboards added
- Tracking: link to follow-up issues

## Error Budget Impact
- How much of the error budget was consumed? (uptime, latency budget, crash budget)
- Is the budget being replenished? (timeline)
```

---

## Anti-Rationalization Table

| Excuse | Rebuttal |
|--------|----------|
| "I can see the bug just by looking at the code, no need to reproduce it." | Seeing the symptom is not understanding the trigger. Without reproduction you cannot prove the fix works, cannot write a guard test, and will likely miss edge cases. |
| "The bug is intermittent; it's not worth trying to reproduce deterministically." | Intermittent bugs are the most expensive class of defect. Invest the time to find the race/ordering condition — it will pay for itself 10x over. |
| "I'll just add a quick log statement to confirm my theory." | One log statement is fine. But if you have not articulated a hypothesis before adding it, you are guessing. Write the hypothesis first, then log to confirm or deny. |
| "The fix is urgent; we can clean it up later." | Urgency demands more rigor, not less. Hasty fixes deploy new bugs faster than they resolve old ones. The stop-the-line rule exists for this exact reason. |
| "I know what the problem is; I don't need to binary search." | Intuition is correct roughly 40% of the time for non-trivial bugs. Binary searching is faster than chasing wrong hunches and provides irrefutable evidence. |
| "This bug is too complex to write a minimal reproduction." | The complexity of the reproduction is proportional to your understanding of the bug. If you cannot write a minimal reproduction, you do not understand the bug well enough to fix it. |
| "The post-mortem is overhead; nobody reads it anyway." | Post-mortems are the primary mechanism for organizational learning. If nobody reads them, the problem is the culture, not the process. Start by writing good ones. |

## Red Flags

- Fix merged without a guard test → the same bug will recur
- More than one attempt to fix the same bug → root cause not found
- "I don't know how to reproduce it" after 30 minutes → need a different
  strategy (rr, tracing, bisect)
- Fix diff exceeds 100 lines → too much changed, regression risk is high
- No post-mortem for P0/P1 incidents → organizational memory is being lost
- Logging added but never removed → technical debt accumulating
- "Works on my machine" → environment mismatch not reconciled
- Fix applied to symptom rather than cause → same symptom will reappear

## Verification

1. Run the reproduction test: does it pass after the fix?
2. Run the full test suite: any regressions?
3. Run `git bisect` from known-good to fixed: confirms the exact commit
   that introduced the bug and the exact commit that fixed it.
4. Run the guard test in CI on the target branch: it should fail before the
   fix and pass after.
5. Deploy to canary/staging: verify the error rate drops to baseline.
6. Update the error budget tracker: document how much budget was consumed.
7. Review the post-mortem with the team within 48 hours of resolution.
