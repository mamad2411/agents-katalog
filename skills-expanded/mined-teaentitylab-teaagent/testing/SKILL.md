---
name: testing
description: Use when writing, running, or debugging tests across unit, integration, and acceptance test suites.
tags: testing, quality, tdd, unit-test, integration-test
---

# Testing Skill

Use this skill when writing or running tests for the codebase.

## Workflow

1. Identify test location: find existing test files and patterns
2. Write tests: follow project conventions and test structure
3. Run tests: execute test suite with appropriate flags
4. Debug failures: analyze test output, fix issues
5. Verify coverage: ensure critical paths are tested

## Test Types

- **Unit Tests**: Test individual functions/classes in isolation
- **Integration Tests**: Test component interactions
- **Acceptance Tests**: Test user-facing functionality
- **E2E Tests**: Test full user workflows

## Key Tools

- `shell` - Run test commands (pytest, unittest, etc.)
- `workspace_read_file` - Read test files
- `workspace_write_file` - Write new tests

## Rules

- Follow project's test naming conventions (`test_*.py`, `*_test.py`)
- Use descriptive test names that explain what is being tested
- Follow AAA pattern: Arrange, Act, Assert
- Keep tests independent and isolated
- Mock external dependencies appropriately
- Aim for meaningful assertions, not just "no exceptions"

## Test Organization

```
tests/
├── unit/          # Unit tests
├── integration/   # Integration tests
├── acceptance/    # Acceptance tests
└── e2e/           # End-to-end tests
```

## References

- See the test types and rules sections above for detailed testing patterns and fixtures.