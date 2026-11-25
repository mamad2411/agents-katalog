---
name: rust-essentials
description: Use when writing any Rust — ownership, errors, Cargo, traits. The non-negotiables.
metadata:
  added: 2026-05-18
  last_reviewed: 2026-05-18
  type: language
  languages: [rust]
  status: active
  invokes_shell: false
  shell_reviewed: "valksor 2026-05-17"
  related: [rust-async-tokio, rust-axum-actix, rust-testing, rust-cli]
---

# Rust Essentials

**Iron Law: make invalid states unrepresentable. `Result` not `panic!`. `cargo clippy -- -D warnings` in CI. Set `edition = "2024"` for new crates (Rust 1.85+, default since Feb 2025) — affects `gen` keyword, `impl Trait` lifetime capture, and cargo fix behavior.**

**Versions:** Supported `1.85`+ (edition 2024 default) · Current `1.86`+ · No LTS series — _Async fn in traits stable (1.75); generic associated types stable; let-else (1.65+); `cargo` workspaces inherit `[workspace.package]` and `[workspace.dependencies]`. Pin MSRV in `Cargo.toml` `rust-version =`._

## Ownership & borrowing (the model you can't escape)

- One owner; many `&T` OR exactly one `&mut T` — never both.
- Borrow only as long as you need. Don't hold a `&mut` across an `await`, across a function call that might re-enter, or across user-controlled scope.
- `clone()` is fine when it's cheap, honest, and ends the borrow argument. It is NOT a fix for "the borrow checker yelled at me" — that means your data structure is wrong.

```rust
fn rename(user: &mut User, name: String) { user.name = name; } // &mut: I mutate
fn label(user: &User) -> String { user.name.clone() }          // &: I read
```

## Smart pointer choice

| Need                            | Use                                                |
| ------------------------------- | -------------------------------------------------- |
| Single owner, heap              | `Box<T>`                                           |
| Many readers, single thread     | `Rc<T>` (+ `RefCell<T>` for interior mut)          |
| Many readers, threads           | `Arc<T>` (+ `Mutex`/`RwLock` for mut)              |
| Maybe-owned (borrow or own)     | `Cow<'a, T>`                                       |
| Self-referential / trait object | `Box<dyn Trait>` or `Arc<dyn Trait + Send + Sync>` |

`Rc`/`Arc` cycles leak — use `Weak` for back-references.

## Common borrow-checker fixes

| Error                                      | Real fix                                                         |
| ------------------------------------------ | ---------------------------------------------------------------- |
| "cannot borrow as mutable" twice           | Shorten the first borrow; split into smaller scopes              |
| "borrowed value does not live long enough" | Return owned (`String`) not borrowed (`&str`), or add a lifetime |
| "cannot move out of borrowed content"      | `clone()` if cheap, `std::mem::take`, or restructure             |
| "lifetime parameters required"             | Add `<'a>`; if you can't, the API needs owned values             |

## Errors

Libraries: `thiserror` for typed errors. Apps: `anyhow` for context-rich `Result`.

```rust
// library
#[derive(thiserror::Error, Debug)]
pub enum Error {
    #[error("config missing key: {0}")]
    MissingKey(String),
    #[error(transparent)]
    Io(#[from] std::io::Error),
}

// application
fn load(path: &Path) -> anyhow::Result<Config> {
    let raw = std::fs::read_to_string(path)
        .with_context(|| format!("read {}", path.display()))?;
    toml::from_str(&raw).context("parse config")
}
```

| Situation                                    | Choice                               |
| -------------------------------------------- | ------------------------------------ |
| Public library API                           | `thiserror` enum — callers can match |
| Binary / app code                            | `anyhow::Result<T>` + `.context()`   |
| One-shot script                              | `anyhow::Result<T>`                  |
| Truly unrecoverable (corrupt invariant, OOM) | `panic!`/`expect("invariant: …")`    |
| User-input validation                        | `Result`, not panic                  |

`?` propagates. Use `From` impls (or `#[from]` on `thiserror`) so `?` Just Works across error boundaries.

## Cargo

```
yourapp/
├── Cargo.toml
├── Cargo.lock     # COMMIT for binaries; libraries: commit too (Rust 1.65+ stance)
├── src/
│   ├── main.rs    # binary entry
│   └── lib.rs     # library root — keep `main.rs` thin, logic in lib
└── tests/         # integration tests
```

Workspaces for multi-crate repos:

```toml
[workspace]
resolver = "2"
members = ["crates/*"]

[workspace.dependencies]
serde = { version = "1", features = ["derive"] }
```

Features are **additive only**. Never use a feature to remove behavior — split crates instead. Default features should be the common case; document non-default features.

Profiles: tune `[profile.release]` (`lto = "thin"`, `codegen-units = 1`) only after profiling proves the wins.

## Traits

Keep traits small and composable. One verb, one purpose. Compose with bounds (`T: Read + Seek`).

```rust
pub trait Store {
    type Error;
    fn put(&self, key: &str, val: &[u8]) -> Result<(), Self::Error>;
    fn get(&self, key: &str) -> Result<Option<Vec<u8>>, Self::Error>;
}
```

- Marker traits (`Send`, `Sync`, `Copy`) carry guarantees, no methods. Don't impl `Copy` for types containing heap data.
- **Orphan rule**: you can impl `Trait` for `Type` only if you own one of them. Wrap foreign types in a newtype to escape.
- `impl Trait` in arg position = generic. In return position = single concrete hidden type.
- `dyn Trait` for runtime polymorphism; pays vtable cost. Use when callers vary at runtime; otherwise prefer generics.

## Anti-patterns

- `.unwrap()` / `.expect("")` in production paths — every one is a future panic. `expect` with an invariant message is acceptable on truly impossible branches.
- `Result<(), Box<dyn Error>>` in library APIs — opaque to callers. Use `thiserror`.
- `unsafe` without a `// SAFETY:` block documenting the invariants the caller must uphold.
- `panic!` for error paths the caller could reasonably handle.
- Manual `init()`-style "two-phase construction" — make the constructor return a fully-valid value or a `Result`.
- `clone()` to silence the borrow checker without thinking about whether the design is wrong.
- `String` parameters when `&str` works; `Vec<T>` parameters when `&[T]` works.
- Re-exporting `pub use foo::*;` in lib roots — name your API explicitly.
- Skipping `cargo fmt` and `cargo clippy` locally; CI catches it but reviewers shouldn't.

## Red flags

| Thought                                | Reality                                                                          |
| -------------------------------------- | -------------------------------------------------------------------------------- |
| "I'll wrap it in `Arc<Mutex<…>>`"      | Often the data should be owned by one task and others should send messages.      |
| "Lifetimes are too hard"               | Your function signature is leaking implementation. Return owned, or restructure. |
| "I need `unsafe` for performance"      | Profile first. 99% of the time safe code with the right data structure wins.     |
| "Just one global with `lazy_static`"   | Pass it explicitly or use `OnceLock`/`OnceCell` with a defined init point.       |
| "I'll use `Box<dyn Error>` everywhere" | Callers can't do anything with it. Type your errors.                             |

## Hand-off

For async, Tokio, cancellation: `Skill(rust-async-tokio)`. For HTTP servers with axum: `Skill(rust-axum-actix)`. For tests, doc-tests, property tests, fuzzing: `Skill(rust-testing)`.
