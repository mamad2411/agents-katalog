---
name: systems-rust
description: "Rust done well: ownership and borrowing idioms, error handling with thiserror and anyhow, traits, generics or trait objects, lifetimes, iterators, unsafe with SAFETY proofs and Miri, async with tokio (Send bounds, cancellation, blocking work), shared state and channels, performance habits, clippy and rustfmt, features and MSRV, choosing crates, and cross-compiling. Read when writing or reviewing Rust."
---

# Rust, idiomatic and sound

Rust on autopilot calls `.clone()` until the borrow checker goes quiet,
`unwrap()`s every `Result`, returns `Box<dyn Error>` from a library, wraps
everything in `Arc<Mutex<_>>`, sleeps a thread inside an async task, and
reaches for `unsafe` to get past a lifetime error. This is the Rust a
senior reviewer expects: borrowing by default, typed errors, unsafe with
proofs, async that cancels cleanly, and the tooling that keeps it so.
General rules in `systems`, threads and atomics in `systems-concurrency`,
a web service in `backend-stack-rust`.

## 1. Ownership and API shape

- Parameters borrow: `&str` not `&String`, `&[T]` not `&Vec<T>`,
  `impl AsRef<Path>` for paths. Take `String` or `Vec<T>` only when the
  function keeps it. Return owned values, or a borrow of `self` for a
  view; `Cow<'_, str>` when the input usually comes back unchanged.
- Clone on purpose: an `Arc` or a small `Copy` value is cheap; cloning a
  `Vec` to satisfy the borrow checker means the data flow is wrong (split
  the borrow, restructure the loop, use indices).
- Newtypes carry invariants and units: `UserId(u64)`, `Millis(u64)`,
  `Name(String)` with a validating `TryFrom`, a private field, no
  `DerefMut`. `NonZeroU32` gives `Option` a free niche.
- Builders past three or four optional settings; `#[must_use]` where a
  result must not be dropped; `#[non_exhaustive]` on public types that
  will grow; `Debug` always (by hand when a field is secret).

## 2. Errors

Libraries: an error enum per crate or module with `thiserror` 2, variants
a caller can match, sources kept. Binaries: `anyhow` (or `eyre` with
`color-eyre`), with context on every `?` that crosses a boundary.

```rust
#[derive(Debug, thiserror::Error)]
#[non_exhaustive]
pub enum LoadError {
    #[error("reading {path}")]
    Io { path: PathBuf, source: std::io::Error },
    #[error("header truncated: need {need} bytes, have {have}")]
    Truncated { need: usize, have: usize },
    #[error("unsupported version {0}")]
    Version(u16),
}

// In the binary, with `use anyhow::Context;`
let cfg = load(&path).with_context(|| format!("loading config {}", path.display()))?;
```

- Messages lowercase, no trailing period, the source's text not repeated:
  the chain prints it (`{:#}` with anyhow; `{:?}` adds the backtrace
  under `RUST_BACKTRACE=1`).
- No `unwrap()` outside tests and invariants proven on the line above;
  `expect` states the proof (`.expect("regex literal is valid")`);
  `lock().expect("state lock poisoned")` passes on an earlier panic.
- Panics are for bugs, never for input; no `Result<T, String>` in a
  library API; `main` returns `anyhow::Result<()>` or `ExitCode`.

## 3. Traits, generics, trait objects

| Need | Use |
|---|---|
| One concrete type per call site, speed matters | `fn run<R: Read>(r: R)` or `fn run(r: impl Read)` |
| Mixed collection, plug-in chosen at run time | `Box<dyn Trait>`, `Arc<dyn Trait + Send + Sync>` |
| Hide a long return type | `-> impl Iterator<Item = T> + '_` |
| Only your crate may implement it | sealed: `pub trait Codec: private::Sealed` |

- Generics monomorphise: fast code, bigger binary, slower builds. Keep the
  generic layer thin over a non-generic inner function
  (`open(p: impl AsRef<Path>)` calling `open_inner(p.as_ref())`).
- `dyn` needs a dyn-compatible trait: no generic methods, no `Self` by
  value, no `async fn` (native `async fn` in traits is for static
  dispatch; for `dyn`, `async-trait` or a boxed future).

## 4. Lifetimes and iterators

- Trust elision. A struct with a lifetime (`Parser<'a>`) is a short-lived
  view; types that live long own their data. `T: 'static` means "owns its
  data", not "lives forever": for `spawn`, move owned data or an `Arc` in,
  or borrow with `std::thread::scope`.
- No self-referential structs: keep the buffer plus `Range<usize>`
  indices (`self_cell` if that fails, never hand-written `unsafe`).
  Graphs: `Vec<Node>` with `u32` or `slotmap` keys, or `Rc` down, `Weak` up.
- Iterators are lazy and collect once, at the end;
  `collect::<Result<Vec<_>, _>>()` stops at the first error; `retain`,
  `drain` and `extend` work in place; `zip`, `chunks_exact` and `windows`
  avoid the bounds checks indexing pays.

## 5. Unsafe

- Justified by FFI, a measured hot path where the compiler cannot prove a
  bound, or a structure std lacks; never by a lifetime error. One
  operation per block with a `// SAFETY:` proof, a `# Safety` section on
  each `pub unsafe fn`, a safe wrapper around it (`systems`, section 5).
- The rules that bite: a `&mut T` is unique for its whole life; a
  reference to uninitialised memory is UB even unread (`MaybeUninit<T>`
  and `&raw mut` instead); `slice::from_raw_parts` needs a non-null
  aligned pointer even for length 0; `transmute` between types without a
  defined layout is UB; `static mut` references are denied in edition 2024.

```sh
rustup +nightly component add miri
cargo +nightly miri test
MIRIFLAGS="-Zmiri-strict-provenance" cargo +nightly miri test
MIRIFLAGS="-Zmiri-many-seeds" cargo +nightly miri test   # other schedules and addresses
cargo +nightly careful test                               # std with its debug checks
RUSTFLAGS="-Zsanitizer=address" cargo +nightly test -Zbuild-std --target x86_64-unknown-linux-gnu
```

Miri is slow and does not run foreign C code: small inputs, and
`#[cfg_attr(miri, ignore)]` on the tests it cannot run.

## 6. Async with tokio

- `#[tokio::main]` (a worker per core) for servers, `flavor =
  "current_thread"` for CLIs; one runtime, never `block_on` inside it.
- `tokio::spawn` needs `Send + 'static`. A `std::sync::MutexGuard` or `Rc`
  alive across `.await` makes the future `!Send`: drop it in a block first
  (clippy `await_holding_lock`); `tokio::sync::Mutex` only when a lock must
  be held across an await.
- Blocking off the workers: CPU work over about 100 microseconds,
  `std::fs`, blocking C calls and compression go to `spawn_blocking` (or
  rayon, answering on a `oneshot`). Never `std::thread::sleep`.
- Cancellation drops the future at its pending `.await`; the rest never
  runs. `select!` branches must be cancel safe: `mpsc::Receiver::recv`,
  `TcpListener::accept` and `CancellationToken::cancelled` are;
  `read_exact`, `read_line` and `write_all` are not.
- A timeout on every external call (`tokio::time::timeout`); bounded
  channels (`mpsc::channel(1024)`), `Semaphore` or `buffer_unordered(n)`
  to cap concurrency. `JoinSet` aborts its tasks on drop; a dropped
  `JoinHandle` detaches, it does not cancel.

Structured shutdown with `tokio-util` (feature `rt`):

```rust
let token = CancellationToken::new();
let tracker = TaskTracker::new();
let worker_token = token.clone();
tracker.spawn(async move {
    loop {
        tokio::select! {
            () = worker_token.cancelled() => break,
            job = rx.recv() => match job {
                Some(job) => handle(job).await,
                None => break, // every sender is gone
            },
        }
    }
});
tracker.close();
shutdown_signal().await; // Ctrl-C or SIGTERM (`systems-os`)
token.cancel();
if tokio::time::timeout(Duration::from_secs(20), tracker.wait()).await.is_err() {
    eprintln!("tasks still running after 20s, exiting anyway");
}
```

## 7. Shared state and channels

- Channels first: `std::sync::mpsc::sync_channel(n)` or
  `crossbeam-channel` between threads; tokio's `mpsc`, `oneshot`, `watch`
  (latest value) and `broadcast` between tasks.
- `Arc<Mutex<T>>` with short critical sections; `RwLock` only when reads
  dominate and the mutex measurably contends; `parking_lot` for locks
  without poisoning; `arc-swap` for read-mostly data replaced whole.
- Globals: `static CONFIG: OnceLock<Config>` set once at startup;
  `static RE: LazyLock<Regex> = LazyLock::new(|| Regex::new(r"^\d+$").expect("valid regex"));`
  (`once_cell` and `lazy_static` are no longer needed). rayon
  (`par_iter`, `par_chunks`) for data parallelism.

## 8. Performance habits

Measure first (`systems`, section 7). What costs nothing:

- No allocation in hot loops: hoist buffers and `clear()` them (capacity
  stays), `with_capacity(n)`, `write!` into a reused `String` instead of
  `format!` per item. `SmallVec<[T; N]>` for collections usually under N;
  `Box<str>` or `Arc<str>` for strings that never grow.
- std's SipHash resists hash flooding (keep it for keys an attacker
  picks); `rustc-hash` or `foldhash` for trusted keys in hot maps.
- `memchr`, `bytes::Bytes`, `sort_unstable`; `#[inline]` only on small
  functions called across crates.

```toml
[profile.release]
lto = "fat"         # or "thin" when link time hurts; measure both
codegen-units = 1
panic = "abort"     # only when nothing catches panics (not FFI libraries)
```

Profile a `[profile.profiling]` (`inherits = "release"`, `debug =
"line-tables-only"`) with `samply record` or `cargo flamegraph`; count
allocations with `dhat`; benchmark with criterion (`harness = false`,
inputs through `std::hint::black_box`). `-C target-cpu=native` only for
binaries run where they are built.

## 9. Tooling, lints and crates

```toml
[lints.rust]
unsafe_op_in_unsafe_fn = "deny"
unexpected_cfgs = { level = "warn", check-cfg = ["cfg(loom)"] }

[lints.clippy]
pedantic = { level = "warn", priority = -1 }
missing_errors_doc = "allow"
undocumented_unsafe_blocks = "warn"
```

- Pedantic on, the lints the team rejects allowed in one place
  (`[workspace.lints]`, `lints.workspace = true` in members); a local
  exception says why:
  `#[expect(clippy::cast_possible_truncation, reason = "len < 2^16, checked above")]`.
- `cargo deny check` (advisories, licences, bans, duplicates, sources)
  with a committed `deny.toml`; `cargo machete` or `cargo +nightly udeps`
  for unused dependencies; `cargo nextest run` plus `cargo test --doc`
  (nextest skips doctests); `cargo semver-checks` before a library release.
- A new crate earns its place: recent releases and answered issues,
  reverse dependencies, how much `unsafe` and why, its own tree
  (`cargo tree -e normal -i <crate>`), MSRV, licence. Defaults: `serde`,
  `postcard`, `thiserror`, `anyhow`, `clap`, `tracing`, `tokio`, `reqwest`,
  `rustls`, `blake3`, `rayon`, `crossbeam-channel`, `parking_lot`,
  `bytes`, `memchr`, `winnow`, `proptest`, `insta`, `criterion`.

## 10. Features, MSRV, edition

- Features are additive: enabling one never removes an API or changes
  behaviour another crate relies on (Cargo unifies them across the graph).
  Optional dependencies via `dep:`; `cargo hack --feature-powerset check`
  tests the combinations.
- MSRV in `rust-version = "1.85"`, checked in CI with that toolchain;
  resolver 3 (default in edition 2024) prefers dependency versions that
  support it. Raise it on purpose, in a minor release, and say so.
- Edition 2024 for new crates (`cargo fix --edition`). What needs thought:
  `unsafe extern` blocks, `#[unsafe(no_mangle)]`, `std::env::set_var` is
  `unsafe`, return-position `impl Trait` captures every lifetime in scope.

## 11. Cross-compiling and no_std

```sh
rustup target add aarch64-unknown-linux-gnu x86_64-unknown-linux-musl
cargo zigbuild --release --target aarch64-unknown-linux-gnu.2.17   # zig links; glibc 2.17 floor
cross build --release --target aarch64-unknown-linux-gnu           # container toolchain; cross test too
cargo xwin build --release --target x86_64-pc-windows-msvc          # MSVC target from Linux or macOS
```

- A bare `cargo build --target` fails on C dependencies (`-sys` crates,
  `cc`) that need the target's C toolchain; these tools bring it. musl is
  static but its allocator is slow under threads: add `mimalloc`.
- `no_std`: `#![cfg_attr(not(feature = "std"), no_std)]` with a default
  `std` feature, `extern crate alloc;` for `Vec` and `String`,
  `core::error::Error` (stable since 1.81), `#[panic_handler]` in binaries.

## Check it

```sh
cargo fmt --all --check
cargo clippy --workspace --all-targets --all-features -- -D warnings
cargo test --workspace --all-features       # or cargo nextest run, then cargo test --doc
cargo +nightly miri test                    # unsafe changed
```

Read the warnings, not only the exit code; every new `#[allow]` or
`#[expect]` has a reason. Say which of these could not run here.

## Avoid

`clone()` to quiet the borrow checker; `&String` and `&Vec<T>` parameters;
`unwrap` in library code; `Box<dyn Error>` or `String` errors from a
library; lifetimes on long-lived structs; self-referential structs with
`unsafe`; `unsafe` without `SAFETY`; `static mut`; a std mutex guard across
`.await`; blocking or `sleep` on the runtime; unbounded channels; external
calls without timeouts; tasks nobody owns; features that remove things;
`target-cpu=native` in distributed builds; a crate for ten lines of code.
