---
description: 
globs: 
alwaysApply: true
---

# Rules

You are an expert Rust developer. When asked to do something, you should do ONLY what the USER asks you to do, your job depends on it and in the current economical situation, you're not getting a new job. While doing code changes, do not change comments or code that is not relevant to what user asked. You can still suggest edits for incomplete code.

## General Coding Principles

- Write clean, idiomatic Rust code that's easy to understand and maintain
- Handle all errors properly without excessive use of `.unwrap()` or `.expect()`
- Prefer using the `?` operator for error propagation where appropriate
- All public functions and types should have clear documentation comments
- Use meaningful variable and function names that reflect their purpose
- Follow the Rust naming conventions (snake_case for functions, CamelCase for types)
- All comments should be in English and should explain "why" not just "what"
- Keep the code properly formatted by running `cargo fmt`

## Error Handling

- Create custom error types using thiserror
- Return Result<T, E> from functions that can fail rather than panicking
- Use anyhow::Result for application code where error details aren't important
- Log errors appropriately before converting them to other error types
- Validate inputs early to prevent propagation of invalid data


## Project Structure

- Use modules to logically separate functionality
- Minimize public exports to keep the API surface clean
- Keep file size manageable (aim for <500 lines per file)
- Ensure dependencies between modules are clear and don't create cycles
- Use test modules for each functionality module

## Testing

- Write unit tests for all public functions
- Create integration tests for key functionality
- Test edge cases and error conditions, not just the happy path
- Use property-based testing for mathematical functions where appropriate
- Maintain test coverage above 80% for core simulation logic

## Performance

- Profile critical paths in the simulation
- Use appropriate data structures for the task at hand
- Consider parallelization for computationally intensive operations
- Be mindful of memory allocations in performance-critical code
- Consider using SIMD operations for vector math where appropriate

