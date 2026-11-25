# Cursor Instructions for Exercism Rust

## Project Overview
This repository contains Rust solutions for Exercism exercises, emphasizing idiomatic Rust patterns and test-driven development.

## Development Workflow

1. **Exercise Implementation Process**
   - Navigate to exercise directory
   - Read README.md for requirements
   - Examine test file to understand expected behavior
   - Implement minimal solution in src/lib.rs
   - Enable all tests (remove #[ignore] attributes)
   - Iterate until all tests pass
   - Refactor for idiomatic Rust
   - Run cargo fmt and cargo clippy

2. **Code Generation Rules**
   - Always use iterator chains over manual loops
   - Prefer borrowing over cloning
   - Handle errors with Result<T, E> instead of panic!
   - Use pattern matching exhaustively
   - Implement standard traits (Debug, Clone, PartialEq)

3. **Testing Philosophy**
   - Write tests first (TDD approach)
   - Include edge cases
   - Test empty inputs, single elements, and boundaries
   - Use property-based testing where appropriate

## Rust Patterns and Anti-patterns

### Preferred Patterns
```rust
// Good: Iterator chain
let result: Vec<_> = items.iter()
    .filter(|x| x.is_valid())
    .map(|x| x.transform())
    .collect();

// Good: Pattern matching
match value {
    Some(x) if x > 0 => process(x),
    Some(_) => handle_negative(),
    None => handle_none(),
}

// Good: Error handling
pub fn parse(input: &str) -> Result<Value, ParseError> {
    // implementation
}