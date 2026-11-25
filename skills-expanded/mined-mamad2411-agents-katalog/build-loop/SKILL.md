---
name: build-loop
description: Run a disciplined implement-verify-fix loop instead of writing a large batch of unverified code. Use when implementing any multi-step change, when a fix did not work on the first try, when several things are failing at once, or whenever you are tempted to write a lot of code before running anything. Enforces one change per verification cycle so failures stay attributable.
category: productivity
---

# Build Loop

The failure mode this prevents: write four hundred lines, run it, get six errors, fix all six speculatively, run again, get four different errors, and no longer understand the system. Recovery from that state costs more than the original task.

## The loop

```
1. Pick the smallest next increment that is independently verifiable
2. Implement only that
3. Run the verification
4. Read the actual output
5. Pass → commit-sized checkpoint, next increment
   Fail → one hypothesis, one change, back to 3
```

The whole discipline is step 5's failure branch. **One hypothesis, one change.** Making three speculative fixes at once means a pass teaches you nothing about which one mattered, and a failure teaches you nothing about which one broke it.

## Sizing an increment

Right-sized: "player moves left and right", "damage reduces health and emits the signal", "the save file writes and reads back". Each has an obvious pass/fail.

Too big: "combat system". Too small: "add one variable" — the verification overhead exceeds the work.

The test is whether you can state the pass condition in one sentence before you start. If you cannot, the increment is too big.

## Verification is not optional

Every increment ends with something actually executed. In a Godot project that is the `godot-verify` skill; elsewhere it is the test suite, a run command, or a manual check you describe precisely.

If you genuinely cannot run it — no engine binary, no test framework, sandboxed environment — say so explicitly at that point in the conversation. Do not substitute reading the code carefully for running it and then report the same confidence. Careful reading and passing tests are different claims and the user is entitled to know which one they got.

## When stuck

If three cycles pass with no progress, stop looping and change strategy:

- **Re-read the actual error text.** Not your summary of it from two cycles ago. Errors get paraphrased into something more convenient with each retelling.
- **Check the assumption underneath.** Is the file being edited the one being run? Is the change actually saved? Is there a cached build? Is the failing line even reached?
- **Shrink the reproduction.** Strip it to the smallest thing that still fails. The cause is usually obvious at that size.
- **Say you're stuck.** Three failed cycles and a clear description of what you tried is more useful to the user than a fourth guess. It is not a failure to report; it is the correct output of a loop that is not converging.

## Checkpoints

At each passing increment, state what now works and what is next in one line. This gives the user a place to redirect before more is built on a direction they did not want, and it means an interrupted session has a clear resume point.

## What not to do

- Do not report "should work now" — run it or say you could not.
- Do not fix an error you have not read in full.
- Do not silently expand scope mid-loop. If you find a second problem, name it and ask whether it is in scope now.
- Do not disable a failing test to make the loop green. That is not a pass.
