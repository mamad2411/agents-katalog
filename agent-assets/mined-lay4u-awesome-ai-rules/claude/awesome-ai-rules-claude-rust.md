# Rust Project Rules

## Scope
- Applies to all Rust crates in this repository.
- Optimize for memory safety, predictable behavior, and reviewability.

## Ownership Discipline
- Design APIs around borrowing first, ownership transfer second.
- Keep references valid by constraining lifetimes to the smallest practical scope.
- Avoid clone-heavy code as a borrow-checker workaround.
- Refactor data flow before introducing `Rc`, `Arc`, or interior mutability.

## Error Model
- Return `Result<T, E>` for recoverable conditions.
- Library crates should define domain errors with `thiserror`.
- Binary entrypoints may use `anyhow::Result` for orchestration layers.
- Add `.context(...)` to I/O and external boundary failures.
- `unwrap()` is disallowed in production code.
- Prefer `?`; use `expect("specific invariant")` only with clear rationale.

## Pattern Matching
- All `match` blocks must be exhaustive.
- Do not hide enum evolution behind `_ =>` unless intentional and documented.
- Prefer explicit variant handling for domain logic.

## Unsafe Policy
- `unsafe` requires a written safety comment describing assumptions.
- Keep unsafe surface area minimal and encapsulated.
- Add focused tests proving the safe wrapper contract.

## Cargo and Layout
- Organize multi-package code as a Cargo workspace.
- Separate reusable core crates from adapters (web, CLI, persistence).
- Keep crate dependencies directional and acyclic.

## Linting and Formatting
- Format with `cargo fmt --all`.
- Enforce Clippy with `cargo clippy --all-targets --all-features -D warnings`.
- Do not silence lints without a justification comment.

## Tests and Documentation
- Run `cargo test --workspace` before completion.
- Unit tests live beside modules; integration tests live in `tests/`.
- Cover happy path, invalid input, and boundary failures.
- Public APIs require rustdoc with concise runnable examples.

## Completion Criteria
- Workspace builds and tests cleanly.
- No production `unwrap()` calls.
- Error handling, matching, and unsafe usage follow these rules.
