---
name: rust-implementation
description: "Implement Rust changes to ownership, public APIs, errors, async, unsafe code, or persistence."
---

# Rust Implementation

Prefer correct, readable Rust first; optimize only where measurements or requirements justify complexity.

## Trigger boundary

Use this skill when a Rust change alters ownership or lifetimes, public APIs, error propagation, async/concurrency, unsafe code, persistence/serialization, tracing, or measured performance behavior.

Do not load it for a small local rename, comment, formatting change, or mechanical edit that does not change those boundaries; follow the repository's established convention directly.

## Coordination

Use this skill together with `itsol-task-intake` for ambiguous work, `itsol-self-review` before handoff, and focused `security-*` or `infra-*` skills when the change touches trust boundaries or deployment behavior.

## Focused References

- [01-overview.md](./references/01-overview.md) - Overview; Cel dokumentu; Zasady ogólne; Ownership i borrowing
- [02-obsluga-bledow.md](./references/02-obsluga-bledow.md) - Obsługa błędów; Paniki i unsafe; SQLx i baza danych; Serde, JSON i DTO
- [Shared Rust tooling and boundary guidance](../_shared/references/rust/tooling-clippy-rustfmt-lints.md) - wspólne fakty dla implementacji: Clippy, rustfmt, lints, config, HTTP, jobs, macros i CI
