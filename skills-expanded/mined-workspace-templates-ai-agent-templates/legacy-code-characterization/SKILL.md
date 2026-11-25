---
name: legacy-code-characterization
description: Records what untested legacy code actually does by writing characterization tests first, so you can change or refactor it without guessing at behavior.
---

# Legacy code characterization

Describe what the code does, not what it should do. Do not fix anything in this step.

## Steps

1. Choose the seam: one function, class or endpoint. Read it and list its inputs, outputs, side effects (database, files, network, clock, randomness) and callers.
2. Make it testable without changing behavior. Replace time, randomness and network with test doubles at the edge, and use a temporary database or fixtures. If the code cannot be called without a rewrite, use the smallest wrapper or an extracted-but-identical function, and say so.
3. Collect realistic inputs: from existing fixtures, logs, call sites and sample data. Add boundaries: empty, zero, null, maximum length, unusual encodings and error cases.
4. Write a test per input that asserts the current output. If you do not know the output, run the code, read the result and paste it in as the expected value. Snapshot tests are fine for large outputs.
5. Run the suite three times to catch flaky tests. A test that fails randomly is not a safety net; find the hidden dependency.
6. Check coverage for the target (`--coverage`) and add inputs until each branch runs at least once.
7. Mark suspicious results. When the output looks wrong, keep the test, add a comment `// current behavior, looks like a bug` and list it.

## Rules

- Change no production logic in this step, except the minimal seam from step 2.
- Name tests after the input, not the expected value.
- Never delete a failing characterization test; ask first.

## Report

Tests added, branch coverage reached, the seams introduced, and a list of suspected bugs with their inputs.
