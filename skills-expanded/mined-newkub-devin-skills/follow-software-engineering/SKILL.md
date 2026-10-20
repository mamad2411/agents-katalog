---
name: follow-software-engineering
description: Design and write software that is easy to test, easy to scale, easy to debug, and easy to use
argument-hint: "[scope]"
related:
  - follow-math-concepts
  - deep-review-codebase
---

## Goal

Design and write software that is easy to test, easy to scale, easy to debug, and easy to use

## Scope

Use for designing architecture, writing code, and designing UX/UI of any kind of project

## Execute

### 1. Design Testable & Scalable Architecture

> Goal: Design Testable & Scalable Architecture

Design an architecture that is easy to test and easy to scale

1. Run `/deep-review-codebase` for the foundational structure
2. Separate business logic from infrastructure
3. Use dependency injection for external dependencies
4. Create interfaces for external services
5. Design modules that are independent and loosely coupled
6. Use stateless design for scalability
7. Design the cache strategy
8. Use async patterns for I/O operations

### 2. Write Debuggable & Testable Code

> Goal: Write Debuggable & Testable Code

Write code that is easy to debug and easy to test

1. Run `/deep-review-codebase` to separate pure logic from side effects
2. Write business logic as pure functions
3. Use clear, meaningful naming
4. Write small, focused functions (max 20-30 lines)
5. Add meaningful, structured logging
6. Handle errors explicitly with typed errors
7. Write defensive code with input validation
8. Add observability (metrics, traces, health checks)

### 3. Design for Usability

> Goal: Design for Usability

Design for ease of use

1. Run `/deep-review-codebase` for design system principles
2. Design APIs that are intuitive and consistent
3. Use sensible defaults
4. Add auto-completion and discoverability
5. Design helpful error messages
6. Provide clear examples and documentation
7. Design smooth onboarding
8. Add immediate, clear feedback

### 4. Create Clear Boundaries

> Goal: Create Clear Boundaries

Create clear boundaries between layers

1. Run `/deep-review-codebase` for layer separation
2. Define interfaces between layers
3. Use the ports and adapters pattern
4. Separate domain logic from application logic
5. Separate presentation logic from business logic

### 5. Implement Testing Strategy

> Goal: Implement Testing Strategy

Manage testing systematically

1. Run `/update-tests` for the testing strategy
2. Write unit tests for pure functions
3. Write integration tests for adapters
4. Write E2E tests for critical flows
5. Create reusable test fixtures
6. Use test doubles for external dependencies
7. Set high coverage targets

### 6. Add Documentation

> Goal: Add Documentation

Add complete documentation

1. Write JSDoc for public functions
2. Describe parameters and return values
3. State the side effects
4. Provide clear examples
5. Write a complete README
6. Keep documentation updated continuously

## Rules

### 1. Architecture Rules

Rules for architecture

- Separation of Concerns: separate business logic, infrastructure, presentation
- Dependency Injection: inject dependencies through constructors
- Pure Functions: business logic as pure functions
- Clear Boundaries: define interfaces between layers
- Scalability: stateless design, cache strategy, async patterns
- Testability: dependency injection, test doubles, pure functions

### 2. Code Quality Rules

Rules for code quality

- Clear Naming: names state purpose, verbs for functions, nouns for variables
- Small Functions: single responsibility, max 20-30 lines, composition over nesting
- Meaningful Logging: log critical points, structured logging, contextual information
- Explicit Error Handling: typed errors, propagate clearly, meaningful messages
- Self-Documenting: clear naming, no magic numbers, use constants
- Defensive Programming: input validation, edge case handling, type guards
- Observability: key metrics, distributed tracing, health checks

### 3. Usability Rules

Rules for usability

- Intuitive API: consistent naming, predictable behavior
- Sensible Defaults: values that work for most cases
- Auto-Completion: DX first, discoverable APIs
- Helpful Errors: error messages that tell how to fix
- Clear Documentation: examples, tutorials, guides
- Smooth Onboarding: quick start, progressive disclosure
- Immediate Feedback: fast response, clear status

### 4. Testing Rules

Rules for testing

- Unit Tests: test pure functions with the AAA pattern
- Integration Tests: test adapters with mock ports
- E2E Tests: test critical flows on real environment
- Test Fixtures: reusable shared test data
- Test Helpers: test utilities for setup/teardown
- High Coverage: set high coverage targets
- Fast Execution: tests should run quickly

### 5. Documentation Rules

Rules for documentation

- JSDoc: for public functions
- Purpose/Parameters/Return: described clearly
- @throws: list the errors that may be thrown
- @example: provide working examples
- README: complete coverage
- Up-to-date: continuously updated

- Use /follow-math-concepts if needed

## Expected Outcome

- Architecture that is easy to test and easy to scale
- Code that is easy to debug and easy to test
- Design that is easy to use and intuitive
- Business logic that is pure and testable
- Clear boundaries between layers
- Good dependency injection
- High observability and debuggability
- High test coverage
- Complete documentation
- Excellent developer experience
