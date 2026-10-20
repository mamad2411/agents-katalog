---
name: rust-programming
description: Use when writing, reviewing, or refactoring Rust code, especially workspace crates, public APIs, error handling, async code, ownership choices, or performance-sensitive paths.
license: MIT
tags: [development, rust-programming, writing, performance, rust]
metadata:
  source_references:
    - https://github.com/udapy/rust-agentic-skills
    - https://rust-lang.github.io/api-guidelines/
    - https://doc.rust-lang.org/book/
    - https://doc.rust-lang.org/clippy/
---

# Rust Programming

Use this skill to keep Rust changes idiomatic, maintainable, and easy to verify.

## Operating Rules

1. Read the surrounding module before changing ownership, trait bounds, public types, or async flow.
2. Prefer the repository's existing crate boundaries and error types over introducing a new abstraction.
3. Make invalid states unrepresentable with focused types, enums, and constructors where the domain has real invariants.
4. Return `Result` for recoverable failures and reserve `panic!`, `unwrap`, and `expect` for tests, impossible states with a clear message, or process-fatal startup validation.
5. Keep allocations and clones intentional. Borrow first, clone at ownership boundaries, and document non-obvious lifetime or allocation tradeoffs.
6. Favor explicit control flow over clever chains when error handling, locking, cancellation, or state mutation is involved.
7. Keep public APIs small, named consistently, and documented enough that callers know ownership, errors, and side effects.
8. Run `cargo fmt`, focused `cargo test`, and `cargo clippy --workspace --all-targets` when the change warrants it.

## Design Checks

- **Types**: Does the type express the domain, or is it a bag of loosely related fields?
- **Ownership**: Can the caller pass a reference? If ownership is needed, is the transfer visible in the API?
- **Errors**: Is each error actionable at the layer that receives it?
- **Concurrency**: Are locks held for the shortest practical scope, and never across awaits unless deliberately required?
- **Traits**: Are trait bounds on the function that needs them instead of leaking through larger structs?
- **Testing**: Do tests cover behavior and edge cases, not only compilation or snapshots?

## Best Practice Patterns

### Accept Borrowed Inputs

```rust
// Avoid: forces callers to allocate or give up ownership.
fn load_config(path: PathBuf) -> Result<Config, ConfigError> {
    std::fs::read_to_string(path)?.parse()
}

// Prefer: accepts Path, PathBuf, and path-like wrappers.
fn load_config(path: impl AsRef<std::path::Path>) -> Result<Config, ConfigError> {
    std::fs::read_to_string(path)?.parse()
}
```

### Keep Error Types Actionable

```rust
#[derive(Debug, thiserror::Error)]
pub enum ImportError {
    #[error("failed to read import file {path}")]
    Read {
        path: std::path::PathBuf,
        #[source]
        source: std::io::Error,
    },

    #[error("invalid import payload")]
    InvalidPayload(#[from] serde_json::Error),
}
```

Use typed variants when callers can recover differently. Use context-rich messages at process or UI boundaries where diagnosis matters more than matching.

### Make Invalid States Unrepresentable

```rust
pub struct NonEmptyName(String);

impl NonEmptyName {
    pub fn parse(value: String) -> Result<Self, NameError> {
        if value.trim().is_empty() {
            return Err(NameError::Empty);
        }
        Ok(Self(value))
    }

    pub fn as_str(&self) -> &str {
        &self.0
    }
}
```

Do validation once at construction instead of repeatedly checking raw strings throughout the codebase.

### Do Not Hold Locks Across Awaits

```rust
// Avoid: the lock stays held while the async write waits.
async fn save_bad(state: &tokio::sync::Mutex<State>, store: &Store) -> anyhow::Result<()> {
    let guard = state.lock().await;
    store.write(&guard.snapshot()).await
}

// Prefer: copy the data needed, then release the lock before await.
async fn save_good(state: &tokio::sync::Mutex<State>, store: &Store) -> anyhow::Result<()> {
    let snapshot = {
        let guard = state.lock().await;
        guard.snapshot()
    };

    store.write(&snapshot).await
}
```

### Clone At Ownership Boundaries

```rust
let workspace_id = workspace.id.clone();

tokio::spawn(async move {
    refresh_workspace(workspace_id).await
});
```

Cloning for a spawned task, channel message, cache entry, or stored value is often correct. Cloning to satisfy the borrow checker inside one synchronous function is a signal to shorten borrows first.

### Test Behavior, Not Implementation Shape

```rust
#[test]
fn rejects_empty_workspace_name() {
    let err = NonEmptyName::parse("  ".to_string()).unwrap_err();

    assert!(matches!(err, NameError::Empty));
}
```

Prefer tests that pin public behavior, error variants, state transitions, and regression cases.

## References

Read `references/idiomatic-rust.md` for concrete patterns and review heuristics.
