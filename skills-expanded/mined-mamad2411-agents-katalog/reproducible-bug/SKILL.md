---
name: reproducible-bug
description: "Shrink a failing input to the smallest reliable repro before filing or escalating. Improves signal-to-noise for whoever fixes the bug."
---

# Reproducible bug

A bug report without a deterministic repro wastes the engineer's time.
Before filing or escalating, **minimize**.

## When to apply
- A tool fails on input `X` but you suspect the failure is data-dependent
  (not pure env / auth).
- A code change you produced breaks a test and you need to file the
  regression cleanly.

## Method (binary-search style)

1. **Confirm** the failure with input `X` - run the tool once, capture the
   exact error.
2. **Halve `X`**: drop half of the input (rows, fields, args, file content).
   Re-run.
   - Fails the same way -> keep the smaller half.
   - Passes -> the dropped half contains the trigger; keep it.
3. **Repeat** until removing any single element makes the failure disappear.
4. **Capture** that minimal input verbatim - this is the repro for the bug
   report.

## What "minimal" includes
- The exact tool name + version (if exposed via `list_tools`).
- The smallest argument set that triggers the failure.
- Any precondition the tool depends on (auth state, prior call, file in
  sandbox).

## Stop conditions
- Each shrink takes < 30 seconds; if you have spent 5+ tool calls without
  progress, document what you tried and stop.
- If the failure becomes flaky during shrinking, mark the bug `flaky` and
  stop - flaky bugs are bugs too.

## What to hand to `self-report-agent-issue` or `file-bugs`
- Minimal failing input
- Minimal passing input (for diff)
- Number of shrink iterations + how long they took
- A copy/pasteable repro snippet that another agent or engineer can run
  end-to-end.
