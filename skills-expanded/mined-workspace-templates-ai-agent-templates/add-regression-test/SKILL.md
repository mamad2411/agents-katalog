---
name: add-regression-test
description: Writes a test that fails on the bug you describe, proves it fails, then confirms it passes once the fix is in.
disable-model-invocation: true
---

Add a regression test for this bug: $ARGUMENTS

1. Restate the bug as input, expected result and actual result. If any of the three is unclear, ask one question and wait.
2. Find the code responsible and the nearest existing test file. Copy its naming, fixtures and assertion style. Do not add a new framework.
3. Write the smallest test that reproduces the bug at the lowest level possible (unit before integration). Use a name that states the behavior, not the ticket number alone.
4. Run it before any fix. It must fail, and the failure message must show the bug itself, not a typo or missing import. If it passes, the bug is not reproduced: say so and investigate.
5. If a fix is not in yet, show the proposed fix and ask before editing source. If it is already in, check out the previous version of the file with `git stash` or `git show` to confirm the test fails there.
6. Run the test again with the fix, then the surrounding test file.

Report: test file and name, red output, green output, and the one-line cause.
