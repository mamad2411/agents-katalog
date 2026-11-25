---
name: reproduce-bug
description: Turns a bug report into the smallest set of steps or a failing test and shows the actual failing output.
disable-model-invocation: true
---

Reproduce this bug and prove it fails: $ARGUMENTS

1. Extract from the report: expected behavior, actual behavior, inputs, environment, version. List what is missing; guess nothing silently.
2. Find the code path involved and the existing tests nearest to it. Copy their setup style.
3. Write the smallest reproduction: a unit test is best, otherwise a script or exact command with sample input. Remove every step that is not needed, one at a time, and re-run to confirm it still fails.
4. Run it. Capture the real output, exit code and the line where it breaks. If it passes, vary one input at a time (empty values, large sizes, time zones, concurrency) and report what you tried.
5. Save the test under the project's test folder with a name that describes the bug, but mark nothing as skipped.

Report: reproduction steps (numbered), the command to run, the failing output verbatim, and your confidence that this is the reported bug. If you cannot reproduce it, say so plainly and list the next information to request. Do not fix the bug in this step.
