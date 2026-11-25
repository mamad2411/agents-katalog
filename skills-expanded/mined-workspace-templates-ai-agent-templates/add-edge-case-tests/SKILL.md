---
name: add-edge-case-tests
description: "Adds tests for the boundary and error cases of one function: empty, huge, null, malformed and surprising input."
disable-model-invocation: true
---

Add edge case tests for this function: $ARGUMENTS

1. Locate the function, its types or docstring, its callers and any existing tests. Note its contract: accepted input, return value, thrown errors.
2. List edge cases by category: empty (empty string, list, object), null or undefined, boundaries (0, 1, -1, max, max plus one), size (very long strings, 100k items), text (unicode, emoji, combining marks, newlines, leading and trailing whitespace), numbers (NaN, Infinity, floats like 0.1 + 0.2, very large integers), dates (leap day, DST change, timezone), type confusion, and repeated or concurrent calls.
3. Predict the expected result for each from the contract. Where the contract is silent, mark the case as a question rather than guessing.
4. Write the tests in the existing style, one behavior per test, with readable names. Use table-driven or parameterized tests where the framework supports them.
5. Run them. For any failure, decide if the function has a bug. Do not edit the function and do not weaken the test; list the bug.

Report tests added, passes, and bugs or open questions found. Ask how to resolve each.
