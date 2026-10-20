# Gemini CLI Rust Rules

## Role
- You are a CLI coding agent operating in Rust repositories.
- Produce robust code with clear failure behavior and strong safety defaults.

## Ownership and Borrowing
- Prefer borrowed inputs in helper APIs unless ownership is required.
- Keep mutable borrows narrow and avoid hidden aliasing.
- Introduce explicit lifetimes when they make contracts obvious.
- Refactor before adding clone-heavy patterns.

## Error Handling
- Model recoverable failures as `Result<T, E>`.
- Use `thiserror` in shared libraries for structured error types.
- Use `anyhow` in command runners and top-level orchestration.
- Attach context to filesystem, process, parse, and network errors.
- Never ship `unwrap()` in production paths.
- Use `?` for propagation; `expect()` must include actionable context.

## Pattern Matching
- Keep enum matching exhaustive.
- Avoid wildcard branches that hide new variant handling.
- Prefer explicit state enums over fragile string comparisons.

## Workspace and Tooling
- Use Cargo workspace conventions for multi-crate projects.
- Keep crates cohesive: core logic, adapters, CLI entrypoints.
- Format with `cargo fmt --all`.
- Lint with `cargo clippy --all-targets --all-features -D warnings`.
- Treat lint violations as blockers, not suggestions.

## Unsafe Guardrails
- Only use `unsafe` for proven performance or FFI constraints.
- Wrap unsafe internals with safe external APIs.
- Record required invariants in safety comments.
- Add tests that validate invariant enforcement.

## Testing and Docs
- Validate changes using `cargo test --workspace`.
- Store integration tests in `tests/` directories.
- Keep unit tests near module code.
- Document public APIs with rustdoc and concise examples.
- Ensure examples remain compilable and realistic.

## Coding Style
- Prefer iterator adapters over manual index loops.
- Keep functions narrow, explicit, and easy to test.
- Avoid mixing boundary side effects into core domain logic.
