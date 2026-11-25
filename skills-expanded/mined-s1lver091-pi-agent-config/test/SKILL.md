---
name: test
description: Write tests for existing code or new features. Use when asked to add tests, improve test coverage, or write tests for a specific function or module.
---

# Writing Tests

Tests verify behavior, not implementation. A test that breaks when you rename a variable is a bad test.

## Step 1: Understand what to test

Before writing any test:
- Read the function or module you are testing in full
- Identify its contract: given input X, what output or side effect is promised?
- Find existing tests to understand the pattern in this codebase

## Step 2: Identify the cases

For every function or behavior, enumerate:

**Happy path**
The normal input that produces the expected output.

**Boundary cases**
- Empty input (empty string, empty array, zero, null)
- Single element vs. many elements
- Min and max values
- Exact boundary values (e.g. >= vs >)

**Error cases**
- Invalid input: what should happen?
- Missing required fields
- Network failure, file not found, permission denied

**Edge cases specific to the logic**
Think about what could go wrong given how the code works.

## Step 3: Write the tests

Follow the existing test framework and style in the codebase. Do not introduce a new testing library.

Structure each test as:
1. **Arrange**: set up inputs and any mocks or state
2. **Act**: call the function
3. **Assert**: verify the outcome

```typescript
it("returns null when the token is expired", () => {
  // Arrange
  const token = createToken({ expiresAt: new Date("2000-01-01") });

  // Act
  const result = validateToken(token);

  // Assert
  expect(result).toBeNull();
});
```

Rules:
- One assertion per test (or logically grouped assertions about the same outcome)
- Test names describe the behavior, not the implementation: "returns null when token is expired" not "test validateToken case 3"
- Do not test private implementation details
- Mock only external dependencies (network, filesystem, time), not your own code

## Step 4: Verify

- Run the tests and confirm they pass
- Temporarily break the implementation to confirm each test actually catches the failure
- Check that test names read clearly in the output

## Report format

**Tests written**
- `path/to/file.test.ts` — what behaviors are now covered

**Cases covered**
List the scenarios now tested.

**Cases not covered**
Any gaps you identified but did not write tests for, and why (e.g. requires integration setup, out of scope).
