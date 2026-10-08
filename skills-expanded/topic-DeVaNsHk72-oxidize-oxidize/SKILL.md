---
name: oxidize
description: >-
  Migrate, port, or rewrite a codebase or application to Rust — from Python, JavaScript/TypeScript/Node,
  Go, C, C++, Java, Ruby, or C#/.NET. Use this skill whenever the user wants to move code to Rust:
  "rewrite it in Rust" (RIIR), oxidize a service, port a hot path for speed, replace a slow native
  extension, shrink memory, or incrementally migrate one module behind an FFI boundary
  (PyO3, napi-rs, cxx, bindgen, JNI, magnus, wasm). Trigger it even when the user only says
  "make this faster in Rust", "can we port this", or "should we rewrite this in Rust" — it covers
  whether to migrate at all, strategy, interop, idiom translation, behavior-parity verification,
  and production rollout.
---

# Oxidize — migrating code and apps to Rust

Most Rust rewrites fail for the same reasons: they attempt a big-bang rewrite that never ships, they
translate the source language literally and end up with un-idiomatic Rust that fights the borrow
checker, or they cut over without ever proving the new code behaves like the old one. This skill exists
to prevent those three failures.

Your job is to run a **disciplined, incremental migration** where the old system keeps working at every
step, each ported piece is proven equivalent before it replaces anything, and idiomatic Rust is the
finishing move — not the opening one.

## Core principles

Hold these throughout; every phase below is in service of them.

1. **Parity before idiom.** First make Rust that does *exactly* what the old code did, proven by tests.
   Only then refactor it to be idiomatic and fast. Trying to do both at once is how subtle behavior
   changes slip in.
2. **Incremental over big-bang.** Prefer porting module-by-module behind a stable interface (FFI, a
   service boundary, or wasm) so you can ship continuously and roll back cheaply. Reserve full rewrites
   for small, well-specified components. See `references/strategy.md`.
3. **Prove equivalence with differential tests.** The old implementation is your oracle. Run both on the
   same inputs and diff the outputs. This is the single highest-leverage thing you can do — set it up
   *before* porting logic. See `references/verification.md`.
4. **Keep it shippable at every step.** Never have a "big red" period where nothing works. The repo
   should build, pass tests, and be deployable after every merge.
5. **Don't migrate on autopilot — advise honestly.** Rust is the right tool for CPU-bound work, memory
   footprint, predictable latency, memory safety, and long-lived services. It is often the *wrong* tool
   for glue code, rapidly-changing prototypes, or teams with no Rust capacity and no time to build it.
   If a migration is a bad idea, say so and explain why before writing code.

## Before anything: is this migration worth it?

Do this thinking first, out loud, with the user. Don't skip to code.

- **What is the actual goal?** Speed? Memory? Safety? Removing a GC pause? Deleting a fragile C
  extension? Consolidating a service? Each goal implies a different scope and a different success metric.
- **What's the smallest slice that delivers it?** A "port the whole app" ask is usually satisfied by
  porting one hot module and leaving the rest. Push for the smallest valuable slice.
- **Is there a cheaper win first?** Sometimes an algorithmic fix, a caching layer, or a native library in
  the *current* language beats a rewrite. Name it if you see it.
- **Who maintains the Rust?** A migration that lands and then rots because nobody on the team reads Rust
  is a net negative. Factor this in.

Write down the **goal, the success metric, and the scope** before proceeding. If the user can't name a
metric, help them pick one (e.g. p99 latency < X ms, RSS < Y MB, throughput ≥ Z req/s, zero segfaults).

## The migration workflow

Follow these phases in order. Each names the reference to read when you reach it — read the reference
when you get there, not upfront, to keep context focused.

### Phase 0 — Assess the codebase

Understand what you're dealing with before proposing a plan.

- Run `scripts/assess.sh <path>` to inventory languages, lines of code, build systems, dependency
  counts, and likely entry points. It's read-only and works without extra tools installed.
- Identify the **hot paths** and the **boundaries**: where does data enter and leave each module? Clean
  boundaries are where you'll cut. Tangled globals and shared mutable state are where migration gets
  expensive — flag them early.
- Catalog external dependencies. For each, decide: does Rust have a mature equivalent crate, do you wrap
  the existing native lib via FFI, or does this dependency block the migration? Check crates.io /
  lib.rs / blessed.rs for equivalents.

### Phase 1 — Choose a strategy and find the seams

Read `references/strategy.md`. Decide between:

- **Incremental via FFI** — port a module, call it from the old language across an FFI boundary. Best for
  hot paths inside a larger app (a Python data pipeline, a Node server, a C++ engine).
- **Strangler service** — stand up a Rust service alongside the old one, route a slice of traffic to it,
  grow its responsibility over time. Best for network services with clean request/response boundaries.
- **wasm boundary** — compile Rust to WebAssembly and call it from JS/Python/etc. Best for portable,
  sandboxed logic shared across runtimes.
- **Full rewrite** — only for small, well-specified, self-contained components where a clean boundary is
  cheap to define and the whole thing fits in a reviewable change.

Pick the **order of migration**: usually leaf modules (few dependencies) or the single hottest path
first, so you get a win and a working pattern early.

### Phase 2 — Scaffold the Rust project

Read `references/production.md`. Set up a Cargo workspace, lint/format/audit tooling, and CI *before*
writing logic, so quality gates exist from commit one. Do not defer this — retrofitting CI and clippy
onto a pile of already-written code is painful and things rot in the gap.

### Phase 3 — Build the verification harness FIRST

Read `references/verification.md`. Before porting real logic, stand up the way you'll prove parity:

- A **differential/golden harness** (`scripts/parity_check.py` is a reusable template) that feeds the
  same corpus of inputs to the old and new implementations and diffs outputs.
- **Property-based tests** (proptest) for logic where you can state invariants but can't enumerate cases.
- **Snapshot tests** (insta) for structured outputs.

This is the phase people skip and the phase that makes migrations trustworthy. Do it early.

### Phase 4 — Port module by module

Read `references/translation-patterns.md` for source-language idiom → Rust idiom mapping, and consult
`references/pitfalls.md` when the borrow checker fights you.

For each module: translate for **parity first** (a faithful, possibly ugly port), get it passing the
differential harness against the oracle, commit, *then* idiomatize. Resist the urge to "improve" behavior
during translation — capture behavior changes as separate, deliberate commits.

### Phase 5 — Wire it in via interop

Read the relevant section of `references/interop.md` for the source language (PyO3/maturin for Python,
napi-rs or wasm for Node, cxx/bindgen for C++, JNI for Java, magnus for Ruby, C ABI + csbindgen for
C#/Go). Expose the ported module across the boundary and replace the old implementation's call site —
ideally behind a flag so you can switch back instantly.

### Phase 6 — Roll out safely

Read the rollout section of `references/strategy.md`. Prefer: **shadow** (run new alongside old, compare
in production, serve old) → **canary** (serve new to a small % ) → **cutover** → remove old code. Wire up
metrics for the success metric you chose, and keep the rollback path live until you're confident.

### Phase 7 — Idiomatize and harden

Now make it good Rust. Read `references/pitfalls.md` and the idiom guidance. Remove parity-era crutches
(excess `.clone()`, `unwrap()`, `unsafe` shims), tighten error types, add `#![deny(warnings)]` where
appropriate, run clippy at `-W clippy::pedantic` and address what's worth addressing, and benchmark
(criterion) to confirm you hit the metric.

## Quick idiom cheat-sheet

The most common source→Rust translations, so you don't need to open a reference for the basics. See
`references/translation-patterns.md` for the full treatment (OOP, concurrency, memory model, generics).

| Source concept | Rust equivalent |
| --- | --- |
| `null` / `None` / `nil` / `undefined` | `Option<T>` |
| exceptions / `try`/`catch` | `Result<T, E>` + `?`; `thiserror` for lib errors, `anyhow` for apps |
| dynamic dict / object | `struct` (known shape) or `HashMap` / `serde_json::Value` (dynamic) |
| class with methods | `struct` + `impl`; behavior sharing via `trait`, not inheritance |
| inheritance | composition + `trait` objects (`dyn Trait`) or enums + generics |
| duck typing / interface | `trait` bounds (`impl Trait` / `<T: Trait>`) |
| GC'd shared reference | `Rc<T>` (single-thread) / `Arc<T>` (threads); `RefCell`/`Mutex` for interior mutability |
| list / array | `Vec<T>`; slices `&[T]` for borrowed views |
| string | `String` (owned) vs `&str` (borrowed) — pick borrowed in signatures |
| threads with shared state | `Arc<Mutex<T>>`, or channels; `rayon` for data parallelism |
| `async`/`await` | `async`/`.await` on a runtime (`tokio`); mind function-color spread |
| `for x in list` mutating | iterator chains (`.iter().map().filter().collect()`) |

## Reference map

- `references/strategy.md` — migration strategies, finding seams, ordering, and safe rollout.
- `references/interop.md` — FFI/interop per source language (PyO3, napi-rs, wasm, cxx, bindgen, JNI, magnus, csbindgen).
- `references/translation-patterns.md` — idiom translation in depth: errors, ownership, OOP, concurrency, generics.
- `references/verification.md` — differential testing, property tests, snapshots, fuzzing, benchmarks.
- `references/production.md` — Cargo workspace layout, clippy/rustfmt/deny/audit, CI, MSRV, release.
- `references/pitfalls.md` — borrow-checker fights, over-cloning, unsafe misuse, and the anti-patterns to avoid.

## Scripts

- `scripts/assess.sh <path>` — read-only codebase inventory (languages, LOC, build files, deps, entry points).
- `scripts/parity_check.py` — reusable differential/golden test harness: runs old vs new over a corpus and diffs outputs.
