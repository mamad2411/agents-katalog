---
name: fix-failing-tests
description: Runs the suite, groups failures by shared cause and fixes one cause at a time, rerunning after each fix.
disable-model-invocation: true
---

Fix the failing tests. Scope: $ARGUMENTS (the full suite if empty).

1. Find the test command in package.json, Makefile, pyproject or CI config and run it. Save the failing test names and first error line for each.
2. Group failures by cause: same stack frame, same error message, same missing fixture, same changed import. Name each group and count its tests.
3. Take the largest group first. Read the test and the code it exercises and decide whether the code is wrong, the test is stale, or the environment is the problem (time, order, network, missing env var).
4. Fix the root cause with the smallest change. Never delete a test, skip it, loosen an assertion or add retries just to turn it green. If one of those is truly right, explain why and ask.
5. Rerun only the affected tests, then the full suite before moving to the next group.

Finish with a summary: groups fixed, tests per group, what changed, anything still red with your diagnosis. Ask before committing.
