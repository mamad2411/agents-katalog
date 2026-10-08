---
description: 
globs: 
alwaysApply: true
---
# TDD Rules

_Rules to ensure Test-Driven Development practices are followed throughout the codebase_

## TypeScript Testing Requirements

**ID**: TDD-000  
**Severity**: critical  

TypeScript is required for all JavaScript code including test files

- All test files for frontend code must use TypeScript (.ts or .tsx extensions)
- Type checking must be enabled in test configuration
- Test data must use proper TypeScript interfaces/types
- No use of `any` type in test files; use appropriate type definitions instead
- Mock objects and functions must have proper TypeScript typing

## Test Coverage for New Code

**ID**: TDD-001  
**Severity**: error  

Every new feature or module must have corresponding test files with adequate coverage

- Each new module should have a corresponding test file or test module
- Tests should cover happy paths, edge cases, and potential failure scenarios
- Minimum code coverage for new features should be 80%
- Test files should follow the naming convention: [filename]_test.py or test_[filename].py
- TypeScript components must have test files with .test.tsx or .spec.tsx extensions

## Test Before Implementation

**ID**: TDD-002  
**Severity**: warning  

Tests should be written before the implementation code (Red-Green-Refactor)

- Create failing tests first to define expected behavior
- Write the minimum implementation to make tests pass
- Refactor code while maintaining passing tests
- Commit history should show test files created or modified before implementation files
- For TypeScript components, define interfaces/types as part of the test-first approach

## Test Class and Method Naming

**ID**: TDD-003  
**Severity**: info  

Test classes and methods should follow naming conventions that clearly indicate what they test

- Test classes should be named with 'Test' prefix or suffix (e.g., TestUserAuthentication)
- Test methods should use descriptive names that indicate what is being tested (e.g., test_user_can_login_with_valid_credentials)
- Use snake_case for test method names in Python
- Use camelCase for test method names in TypeScript (e.g., itShouldRenderUserNameCorrectly)
- Names should describe the scenario and expected outcome

## Unit vs Integration Tests

**ID**: TDD-004  
**Severity**: warning  

Tests should be properly categorized as unit or integration tests

- Unit tests should focus on testing a single component in isolation, using mocks for dependencies
- Integration tests should validate the interaction between components
- Unit tests should be placed in the 'tests/unit/' directory
- Integration tests should be placed in the 'tests/integration/' directory
- End-to-end tests should be placed in the 'e2e_tests' directory
- TypeScript unit tests should be co-located with the component files

## Test Requirements Traceability

**ID**: TDD-005  
**Severity**: warning  

Tests should link back to specific requirements from the requirements documentation

- Each test class should include a docstring that references the requirements being tested
- Use @requirement annotation to link tests to specific requirements documents
- Format: @requirement [document_name]:[section]:[subsection]
- Test for edge cases defined in the requirements
- For TypeScript tests, use JSDoc comments with @requirement tag

## Mocking External Dependencies

**ID**: TDD-006  
**Severity**: warning  

Tests should use mocks for external dependencies to ensure unit isolation

- Use mock objects for external services, APIs, and databases
- Explicitly define the expected behavior of mocked dependencies
- Only mock direct dependencies, not the system under test
- Reset mocks between tests to prevent test interference
- For TypeScript, use properly typed mock implementations with jest.mock()

## Test Independence

**ID**: TDD-007  
**Severity**: error  

Tests should be independent and not rely on the state from other tests

- Each test should set up its own test environment
- Tests should not depend on execution order
- Clean up resources and state after each test
- Use setUp and tearDown methods (or fixtures) for Python tests
- Use beforeEach and afterEach for TypeScript/Jest tests

## Performance Tests

**ID**: TDD-008  
**Severity**: info  

Critical functionality should include performance tests that validate response times

- Define performance benchmarks based on requirements
- Create tests that measure execution time of critical operations
- Performance tests should be tagged and can be run separately from regular tests
- Test should fail if performance falls below defined thresholds
- Include TypeScript-specific performance testing for frontend components

## Test Factories

**ID**: TDD-009  
**Severity**: warning  

Use the factory pattern for test data creation to ensure consistency and readability

- Create factory classes for each major model in the system
- Implement factories with sensible defaults and customization options
- Use factories to reduce code duplication across tests
- Ensure factories create valid model instances that pass validation

## End-to-End Testing

**ID**: TDD-010  
**Severity**: error  

Implement end-to-end tests for critical user flows to validate complete system functionality

- Use browser automation tools (Selenium/Playwright) for UI testing
- Focus E2E tests on the most critical user workflows
- Maintain a small, focused set of E2E tests to avoid long test execution times
- Include tests for all supported browsers and devices as specified in requirements

