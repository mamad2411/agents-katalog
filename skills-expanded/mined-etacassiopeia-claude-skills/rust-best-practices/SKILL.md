---
name: rust-best-practices
description: >
  Comprehensive Rust coding standards, idioms, and anti-pattern prevention for
  production Rust projects. Use this skill whenever writing, reviewing, or
  refactoring any Rust code — including new modules, async code, error handling,
  ownership patterns, trait design, concurrency, performance-sensitive code, FFI,
  and CLI tooling. Trigger on any .rs file work, Cargo.toml changes, or questions
  about how to structure Rust code correctly. Always consult this skill before
  generating non-trivial Rust — it encodes decisions that are easy to get wrong
  and hard to refactor later.
---

# Rust Best Practices Skill

This skill encodes production-grade Rust idioms and the most common anti-patterns
to avoid. It is organized by domain. Read the top-level sections that apply to
your current task; load reference files for deeper guidance on specific topics.

## Reference Files (load when relevant)

- `references/ownership-and-borrowing.md` — Lifetime annotations, NLL, self-referential types, `Pin`
- `references/error-handling.md` — `thiserror`, `anyhow`, error propagation patterns
- `references/async.md` — Tokio patterns, `async_trait`, cancellation, blocking work
- `references/traits-and-generics.md` — Trait design, HRTBs, blanket impls, object safety
- `references/concurrency.md` — `Arc`/`Mutex` vs channels vs atomics, `Send`/`Sync`
- `references/performance.md` — Allocation, cache, SIMD, profiling hooks
- `references/testing.md` — Unit, integration, property-based, snapshot testing

---

## 1. Project & Module Structure

**DO:**
- One concern per module; keep `lib.rs` and `main.rs` thin (re-exports + wiring only)
- Put public API surface in `src/lib.rs`; binary logic in `src/bin/` or `src/main.rs`
- Use `pub(crate)` liberally — default to minimum visibility
- Feature-gate optional dependencies with Cargo features

**DON'T:**
- Dump everything in `main.rs` or one giant `lib.rs`
- Use `pub use *` glob re-exports in internal modules (breaks `rustdoc` and discoverability)
- Reach for `mod.rs` files; prefer `module_name.rs` with inline submodule declarations (Rust 2018+)

```rust
// ANTI-PATTERN: flat everything
mod lib {
    pub fn a() {}
    pub fn b() {}
    // ...100 more items
}

// GOOD: domain modules
mod auth;
mod storage;
mod api;
pub use api::Router;
```

---

## 2. Ownership & Memory

**DO:**
- Prefer borrowing (`&T`, `&mut T`) over cloning; clone only at API boundaries
- Use `Cow<'_, str>` when a function sometimes needs ownership, sometimes doesn't
- Use `Box<T>` for heap allocation of single values; `Vec<T>` for sequences
- Use `Arc<T>` only when shared ownership across threads is genuinely needed
- Prefer `&str` over `String` in function parameters; `&[T]` over `&Vec<T>`

**DON'T:**
- `.clone()` to silence borrow checker errors without understanding the root cause
- Return `&String` or `&Vec<T>` — return `&str` and `&[T]` instead
- Use `Rc<RefCell<T>>` in async code (not `Send`); use `Arc<Mutex<T>>` or channels

```rust
// ANTI-PATTERN
fn greet(name: &String) -> String { format!("Hello, {name}") }

// GOOD
fn greet(name: &str) -> String { format!("Hello, {name}") }

// ANTI-PATTERN: clone to avoid thinking
let result = expensive_map.clone().into_iter().find(|..| ..);

// GOOD: borrow and collect only what's needed
let result = expensive_map.iter().find(|..| ..).map(|(k, v)| v.clone());
```

---

## 3. Error Handling

**DO:**
- Use `thiserror` for library errors (derive `Error`, keep variants meaningful)
- Use `anyhow` for application/binary errors (rich context with `.context()`)
- Use `?` for propagation; never `.unwrap()` in library code
- Return `Result<(), MyError>` from `main()` or use `anyhow::Result`
- Add context to errors at each layer: `op().context("while loading config")?`

**DON'T:**
- `.unwrap()` or `.expect()` in production paths (document why it's safe if you must)
- Use `Box<dyn Error>` as a library error type (loses type info for callers)
- Create one monolithic error enum for an entire crate; scope errors to modules
- Silence a `Result` on a data path with `.ok()` / `unwrap_or_else(|_| default)` /
  `unwrap_or_default()` — the **swallow pattern**. Failure degrades into wrong-but-quiet
  behavior that surfaces far from the cause (e.g. a serde failure served as `200 OK {}`; a
  config block silently dropped; a security gate failing open). Only two silencing shapes are
  legitimate, and each deserves a comment naming it:
  1. **Domain-optional parse** — the input may genuinely not be that type; absence is a domain
     value ("is this body JSON?").
  2. **Terminal last-resort** — the final fallback of an error path, valid only if the fallback
     payload is infallible by construction AND keeps a correct status/severity
     (`Response::new(..)` defaults to `200` — a 200 "error" fallback is a bug).
  Everything else: propagate, map to a correct error response, or log at error level.
  Security classifiers **fail closed** — unparseable input classifies as the dangerous class.

```rust
// ANTI-PATTERN (swallow): parse failure silently drops the whole block, serves 200
let parsed = serde_json::from_value::<Behaviors>(v).ok();          // gone, no log

// GOOD: loud degradation — the failure is visible and correctly classified
let parsed = match serde_json::from_value::<Behaviors>(v) {
    Ok(b) => Some(b),
    Err(e) => {
        tracing::error!(error = %e, "malformed _behaviors block dropped");
        None
    }
};

// ANTI-PATTERN: library with Box<dyn Error>
pub fn load(path: &str) -> Result<Config, Box<dyn Error>> { .. }

// GOOD: typed errors for libraries
#[derive(Debug, thiserror::Error)]
pub enum ConfigError {
    #[error("file not found: {path}")]
    NotFound { path: PathBuf },
    #[error("parse failed: {0}")]
    Parse(#[from] serde_json::Error),
}
pub fn load(path: &str) -> Result<Config, ConfigError> { .. }

// GOOD: anyhow for binaries
fn main() -> anyhow::Result<()> {
    let cfg = load("config.json").context("loading startup config")?;
    Ok(())
}
```

---

## 4. Traits & Generics

**DO:**
- Prefer generics over `dyn Trait` for zero-cost abstraction in hot paths
- Use `dyn Trait` for heterogeneous collections and when erasing type at API boundary
- Implement standard traits when semantically correct: `Display`, `From`, `Into`,
  `FromStr`, `Default`, `Clone`, `Debug`, `PartialEq`, `Hash`
- Use associated types when there's a single natural output type; type params when
  callers need to select among multiple implementations
- Make traits object-safe by design; avoid `Self: Sized` bounds unless necessary

**DON'T:**
- Implement `Display` for types that should use `Debug` (or vice versa)
- Use `impl Trait` in return position in trait methods (not object-safe)
- Overuse blanket impls — they cause coherence issues and confusing errors

```rust
// ANTI-PATTERN: overly broad generic where dyn is clearer
fn run_all<T: Task>(tasks: &[T]) { .. }  // all tasks must be same type!

// GOOD
fn run_all(tasks: &[Box<dyn Task>]) { .. }

// ANTI-PATTERN: manual From impls for error variants
impl From<io::Error> for MyError {
    fn from(e: io::Error) -> Self { MyError::Io(e) }
}

// GOOD: use #[from] with thiserror
#[derive(thiserror::Error, Debug)]
enum MyError {
    #[error(transparent)]
    Io(#[from] io::Error),
}
```

---

## 5. Async & Tokio

**DO:**
- Use `tokio::spawn` for CPU-independent concurrent tasks
- Use `tokio::task::spawn_blocking` for blocking/CPU-bound work inside async context
- Cancel tasks explicitly via `JoinHandle::abort()` or cancellation tokens (`tokio_util::CancellationToken`)
- Use `tokio::select!` for racing futures; handle all branches
- Use `#[async_trait]` (from `async-trait` crate) for async trait methods until RPITIT stabilizes

**DON'T:**
- Block inside async functions: no `std::thread::sleep`, `std::fs::read`, heavy compute
- Hold `MutexGuard` across `.await` — use `tokio::sync::Mutex` or drop before awaiting
- Ignore `JoinHandle` return values (panics are silently swallowed)
- Use `async fn` in traits without `#[async_trait]` in stable Rust

```rust
// ANTI-PATTERN: blocking inside async
async fn fetch_and_process(url: &str) -> Result<Data> {
    let body = reqwest::get(url).await?.text().await?;
    let parsed = heavy_parse(&body); // blocks the executor thread!
    Ok(parsed)
}

// GOOD
async fn fetch_and_process(url: &str) -> Result<Data> {
    let body = reqwest::get(url).await?.text().await?;
    let parsed = tokio::task::spawn_blocking(move || heavy_parse(&body)).await??;
    Ok(parsed)
}

// ANTI-PATTERN: holding std::sync::MutexGuard across .await
async fn update(state: Arc<std::sync::Mutex<State>>) {
    let mut guard = state.lock().unwrap();
    some_async_op().await; // DEADLOCK RISK
    guard.value = 42;
}

// GOOD: use tokio::sync::Mutex OR drop before await
async fn update(state: Arc<tokio::sync::Mutex<State>>) {
    let mut guard = state.lock().await;
    guard.value = 42;
    // guard dropped before any await
}
```

---

## 6. Concurrency

**DO:**
- Default to message passing (`mpsc`, `oneshot`, `broadcast` from `tokio::sync`)
- Use `Arc<RwLock<T>>` when reads dominate writes; `Arc<Mutex<T>>` for balanced access
- Use atomics (`AtomicU64`, `AtomicBool`) for single-value counters/flags; avoids lock overhead
- Use `DashMap` for concurrent hashmaps (shard-locked, significantly faster than `Mutex<HashMap>`)
- Document the locking order whenever multiple locks are taken together

**DON'T:**
- Use `Mutex` for read-heavy data (prefer `RwLock`)
- Take multiple locks without a consistent ordering (deadlock)
- Use `std::sync::Mutex` in async code (blocks the executor thread under contention)

```rust
// ANTI-PATTERN: Mutex for a counter
let counter = Arc::new(Mutex::new(0u64));
// ...
*counter.lock().unwrap() += 1;

// GOOD: atomic for simple counters
let counter = Arc::new(AtomicU64::new(0));
counter.fetch_add(1, Ordering::Relaxed);
```

---

## 7. Iterators & Collections

**DO:**
- Chain iterator adapters rather than imperative loops: `filter`, `map`, `flat_map`,
  `fold`, `any`, `all`, `collect`
- Use `Entry` API to avoid double-lookups: `map.entry(key).or_insert_with(|| ..)`
- Pre-allocate `Vec` and `HashMap` with `with_capacity` when size is known
- Prefer `BTreeMap` over `HashMap` when ordered iteration matters

**DON'T:**
- `.collect()` into a `Vec` only to immediately iterate again — chain instead
- Index into `Vec` with `[]` in non-trivial code; prefer `.get(i)` and handle `None`
- Use `HashMap::insert` in a loop without checking if key already exists

```rust
// ANTI-PATTERN: collect-then-iterate
let names: Vec<_> = users.iter().map(|u| &u.name).collect();
let result: Vec<_> = names.iter().filter(|n| n.starts_with('A')).collect();

// GOOD: single chain
let result: Vec<_> = users.iter()
    .map(|u| &u.name)
    .filter(|n| n.starts_with('A'))
    .collect();

// ANTI-PATTERN: double lookup
if !map.contains_key(&key) {
    map.insert(key, compute_value());
}

// GOOD: entry API
map.entry(key).or_insert_with(compute_value);
```

---

## 8. Deriving & Macros

**DO:**
- Derive `Debug` on almost everything; it costs nothing and is essential for debugging
- Derive `Clone` only when cloning is semantically meaningful for the type
- Use `#[non_exhaustive]` on public enums and structs to allow future additions
- Use `serde` `rename_all`, `skip_serializing_if`, `default` attributes instead of manual impls

**DON'T:**
- Derive `Copy` on types that may grow heap allocation later
- Derive `PartialEq`/`Hash` on types with floating-point fields without care
- Use `Default` derive when a meaningful default doesn't exist — implement it explicitly
  or don't implement it at all

```rust
// GOOD: serde attributes over manual impl
#[derive(Debug, Clone, serde::Serialize, serde::Deserialize)]
#[serde(rename_all = "camelCase")]
pub struct ApiResponse {
    pub user_id: u64,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub display_name: Option<String>,
}
```

---

## 9. Performance Hygiene

**DO:**
- Profile before optimizing: use `cargo flamegraph`, `criterion`, or `perf`
- Understand monomorphization cost: heavy generic code bloats binary; use `dyn` at boundaries
- Avoid `String::new()` + repeated `push_str`; use `format!` or a `String` with `with_capacity`
- Use `#[inline]` on small, hot functions that cross module boundaries

**DON'T:**
- Premature optimization: idiomatic Rust is already fast
- Use `unsafe` for performance without benchmarking the safe alternative first
- Clone large data structures to avoid lifetime annotations

---

## 10. `unsafe` Code

**DO:**
- Isolate `unsafe` in the smallest possible scope
- Write a `// SAFETY:` comment explaining every invariant the caller must uphold
- Use `#[deny(unsafe_code)]` at the crate root and lift it only for specific modules
- Wrap `unsafe` blocks in safe abstractions; never expose raw pointers in public API

**DON'T:**
- Use `unsafe` because the borrow checker is annoying — understand why it's complaining
- Transmute between types without static size/alignment checks
- Use `ptr::read`/`ptr::write` without `MaybeUninit` discipline

```rust
// GOOD: documented unsafe with smallest scope
fn split_at_mid(slice: &[u8], mid: usize) -> (&[u8], &[u8]) {
    assert!(mid <= slice.len());
    // SAFETY: mid is checked to be <= slice.len() above,
    // so both pointers are within the allocation and non-overlapping.
    unsafe {
        (
            std::slice::from_raw_parts(slice.as_ptr(), mid),
            std::slice::from_raw_parts(slice.as_ptr().add(mid), slice.len() - mid),
        )
    }
}
```

---

## 11. Testing

**DO:**
- Put unit tests in `#[cfg(test)]` modules at the bottom of each source file
- Put integration tests in `tests/` (they test the public API as an external crate would)
- Use `proptest` or `quickcheck` for property-based tests on pure functions
- Use `insta` for snapshot testing of complex output (JSON, rendered strings)
- Test error paths explicitly; don't only test the happy path

**DON'T:**
- Test implementation details — test observable behavior
- Use `unwrap()` in test helpers without a message; use `expect("context")`
- Share mutable global state across tests (causes flaky parallel tests)

---

## 12. Clippy & Formatting

**Enforce in CI:**
```toml
# .cargo/config.toml
[build]
rustflags = ["-D", "warnings"]
```

**Recommended clippy lints to enable:**
```rust
#![warn(
    clippy::all,
    clippy::pedantic,
    clippy::nursery,
    clippy::unwrap_used,       // force explicit error handling
    clippy::expect_used,       // same
    clippy::panic,             // no panics in lib code
    clippy::indexing_slicing,  // prefer .get()
)]
#![allow(
    clippy::module_name_repetitions, // often unavoidable
    clippy::must_use_candidate,      // too noisy for rapid dev
)]
```

**Always run:**
```bash
cargo fmt --all
cargo clippy --all-targets --all-features -- -D warnings
cargo test --all-features
```

---

## Quick Reference: Type Choices

| Situation | Use |
|-----------|-----|
| Shared ownership, single thread | `Rc<T>` |
| Shared ownership, multi-thread | `Arc<T>` |
| Interior mutability, single thread | `RefCell<T>` |
| Interior mutability, multi-thread | `Mutex<T>` / `RwLock<T>` |
| Concurrent counter/flag | `AtomicU64` / `AtomicBool` |
| Concurrent hashmap | `DashMap<K, V>` |
| Maybe-owned string | `Cow<'_, str>` |
| Heap-allocated, immutable string | `Box<str>` |
| Error in library | `thiserror` enum |
| Error in binary | `anyhow::Error` |
| Async runtime | `tokio` |
| Blocking work in async | `spawn_blocking` |
