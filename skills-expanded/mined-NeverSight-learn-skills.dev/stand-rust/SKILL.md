---
name: stand-rust
description: >-
  Rust coding standards. Use when writing Rust code. Covers edition, error handling
  with thiserror/anyhow, unsafe policy, type patterns, testing, documentation, and
  dependency management.
---

# Rust Standards

Standards for Rust code.

## Edition

- Use the latest stable edition (2021+)
- Set `edition` explicitly in `Cargo.toml`

## Toolchain

- Follow the `lint` skill for formatting and linting — lintro runs `rustfmt`, `clippy`,
  `cargo_audit`, and `cargo_deny` as configured
- Treat clippy warnings as errors in CI (`-D warnings`)
- Customize formatting via `rustfmt.toml` where needed

## Error Handling

- Use `thiserror` for library error types — derive structured, typed errors
- Use `anyhow` for application-level error propagation
- No `.unwrap()` in library code — use `?` or return `Result`
- `.expect()` only with descriptive messages explaining the invariant:

  ```rust
  // Good
  let config = load_config().expect("config.toml must exist at startup");

  // Bad
  let config = load_config().unwrap();
  ```

- Implement `std::fmt::Display` for all custom error types
- Non-panicking `.unwrap_or_default()`/`.unwrap_or()` over trivial-arm matches:

  ```rust
  // Don't
  let count = match maybe_count {
      Some(n) => n,
      None => 0,
  };

  // Do
  let count = maybe_count.unwrap_or(0);
  ```

## Type Patterns

- Prefer newtypes for domain concepts — `struct UserId(u64)` over bare `u64`
- Use `impl Trait` in argument position for flexibility; explicit generics in return
  position for clarity
- Derive `Debug` on all public types
- Derive `Clone`, `PartialEq`, `Eq`, `Hash` where semantically appropriate
- Prefer `&str` over `String` in function arguments; return `String` when ownership
  transfers

## Unsafe

- `unsafe` blocks MUST include a `// SAFETY:` comment justifying soundness:

  ```rust
  // SAFETY: pointer is guaranteed non-null by the allocator contract,
  // and the lifetime is bounded by the enclosing scope.
  unsafe { ptr.as_ref() }
  ```

- Minimize unsafe surface area — encapsulate in safe abstractions
- Prefer safe alternatives (e.g., `std::sync::Mutex` over raw atomics) unless
  performance demands otherwise

## Documentation

- `///` doc comments on all public items (functions, types, traits, modules)
- Include code examples in doc comments for non-trivial APIs:

  ```rust
  /// Parse a duration string like "5s", "100ms", or "2m".
  ///
  /// # Examples
  ///
  /// ```
  /// use mycrate::parse_duration;
  ///
  /// let d = parse_duration("5s").unwrap();
  /// assert_eq!(d, std::time::Duration::from_secs(5));
  /// ```
  pub fn parse_duration(s: &str) -> Result<Duration> { ... }
  ```

- Use `#![deny(missing_docs)]` for library crates
- Module-level `//!` doc comments for crate and module overviews

## Testing

- Unit tests in `#[cfg(test)] mod tests` within the same file
- Integration tests in `tests/` directory
- Use `#[should_panic(expected = "...")]` for expected panics
- Consider `proptest` or `quickcheck` for property-based testing where valuable
- Use `assert_eq!` and `assert_ne!` over bare `assert!` for better error messages

```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn parse_duration_seconds() {
        let d = parse_duration("5s").unwrap();
        assert_eq!(d, Duration::from_secs(5));
    }

    #[test]
    #[should_panic(expected = "invalid format")]
    fn parse_duration_rejects_garbage() {
        parse_duration("not_a_duration").unwrap();
    }
}
```

## Dependencies

- Keep the dependency tree minimal — every dependency is an audit and supply chain
  surface
- Run vulnerability scanning via lintro (`uv run lintro chk` includes `cargo_audit`
  and `cargo_deny`)
- Pin versions in workspace `Cargo.toml` for multi-crate workspaces
- Prefer well-maintained crates with active maintainers and good documentation

## Patterns

- Prefer `impl` blocks over free functions for associated behavior
- Use the builder pattern for types with many optional fields
- Prefer iterators and combinators over manual loops where readability permits
- `let-else` over nested `if let` pyramids:

  ```rust
  // Don't
  if let Some(user) = lookup(id) {
      if let Some(email) = user.email {
          send(email);
      }
  }

  // Do
  let Some(user) = lookup(id) else { return };
  let Some(email) = user.email else { return };
  send(email);
  ```

- `.find()`/`.position()`/`.any()` over manual index loops:

  ```rust
  // Don't
  let mut idx = None;
  for (i, item) in items.iter().enumerate() {
      if item.id == target {
          idx = Some(i);
          break;
      }
  }

  // Do
  let idx = items.iter().position(|item| item.id == target);
  ```

- `matches!()` for pattern booleans:

  ```rust
  // Don't
  let is_ready = match state {
      State::Ready => true,
      _ => false,
  };

  // Do
  let is_ready = matches!(state, State::Ready);
  ```

- Use `#[must_use]` on functions whose return value should not be ignored
- Prefer `From`/`Into` implementations over ad-hoc conversion methods

## Linting

Follow the `lint` skill for linting and formatting workflow.
