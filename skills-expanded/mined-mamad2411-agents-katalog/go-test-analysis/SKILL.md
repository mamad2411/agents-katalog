---
name: go-test-analysis
description: Go test coverage analysis — find gaps, suggest missing tests
context: fork
agent: Explore
---

# Go Test Coverage Analyzer

Analyze Go test coverage to find gaps and suggest missing tests.

## Steps

1. **Discover Go modules**: Find all `go.mod` files to identify module boundaries. For each module, identify the package structure.

2. **Identify source files**: For each package, catalog the `.go` source files (excluding `_test.go`) and their exported functions, methods, and types.

3. **Identify test files**: For each package, catalog the `_test.go` files and map which functions/methods they test.

4. **Coverage gap analysis**: Compare source functions against test coverage to identify:
   - Packages with no test files at all
   - Exported functions/methods with no corresponding test
   - Complex functions (high cyclomatic complexity, multiple branches) that lack thorough testing
   - Error paths that are untested

5. **Priority ranking**: Rank uncovered code by importance:
   - **Critical**: Public API handlers, authentication/authorization, data mutations
   - **High**: Business logic, data transformations, validation
   - **Medium**: Utility functions, helpers
   - **Low**: Simple getters/setters, constants

6. **Test suggestions**: For the top gaps, suggest concrete test cases including:
   - Test function name and signature
   - Table-driven test structure where appropriate
   - Edge cases to cover (nil inputs, empty slices, boundary values, error conditions)

Present the final report as a prioritized list of coverage gaps with suggested test outlines.
