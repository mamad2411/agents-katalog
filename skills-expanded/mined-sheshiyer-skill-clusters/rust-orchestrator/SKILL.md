---
name: rust-orchestrator
description: "Route a Rust task to the right skill — idiomatic patterns (ownership, errors, traits, concurrency, crate layout) versus testing (unit, integration, async, property-based, mocking, coverage, TDD). USE WHEN a user is writing, reviewing, refactoring, or testing Rust but hasn't named the specific concern."
cluster: rust
version: 1.0.0
---

# Rust Orchestrator

The single entry skill for Rust work. It locates the task on the **write ↔ verify** axis
and delegates to one of two specialist spokes. The cross-cutting model both spokes share —
the library-vs-application error strategy (`thiserror` vs `anyhow`), the type-driven design
stance, and the standard cargo toolchain — lives in `rust-core`; read it before choosing an
error type or shaping a public API.

## Cluster map (intent → spoke)

- **`rust-patterns`** — idiomatic production code. Ownership & borrowing, `Result`/`?` error
  propagation, enums + exhaustive matching, traits/generics, `Arc<Mutex<T>>` and async
  concurrency, builder/newtype patterns, and domain-organized crate/module layout.
- **`rust-testing`** — verification. TDD RED-GREEN-REFACTOR, `#[cfg(test)]` unit tests,
  `tests/` integration binaries, `#[tokio::test]` async tests, `rstest` parameterization,
  `proptest` property tests, `mockall` trait mocking, doc tests, Criterion benches, and
  `cargo-llvm-cov` coverage gates.
- **`rust-core`** *(shared reference)* — the error-strategy decision both spokes turn on, plus
  shared cargo conventions, the version/tooling matrix, and guardrails.

## Folded spokes

- **`rust-coding-skill`** — deep-dive authoring companion to `rust-patterns`. Goes
  finer-grained on **data modeling** (`struct`/`enum`/`newtype`, `&str` vs `String`,
  `Cow`/`Arc` ownership choices, modeling invariants with types like `NonZeroU32`),
  **impl-block organization** (placement, constructor/getter/mutation grouping, builders),
  **macros** (derive, focused declarative macros, proc-macro boundaries), and **build-speed
  tuning** (`mold` linker, `sccache`, `cargo check` iteration, workspace splitting,
  dev/release profiles). Route here when the ask is specifically about *how to shape the
  types/impls/macros* or *speed up compiles*; route to `rust-patterns` for broader idiomatic
  review (borrow-checker fights, concurrency, error propagation) and to `rust-core` for the
  error-strategy and toolchain model both share.

## Routing rules by intent

**Writing or shaping code → `rust-patterns`**
- "Is this idiomatic?" / code review → `rust-patterns`
- Ownership, lifetimes, `Cow`, "stop cloning to please the borrow checker" → `rust-patterns`
- Error design — `thiserror` for a library, `anyhow` for a binary → `rust-patterns` *(model in `rust-core`)*
- Modeling states as enums, newtypes, builders, trait objects vs generics → `rust-patterns`
- Concurrency — `Arc<Mutex<T>>`, channels, async/Tokio → `rust-patterns`
- Crate/module structure, `pub` surface, visibility → `rust-patterns`
- Detailed data modeling (`struct`/`enum`/`newtype`, ownership of each field), impl-block
  layout, writing macros, or **build-speed** tuning (`mold`, `sccache`, `cargo check`,
  workspaces) → `rust-coding-skill`

**Proving or measuring code → `rust-testing`**
- "Write tests for this" / add coverage → `rust-testing`
- TDD workflow / "test first" → `rust-testing`
- Async test, integration test, mock a dependency → `rust-testing`
- Property-based testing, fuzz-style invariants → `rust-testing`
- Benchmarks, coverage thresholds, CI test matrix → `rust-testing`

**Touches the boundary between both**
- Error *types* are designed in `rust-patterns` and *asserted* in `rust-testing`
  (`matches!(err, …)`, `Result`-returning tests) — keep the variant shape consistent via `rust-core`.

## Standard flow

1. Locate the task on the **write ↔ verify** axis: shaping/refactoring code → `rust-patterns`;
   proving/measuring it → `rust-testing`.
2. If it touches **error types, public API shape, or the cargo toolchain**, pull the model from
   `rust-core` first — the error strategy chosen in code dictates how tests assert on it.
3. Delegate to the spoke(s). A "build it the right way *with* tests" ask fans out in TDD order:
   `rust-testing` (write the failing test) → `rust-patterns` (implement idiomatically) →
   `rust-testing` (coverage gate).
4. Return: chosen spoke(s), the error strategy implied (lib `thiserror` vs app `anyhow`), and the
   next action.

## Guardrails

See `rust-core`. In short: **let the type system do the work** — `?` over `unwrap()` in
production, model illegal states as unrepresentable, keep `unsafe` minimal and documented with a
`# Safety` comment, and expose the narrowest `pub` surface. Pick `thiserror` for libraries and
`anyhow` for applications, and never silently widen that boundary. Tests follow TDD, stay
independent, never `sleep()`, and assert on typed error variants — not panic strings — wherever
the code returns a `Result`.

## Loading spokes on demand

To keep CLI startup context lean, this cluster's spokes are **not** separately registered as skills — only this orchestrator and its `*-core` are enumerated. When you route to a spoke named above, **load it on demand** by reading its file:

`~/.agents/skill-clusters/skills/<spoke-name>/SKILL.md`  (or `skills/<spoke-name>/SKILL.md` inside the skill-clusters repo).
