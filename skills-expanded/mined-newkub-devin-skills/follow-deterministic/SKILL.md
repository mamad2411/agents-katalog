---
name: follow-deterministic
description: Develop projects with deterministic programming — predictable outputs, no randomness
argument-hint: "[scope]"
related:
  - follow-math-concepts

---

## Goal

Develop projects with deterministic programming so code always produces identical output for the same input

## Scope

Use `follow-deterministic` for tasks and workflows that must be deterministic

## Execute

### 1. Use Pure Functions

> Goal: functions always return the same result for the same input, no randomness

Always write deterministic functions

1. Avoid `randomness`: `Math.random()`, `Date.now()`, external entropy
2. Avoid `side effects`: I/O, network calls, mutations
3. Always return the same value for the same input
4. Use `seeded random` for deterministic randomness
5. Isolate non-deterministic operations

### 2. Manage External State

> Goal: control external state via dependency injection so determinism is not broken

Manage external state properly

1. Inject external dependencies through parameters
2. Use dependency injection for external services
3. Mock external state for testing
4. Use deterministic mocks for non-deterministic operations
5. Document external dependencies clearly

### 3. Control Time Dependencies

> Goal: control time-dependent operations so every run is reproducible

Manage time-dependent operations

1. Use deterministic time sources for testing
2. Inject time/clock dependencies
3. Avoid reliance on real time
4. Use virtual time for async operations
5. Document time dependencies clearly

### 4. Handle Concurrency

> Goal: keep concurrent operations producing results in a stable order every run

Manage concurrent operations deterministically

1. Use deterministic ordering for async operations
2. Avoid race conditions
3. Use synchronization mechanisms explicitly
4. Test concurrent scenarios thoroughly
5. Document concurrency assumptions

### 5. Input Validation

> Goal: validate inputs before processing so output is predictable

Validate inputs strictly

1. Validate inputs before processing
2. Use type validation for type safety
3. Handle edge cases explicitly
4. Document input requirements
5. Return predictable errors for invalid inputs

### 6. Error Handling

> Goal: handle errors consistently and predictably every time

Handle errors deterministically

1. Return consistent error types
2. Use typed errors for predictability
3. Document error scenarios
4. Handle errors consistently
5. Test error paths thoroughly

### 7. Testing

> Goal: confirm functions always return the same result, via test cases

Write tests for deterministic behavior

1. Test input/output pairs
2. Test edge cases thoroughly
3. Mock external dependencies
4. Use deterministic test data
5. Verify consistent outputs

## Rules

### 1. Pure Functions

Functions must be deterministic where possible

- No `randomness`
- No `side effects`
- Same return value for the same `input`
- Isolate `non-deterministic` operations
- Use `seeded random` when necessary

### 2. External State

Manage external state properly

- Inject `dependencies`
- Use `dependency injection`
- Mock `external state`
- Document `dependencies`
- Isolate `non-deterministic` code

### 3. Time Dependencies

Manage time-dependent operations

- Inject `time/clock`
- Use `deterministic time` for testing
- Avoid `real-time` reliance
- Use `virtual time`
- Document `time dependencies`

### 4. Concurrency

Manage concurrent operations deterministically

- Use `deterministic ordering`
- Avoid `race conditions`
- Use `synchronization`
- Test `concurrent` scenarios
- Document `concurrency` assumptions

### 5. Input Validation

Validate inputs strictly

- Validate `inputs`
- Use `type validation`
- Handle `edge cases`
- Document `requirements`
- Return `predictable errors`

### 6. Error Handling

Handle errors deterministically

- Return `consistent` error types
- Use `typed errors`
- Document `error scenarios`
- Handle `consistently`
- Test `error paths`

- Use /follow-math-concepts if needed

## Expected Outcome

- Deterministic functions
- Predictable outputs for given inputs
- Consistent behavior every run
- Reliable tests
- Error handling that is predictable
- Code that is easy to debug
- Reproducible behavior
