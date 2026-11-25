---
name: simplify-code
description: Cuts the length and nesting of one function without changing what it does, and proves it with before and after tests.
disable-model-invocation: true
---

Simplify this function without changing behavior: $ARGUMENTS

1. Read the function and its callers. Record the starting numbers: lines, deepest nesting level, count of branches.
2. Make sure tests cover it. If a path is untested, add a test for it first, using real inputs from the code. Run them.
3. Apply, in this order, and stop when the code reads cleanly: guard clauses instead of nested else; remove branches that cannot happen; merge duplicated branches; replace flag variables with direct returns; use the language's built-ins (map, filter, any, get with default) over hand loops; delete unused variables and parameters that no caller passes.
4. Keep the same inputs, outputs, exceptions and side effects, including their order. If a change might alter behavior in an edge case, do not make it; list it instead.
5. Run the tests after the edit and compare with the starting numbers.

Show the old and new function side by side with the numbers. Do not touch other functions or ask to commit before showing the diff.
