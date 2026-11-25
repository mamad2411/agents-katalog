---
name: exec-rust
description: Rust execution idioms to embed into Codex prompts when the target project is Rust — ownership discipline, error handling with Result, and idiomatic API design.
---

# Rust Idioms (embed when project is Rust)

```
Rust standards:
- Errors: return Result<T, E> for fallible functions; no unwrap()/expect()/panic! in library code
  (reserve panic for truly unrecoverable invariants). Propagate with ?; model domain errors with
  an enum (thiserror if present), wrap sources with context (anyhow only at bin/top level).
- Ownership: borrow (&T/&mut T) over cloning; clone only when a clear owner is needed. No needless
  .to_owned()/.clone() to appease the borrow checker — restructure instead.
- Prefer iterators/combinators (map/filter/collect) over index loops; use ? and Option combinators
  (map/and_then/ok_or) instead of manual match when clearer.
- Types: newtypes over primitive obsession; derive(Debug, Clone, PartialEq) where sensible; make
  illegal states unrepresentable with enums. Accept impl Trait / generics, expose concrete types.
- Concurrency: prefer message passing or the project's async runtime (tokio/async-std) consistently;
  Send/Sync only where needed; no blocking calls inside async without spawn_blocking.
- No unsafe unless unavoidable — if used, isolate it, document the invariant it upholds, and justify.
- Follow rustfmt (non-negotiable) and clippy if configured; match the repo's module layout.
- Tests: #[cfg(test)] mod tests with #[test]; table cases via loops or rstest if present; assert
  behavior, not internals; use the repo's assertion style.
```
