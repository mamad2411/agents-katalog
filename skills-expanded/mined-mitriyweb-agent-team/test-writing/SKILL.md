---
name: test-writing
description: Write and execute tests to verify the implementation.
compatibility: Requires bash, Claude Code
metadata:
  team: software-development
  role: qa
  version: "1.0"
---

## Procedure

1. **Discover project rules** — follow the Project Rules Discovery procedure from the team PROTOCOL. Read lint config and test config before writing any tests.
2. **Write lint-compliant tests** — your tests MUST pass the project's linter. Use patterns that the linter allows.
3. **Run tests** — use the test command discovered in step 1.
4. **Run lint on test files** — verify your new tests pass the linter. If they don't, fix them.
5. **Report failures** back to the developer with detailed logs.
6. **Iterate** until all tests pass AND lint is clean.

## Gotchas

- Tests must not require an API key or Docker unless explicitly specified.
- Read the project's lint rules BEFORE writing tests. Common violations:
  `testing-library/no-node-access`, `no-unused-vars`, `no-container`.
  Know the rules, write compliant code.
- If the project has a test setup file, read it to understand available mocks and globals.

## Validation loop

The QA role ensures that all tests pass, lint is clean, and no regressions are found in the existing test suite. A test that breaks lint is not a passing test.
