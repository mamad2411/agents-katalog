---
name: debug-root-cause
description: Systematic root-cause debugging - reproduce, hypothesize, instrument, verify, then fix. Use when the user reports a bug, failure, crash, or flaky behavior and the cause is not already known.
---

# Root-Cause Debugging

Never patch a symptom. Follow this loop:

1. **Reproduce.** Find or build the smallest reliable reproduction (a
   failing test is ideal). If you cannot reproduce it, say so and gather
   more evidence (logs, inputs, environment) before proceeding.
2. **Hypothesize.** State one specific, falsifiable hypothesis about the
   cause. Rank multiple candidates by likelihood if you have them.
3. **Instrument.** Add targeted logging/assertions or use a debugger to
   confirm or refute the hypothesis. Prefer observing the live failure
   over reading code and guessing.
4. **Verify the cause.** You have the root cause only when you can explain
   the full chain from trigger to symptom and predict the failure.
5. **Fix at the cause.** Apply the fix at the level where the invariant
   broke, not where the error surfaced. Re-run the reproduction.
6. **Sweep.** Check for the same pattern elsewhere in the codebase and
   remove any temporary instrumentation.

## Report format

- **Root cause:** one paragraph, the causal chain.
- **Fix:** what changed and why this level is the right one.
- **Evidence:** how the reproduction behaved before and after.
