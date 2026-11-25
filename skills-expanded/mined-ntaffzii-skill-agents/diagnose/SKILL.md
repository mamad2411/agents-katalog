---
name: diagnose
description: Disciplined diagnosis loop for bugs, failing tests, crashes, incorrect behavior, and performance regressions. Use when the user asks to debug, investigate, diagnose, find root cause, or provides an error log, stack trace, flaky behavior, or regression.
---

# Diagnose

Use this skill to find root cause before changing code.

## Core Rule

Build a reliable feedback loop before committing to a hypothesis. If there is no runnable signal, create one or explain exactly what is missing.

## Mantra

Reproduce, trace, falsify, validate.

## Workflow

1. Reproduce
   - Capture exact steps, inputs, environment, command, request, fixture, or UI path.
   - Prefer a fast deterministic signal: failing test, CLI command, curl script, browser script, replay harness, or benchmark.
   - If flaky, raise the reproduction rate with loops, stress, narrowed timing, pinned seeds, or isolated state.

2. Minimize
   - Reduce the repro to the smallest case that still shows the bug.
   - Confirm the minimized failure is the same symptom the user reported.
   - Avoid fixing a nearby but different failure.

3. Generate hypotheses
   - List 3 to 5 ranked hypotheses before testing.
   - For each, state a falsifiable prediction.
   - Prefer the hypothesis that explains every observed breadcrumb, not only the latest one.

4. Instrument
   - Test one variable at a time.
   - Prefer debugger or REPL inspection when available.
   - Use targeted logs only at boundaries that distinguish hypotheses.
   - Tag temporary logs with a unique prefix such as `[DEBUG-a4f2]`.
   - Keep a short ledger of experiments and observations when the investigation has more than one branch.

5. Fix
   - Write or preserve a regression signal before the fix when a correct seam exists.
   - Apply the smallest change that addresses the root cause.
   - Re-run the original repro and the minimized repro.

6. Clean up
   - Remove temporary instrumentation.
   - Delete throwaway harnesses or move them to a clearly named debug location.
   - State the root cause, mechanism, fix, and verification.

## Stop Conditions

Stop and ask for missing artifacts when:

- The issue cannot be reproduced locally.
- The only repro depends on an external system the agent cannot access.
- The user has logs, HAR files, screenshots, traces, or environment details that are required.

Do not invent a fix from code reading alone unless the user explicitly asks for a speculative review.

## Output Format

End with:

- Reproduction signal
- Root cause
- Fix summary
- Verification commands
- Remaining risk
