---
name: refactor
description: Refactors the code you name for clarity in small steps, running the tests after each step so behavior never changes.
disable-model-invocation: true
---

Refactor for clarity: $ARGUMENTS

1. Read the code and everything that calls it. Write down in two lines what it does today. Behavior must not change.
2. Run the test suite first and note the result. If the code is not covered, add characterization tests that capture current outputs, including odd cases, and run them green before any edit.
3. List the smells you see (long function, deep nesting, duplicated block, unclear names, mixed concerns) and propose at most five steps, smallest first.
4. Do one step at a time: make the change, run the tests, and move on only when green. If a test fails, undo that step with `git checkout -- <file>` on your own edit and rethink; do not edit the tests to pass.
5. Do not change public signatures, file names or formatting unrelated to the task.
6. Stop after the agreed steps; do not keep polishing.

Finish with the list of steps done, the test results after each, and the diff stat. Ask before committing.
