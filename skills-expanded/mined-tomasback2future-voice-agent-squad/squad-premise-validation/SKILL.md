---
name: squad-premise-validation
description: Before fixing a claimed bug, prove the bug exists by writing a RED test against the current code. If the test passes unmodified, the bug does not reproduce — reclassify, do not "fix" a non-bug.
allowed-tools:
  - Bash
  - Read
  - Edit
disable-model-invocation: false
---

# Premise validation: RED first, always

Every BUG item carries a premise: "this code is wrong, here is the symptom." The premise is a claim, not a fact. Validate it before you spend time fixing it.

## When to use this skill

Invoke this skill any time you have just claimed a BUG item whose acceptance criteria name a concrete, testable failure ("returns wrong value for `(2^33-1, 0)`", "cue injected during stall fires 200ms late", "duplicate request returns 500 instead of 200"). The skill applies before any implementation, before any subagent dispatch, before reading more than the item file itself.

## The rule

Write the failing test FIRST, against the current code, and run it. Two outcomes:

1. **It fails (RED) for the reason the item describes.** The bug is real. Proceed with implementation. The test you just wrote becomes the regression test that goes into the same commit as the fix.
2. **It passes unmodified (GREEN against current code).** The claimed bug does not exist. Stop. Do not implement a "fix." Reclassify the item: `BUG → DEBT (clarity / coverage / audit)`, ship whatever clarity/coverage work the investigation surfaced, or close with "no repro" if there is nothing to ship. Add a reclassification line to the Resolution per the squad-loop close-out.

## Why this matters

Items rot. A symptom described two weeks ago might already be fixed by an unrelated commit. A line number cited in the body might point at different code now. Acceptance criteria written from memory might describe a behavior that the code never actually exhibited. If you skip premise validation, you will spend two hours "fixing" code that already works, ship a no-op patch, and then watch a future agent revert it because it is dead code.

The cost of premise validation is one test invocation — usually under 30 seconds. The cost of skipping it is two hours of wrong-direction work plus a confusing commit that future readers cannot connect to a real failure.

## How to apply

1. Read the item's `## Acceptance criteria` section. Identify the concrete failing scenarios.
2. Write the test that asserts the expected (post-fix) behavior. Place it in the test file next to the code under suspicion.
3. Run the test. Read the output carefully — does it fail for the *reason the item describes*, or does it fail for some unrelated reason (compile error, wrong assertion shape)?
4. If RED for the right reason: implement the fix, watch the test go green, commit both together.
5. If GREEN unchanged: stop. Investigate why the item's premise is wrong (rotted? wrong file? wrong version?). Reclassify per the loop.
6. If RED for an unrelated reason: fix your test, then return to step 3.

## Anti-patterns to avoid

- Writing the test after the implementation. You lose the proof that the bug existed.
- Writing a test that asserts "the new code path runs" rather than "the bug symptom no longer reproduces." The test must reproduce the bug to be a regression test.
- Quietly closing an item as "fixed" when the test would have passed against the original code. Future agents cannot tell apart real fixes from no-op fixes; reclassification is the signal that distinguishes them.
- Dispatching a subagent to "fix" a bug whose premise you have not validated. The subagent cannot ask you mid-task; it will produce a fix and you will not know whether it was needed.
