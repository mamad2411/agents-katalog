---
name: testing-guardian
description: Test coverage, quality, and mocking strategy review
argument-hint: "[files or scope]"
agent: testing-guardian
triggers:
  - user
  - model
allowed-tools:
  - read
  - grep
  - glob
  - exec
permissions:
  allow:
    - Exec(true)
    - Exec(/bin/true)
    - Exec(/usr/bin/true)
    - Exec(cp *)
---
> **Note:** Tests must be written in the same wave as implementation; see `CONVENTIONS.md`

Review test coverage and quality focusing on:

1. **Test coverage**
   - Overall coverage percentage
   - Coverage gaps in critical paths
   - Missing edge case tests
   - Uncovered error handling paths

2. **Test quality**
   - Test clarity and maintainability
   - Appropriate test isolation
   - Meaningful assertions
   - Test data management

3. **Mocking strategy**
   - Appropriate use of mocks vs. real implementations
   - Mock configuration correctness
   - Over-mocking issues
   - Integration vs. unit test balance

4. **Test patterns**
   - Arrange-Act-Assert structure
   - Test naming conventions
   - Setup/teardown appropriateness
   - Parameterized tests where beneficial

5. **Test performance**
   - Slow test identification
   - Unnecessary database/API calls
   - Test parallelization opportunities
   - Fixture optimization

## Review Scope
$ARGUMENTS

If no scope is provided, review test files in the current working directory.

## Output Format
Provide a structured report with:
- File paths and line numbers for each issue
- Coverage statistics by module
- Severity levels (critical, warning, info)
- Specific test quality issues
- Recommendations for improving test coverage
- Mocking strategy improvements
- Priority-ordered action items

## Tools
Use available test coverage tools if present:
- pytest for test execution
- coverage.py for coverage analysis
- pytest-cov for coverage reporting
