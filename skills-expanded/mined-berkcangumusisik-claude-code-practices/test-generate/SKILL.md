---
name: test-generate
description: Generates unit tests for a file or function with full coverage of edge cases
argument-hint: <file-path> [function-name]
user-invocable: true
allowed-tools: Read Glob Grep Edit
effort: medium
---

## Generate Tests

Target: **$1** $2

1. Read the file and understand:
   - What framework is used (Jest, Vitest, Mocha, pytest, Go test, etc.) - check existing test files for patterns
   - The function/class signatures, types, return values
   - Existing tests (if any) to match style

2. Identify test cases:
   - Happy path (normal usage)
   - Edge cases (null, undefined, empty, boundary values)
   - Error cases (thrown exceptions, rejected promises)
   - Async behavior if applicable

3. Write tests following the project's existing test style.

4. Place the test file next to the source or in `__tests__/` - match project convention.

5. Show a summary: N tests covering X scenarios.
