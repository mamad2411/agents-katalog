# Rust Skill

You are working on a Rust project. Apply these conventions.

## Ownership & Borrowing

- Prefer passing references (`&T` / `&mut T`) over moving values unless ownership transfer is intended.
- Use `Clone` explicitly when you do want a copy — the compiler will tell you when it's needed.
- Use `Cow<'_, str>` for functions that may return either borrowed or owned string data.
- Use `Arc<T>` for shared ownership across threads; `Rc<T>` for single-threaded shared ownership.

## Error Handling

- Use `Result<T, E>` for recoverable errors; use `?` to propagate errors up the call stack.
- Define domain-specific error types with `thiserror`:
  ```rust
  #[derive(Debug, thiserror::Error)]
  pub enum AppError {
      #[error("database error: {0}")]
      Database(#[from] sqlx::Error),
  }
  ```
- Use `anyhow::Result` in application code where detailed error types aren't needed.
- Never use `.unwrap()` in library or production code — use `.expect("descriptive message")` during prototyping only.

## Types & Traits

- Use `impl Trait` in function arguments for ergonomic generics: `fn process(items: impl Iterator<Item = u32>)`.
- Implement `Display` for user-facing types and `Debug` for all types (use `#[derive(Debug)]`).
- Use `From` / `Into` for cheap conversions; `TryFrom` / `TryInto` for fallible ones.
- Use `Default` trait and `#[derive(Default)]` where sensible.

## Async (Tokio)

- Use `tokio::main` macro for the async entry point.
- Use `tokio::spawn` for fire-and-forget tasks; collect handles to join or detect panics.
- Use `tokio::select!` for racing multiple async futures.
- Use `tokio::sync::Mutex` (async-aware) instead of `std::sync::Mutex` in async contexts.

## Performance

- Avoid unnecessary heap allocations in hot paths — consider `SmallVec` or stack arrays.
- Use iterators instead of manual loops — the optimizer handles them well.
- Profile with `cargo flamegraph` or `perf` before micro-optimizing.

## Clippy & Formatting

- Always run `cargo clippy --all-targets -- -D warnings` in CI.
- Always run `cargo fmt --check` in CI.
- Run `cargo test` with `RUST_BACKTRACE=1` to get full backtraces on failures.
