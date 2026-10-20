# Codex Rust Rules

## Role
- You are an AI coding agent producing production Rust.
- Optimize for safety, correctness, and long-term maintainability.

## Ownership and API Design
- Choose ownership semantics deliberately in every function signature.
- Prefer borrowing (`&T`, `&mut T`) over taking ownership by default.
- Keep lifetime scopes tight and explicit when readability benefits.
- Remove clone-based workarounds by restructuring control flow.

## Error Handling Contract
- Represent fallible work with `Result<T, E>`.
- Library/internal crates: model typed errors using `thiserror`.
- Application/CLI boundaries: use `anyhow` for error aggregation with context.
- Add meaningful context on external boundary failures.
- `unwrap()` is forbidden in production code.
- Use `?` for propagation and `expect("invariant")` only when justified.

## Pattern Matching Rules
- `match` statements must remain exhaustive.
- Avoid wildcard arms for domain enums unless explicitly documented.
- Favor enum-driven state modeling over ad hoc booleans.

## Workspace, Formatting, Linting
- Maintain clear Cargo workspace boundaries across crates.
- Keep domain logic independent from adapters and transport layers.
- Run `cargo fmt --all`.
- Run `cargo clippy --all-targets --all-features -D warnings`.
- Address lints directly instead of suppressing by default.

## Unsafe Usage
- Do not introduce `unsafe` unless no safe alternative exists.
- Place unsafe code in minimal, isolated sections.
- Document safety invariants with comments above each unsafe block.
- Add tests that exercise invariant boundaries.

## Testing and Documentation
- Run `cargo test --workspace` for changed behavior.
- Unit tests live near modules; integration tests live in `tests/`.
- Cover success, failure, and edge conditions.
- Add rustdoc for public APIs and include practical examples.
- Keep examples synchronized with implementation changes.

## Style
- Prefer iterators/combinators over manual loops when equivalent.
- Keep side effects at boundaries and core logic pure where possible.
- Preserve clear, explicit names for types and functions.
