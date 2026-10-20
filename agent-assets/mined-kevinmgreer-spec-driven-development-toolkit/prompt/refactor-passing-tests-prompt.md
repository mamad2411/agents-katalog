---
description: "Safely refactor an implementation after all acceptance tests are passing. Improves code quality without changing behavior. Runs tests after each change to keep everything green."
agent: agent
tools: [read, edit, search, execute]
argument-hint: "Feature name, or path to implementation file(s) to refactor"
---

Refactor the implementation for:

${input}

**Precondition**: All acceptance tests must be green before starting. Run them first to confirm.

## Steps

1. Run the test suite — confirm all tests are **green** before making any changes
2. Review the implementation for:
   - **Duplication**: Repeated logic that can be extracted into a function or shared module
   - **Clarity**: Variable, function, or class names that don't express intent
   - **Complexity**: Functions doing more than one thing (violating Single Responsibility)
   - **Structure**: Logic placed in the wrong layer or module

3. Make **one focused change at a time**:
   - Extract a function
   - Rename a variable or method
   - Simplify a conditional
   - Move a responsibility to the correct module

4. Run tests after **every single change**
5. If tests fail after a refactor, **revert that change immediately** and try a different approach
6. Stop when the code is clean — do not add design patterns or abstractions speculatively

## Rules

- Do NOT add new features or behavior
- Do NOT modify test files
- Do NOT change public APIs unless clearly improving them (and tests confirm they still pass)
- Do NOT add error handling not covered by an existing `@error` scenario
- When in doubt about a change — skip it

## Report

When complete:

- List each change made (what was changed and why)
- Confirm all tests still green
- Note anything intentionally left unchanged (and why)
