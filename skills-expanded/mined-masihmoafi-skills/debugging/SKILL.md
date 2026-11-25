---
name: debugging
description: Use for any bug, failing test, crash or unexpected behaviour, before proposing a fix. Root cause first, one hypothesis at a time, and a stop after three failed fixes.
---

# Debugging

No fix without a root cause. A fix that removes the symptom leaves the cause to come back elsewhere.

## 1. Find the cause

1. **Read the whole error**: message, stack, exit code. A wrapper that hides the exception ("query failed (ValueError)") gets unwrapped first.
2. **Reproduce it** with one command or action. If you cannot, gather evidence before guessing.
3. **Check what changed**: recent commits, dependencies, config, environment.
4. **Check the environment before the code**: proxy, network, credentials, versions, which binary actually runs. A timeout raised to hide a proxy that was never used is a symptom fix.
5. **Across components** (CI → build → sign, API → service → database), log what enters and leaves each boundary once, find the layer where it breaks, then look inside that layer.
6. **Trace bad data backwards** to where it was first wrong.

## 2. Compare

Find similar code that works, read it completely, and list every difference, however small.

## 3. One hypothesis

Write "X is the cause because Y", make the smallest change that tests it, one variable at a time. If it fails, form a new hypothesis; never stack fixes. If you do not understand something, say so.

## 4. Fix

Write a test that fails on the current code for this reason, make one fix at the cause, and run the test and its neighbours. If three fixes have failed, or each fix surfaces a new problem somewhere else, stop: the design is wrong. Say so and discuss it before fix number four.

If the cause is truly external (timing, a remote service), record what you checked and add handling and logging; most "no root cause" cases are an investigation that stopped early.

## Signs you skipped a step

"Is that not happening?" (you assumed), "Stop guessing", "We're stuck?", "just try this first", "one more fix". Each means: back to step 1.

Adapted from [obra/superpowers](https://github.com/obra/superpowers) `systematic-debugging` (MIT, © 2025 Jesse Vincent).
