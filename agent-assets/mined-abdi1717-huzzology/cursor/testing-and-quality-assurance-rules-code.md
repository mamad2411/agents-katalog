---
description: Testing and quality assurance standards for unit, integration, and end-to-end testing
globs: "**/*.{test,spec}.{js,jsx,ts,tsx}", "**/__tests__/**/*"
alwaysApply: true
---

# Testing and Quality Assurance Rules

## Test Strategy
- Write tests before or alongside code (TDD/BDD)
- Aim for high test coverage (80%+ line coverage)
- Test behavior, not implementation
- Use appropriate test types (unit, integration, e2e)
- Mock external dependencies appropriately
- Test edge cases and error conditions

## Unit Testing
- Test single units of functionality
- Keep tests fast and isolated
- Use descriptive test names
- Follow AAA pattern (Arrange, Act, Assert)
- One assertion per test when possible
- Test both positive and negative cases

## Integration Testing
- Test component interactions
- Use real dependencies where appropriate
- Test data flow between components
- Verify external service integrations
- Test configuration and environment setup
- Validate error propagation

## End-to-End Testing
- Test complete user workflows
- Use page object model for UI tests
- Test critical business paths
- Validate user experience
- Test across different environments
- Include performance considerations

## Test Data Management
- Use factories for test data creation
- Keep test data isolated and clean
- Use realistic but safe test data
- Implement proper test data cleanup
- Version control test fixtures
- Avoid production data in tests

## Quality Gates
- All tests must pass before merge
- Maintain code coverage thresholds
- Run linting and formatting checks
- Perform security scans
- Check for performance regressions
- Validate documentation updates

## Testing Tools and Frameworks
- Choose appropriate testing frameworks
- Use code coverage tools
- Implement continuous testing
- Use mutation testing when beneficial
- Integrate with CI/CD pipelines
- Monitor test execution times
## Test Maintenance
- Refactor tests with production code
- Remove obsolete tests
- Update tests for changed requirements
- Keep test code clean and readable
- Review test failures promptly
- Maintain test environment consistency
