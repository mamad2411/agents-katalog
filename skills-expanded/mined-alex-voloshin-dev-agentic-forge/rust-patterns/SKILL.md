---
name: rust-patterns
description: Rust stack conventions agentic-forge applies when the detected stack is Rust — the toolchain (cargo test / clippy -D warnings / cargo fmt / cargo check), ownership and error-handling idioms, testing discipline, layout, and the high-value Rust pitfalls. Loaded on demand by develop / code-review and the software-engineer / qa-engineer roles after stack detection; kept off the always-on listing.
disable-model-invocation: true
---

# Rust patterns

The Rust stack pack: loaded by the `software-engineer` / `qa-engineer` roles (and the
`code-review` lint aspect) when `stacks.detect` reports Rust. It carries only what is
**Rust-specific** on top of [`engineering-standards`](../engineering-standards/SKILL.md) —
Claude already knows general Rust; this encodes the conventions and gates agentic-forge holds
Rust work to. (Mechanism: ADR 0015, by-stack detection + reference packs.)

## Toolchain

**Prefer the repo's own commands** — read the `Makefile` / `justfile` / CI workflow and run
*those*; Cargo is otherwise standard. Defaults:

| Job | Conventional command | Gate |
| --- | --- | --- |
| test | `cargo test` (or `cargo nextest run`) | green; new behaviour + doc-tests covered |
| build/types | `cargo check` (fast) / `cargo build` | compiles clean |
| lint | `cargo clippy --all-targets -- -D warnings` | clean (no new `#[allow]`) |
| format | `cargo fmt` | applied (rustfmt is canonical) |

Run `cargo clippy --all-targets -- -D warnings` and `cargo fmt` on the change before declaring
done; keep `Cargo.toml`/`Cargo.lock` consistent. Never silence a lint to pass — fix the cause.

## Idioms

- **Let the borrow checker guide design**: borrow over clone; take `&str`/`&[T]` not
  `&String`/`&Vec<T>`; reach for `.clone()` deliberately, not to dodge a borrow error.
- **Errors are `Result<T, E>` + `?`.** Library errors via `thiserror`; application errors via
  `anyhow` (or `Box<dyn Error>`). Avoid `unwrap()`/`expect()` outside tests and documented
  invariants. Use `Option` over sentinels; combinators (`map`/`and_then`/`ok_or`).
- **Make illegal states unrepresentable**: enums + exhaustive `match`, newtypes, typestate.
  Derive `Debug`/`Clone`/`PartialEq`/`Default`; `From`/`Into` for conversions.
- Iterators over manual index loops (zero-cost). Concurrency is "fearless" — the compiler
  enforces `Send`/`Sync`; `Arc<Mutex<T>>` for shared state; in async, don't block the runtime.

## Testing

- Unit tests in `#[cfg(test)] mod tests`, integration tests in `tests/`, **doc-tests** in `///`
  examples (they run). Use `assert_eq!`, `#[should_panic]`, and a case table (array or `rstest`).
- Cover the happy path plus a boundary and an **`Err`** case. Tests must be deterministic — no
  real network/clock. Never weaken, skip, or delete a test to go green.

## Pitfalls (Rust-specific, high-value)

- **`unwrap()`/`expect()` panicking** in library/prod paths; use `?` + real error types.
- **`.clone()` overuse** to silence the borrow checker (usually a design smell).
- **`unsafe` without a documented invariant**; needless `unsafe`.
- **Blocking in async** (sync blocking calls on the runtime); **holding a lock across `.await`**
  (contention/deadlock).
- **Integer overflow** — panics when `overflow-checks` is on (the debug/test default), wraps in
  release by default; use `checked_*`/`saturating_*`/`wrapping_*`. **`Rc`/`RefCell` reference
  cycles** leak (break them with `Weak`).

## Definition of done (Rust)

`cargo check`/`cargo build` clean, `cargo clippy --all-targets -- -D warnings` clean, `cargo fmt` applied,
`cargo test` green with the new boundary/`Err` cases (and doc-tests), no new
`unwrap`/`expect`/`unsafe` in non-test code without a documented reason, public API documented —
using the repo's own commands where declared.
