---
name: efficient-code-rust
description: Applies when writing or reviewing Rust code. Extends the core efficient-code principles with Rust-specific rules around Vec::with_capacity, String vs &str, iterator chains as zero-cost abstractions, Box/Rc/Arc tradeoffs, bounds-check elision, format! allocations, release-build discipline, and clippy perf lints.
---

# Efficient Code — Rust

This skill assumes you also have the core `efficient-code` skill active.

## Stdlib primitives

- **`Vec<T>`** — contiguous, amortized O(1) push. `Vec::with_capacity(n)` avoids reallocation when size is known. Internal layout: `(ptr, len, cap)`.
- **`String`** — `Vec<u8>` of UTF-8. `String::with_capacity(n)` to preallocate. **`&str`** is a borrowed slice — zero-copy, always prefer for read-only parameters.
- **`HashMap<K,V>`** — average O(1); `HashMap::with_capacity(n)` to preallocate.
- **`BTreeMap<K,V>`** — B-tree, O(log n), ordered; better cache behavior than red-black trees.
- **`HashSet` / `BTreeSet`** — same tradeoff.
- **`VecDeque<T>`** — ring buffer, O(1) push/pop at both ends.
- **`Box<T>`** — single heap allocation.
- **`Rc<T>`** — non-atomic reference count, single-thread only.
- **`Arc<T>`** — atomic reference count, multi-thread, more expensive per clone.
- **Iterators** — `iter()` / `into_iter()` / `iter_mut()` chains are **zero-cost abstractions** — they compile to the same code as hand-written loops. Chain freely.
- Third-party: `smallvec` / `tinyvec` / `arrayvec` for stack-allocated small-vector optimization (stdlib has none).

## Rust-specific gotchas

1. **`clone()` is explicit and usually an allocation + copy.** It's often a sign you should pass `&T` instead.
2. **`String` vs `&str`:** functions should take `&str` for read-only access; return `String` only when ownership is needed. `&String` auto-derefs to `&str`.
3. **`Vec::push` reallocates when `len == cap`** (growth factor ~2×). Always `with_capacity` when the size is known.
4. **`format!("{}", x)` allocates a new `String`.** In hot loops, `write!` to an existing `String` or `io::Write` target.
5. **`println!` takes a lock on stdout each call.** Batch writes via `BufWriter` and `writeln!`.
6. **`Vec` never auto-shrinks.** Call `shrink_to_fit()` to release unused capacity.
7. **Trait object `Box<dyn Trait>`** adds a vtable indirection and prevents inlining. Prefer generics (`impl Trait` or `<T: Trait>`) for monomorphic dispatch when the concrete types are known.
8. **`Rc` / `Arc` cycles leak** — break with `Weak`.
9. **`Arc<Mutex<T>>` is the "shared state" hammer.** Contention is usually the bottleneck; prefer message passing (`crossbeam_channel`, `tokio::sync::mpsc`) or sharding.
10. **`.collect::<Vec<_>>()` allocates.** Chain iterators without collecting when possible.
11. **`?` on `Result` is essentially free.** `panic!` unwinds the stack (expensive) unless you set `panic = "abort"` in `Cargo.toml`.
12. **Async state machines:** `async fn` desugars to a generated type; large futures are often boxed in practice. Holding a non-`Send` guard across an `.await` is a common bug and forces the runtime to pin to one thread.
13. **The borrow checker forbids many O(1) patterns.** Interior mutability via `RefCell` / `Cell` exists but adds runtime checks. `UnsafeCell` is the unsafe escape hatch.
14. **`unsafe` is not faster by default** — use only with measurement and clear bounds.
15. **Bounds checks on slice indexing:** prefer iterators (the compiler elides checks automatically) or use `get_unchecked` in measured hot paths.
16. **`#[inline]` is a hint.** `#[inline(always)]` forces; use sparingly.
17. **`cargo build --release` is mandatory for any benchmark.** Debug builds are 10-100× slower.
18. **`lto = "fat"` and `codegen-units = 1`** in the release profile give extra performance at compile cost.
19. **`cargo clippy` has a `perf` lint group** — run it; many of its suggestions are listed here.

## Profiling

`cargo flamegraph` (wraps `perf` + FlameGraph); `samply` for cross-platform; `criterion` via `cargo bench` for microbenchmarks.

## Sources

- https://doc.rust-lang.org/std/vec/struct.Vec.html
- https://nnethercote.github.io/perf-book/
- https://rust-lang.github.io/rust-clippy/master/ (perf lints group)
- https://doc.rust-lang.org/nomicon/
- https://github.com/bheisler/criterion.rs
