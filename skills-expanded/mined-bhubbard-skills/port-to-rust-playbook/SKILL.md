---
name: port-to-rust-playbook
description: >
  End-to-end orchestration guide for porting or rewriting a C, C++, Zig,
  Go, or other systems codebase INTO Rust — why Rust wins for memory-
  safety-critical code, and the full sequence from planning to shipping.
  Use whenever the target language of a port is Rust: "rewrite our engine
  in Rust", "port this C library to Rust", "migrate the Zig codebase to
  Rust", "should we move X to Rust", or planning a Rust rewrite of a
  performance-sensitive or memory-unsafe codebase. This is the Rust-target
  entry point; it ties together port-planning, rust-lifetimes-analysis,
  zig-to-rust-mapping, rust-crate-decomposition, and rust-porting-mistakes
  with the generic porting-workflow-loops and adversarial-code-review.
---

# Port-to-Rust playbook

This is the top-level guide when the *target* is Rust. It explains when a Rust rewrite is the right call and sequences the whole effort, pointing to the specialized skills for each stage. It generalizes Bun's Zig→Rust rewrite (~535k lines, 11 days, Claude Code + adversarial review), and applies equally to C, C++, or Go sources.

## When Rust is the right target

Rust pays off when your bug list is dominated by memory-safety and resource-lifetime errors. The specific case for it:

- **Use-after-free, double-free, and "forgot to free in an error path" become compiler errors** in safe Rust, instead of runtime crashes caught (if you're lucky) by sanitizers, fuzzing, or CI. A compiler error is a strictly better feedback loop than a style guide enforced by code review — it fires before the code runs, on every build, for everyone.
- **`Drop` gives RAII-style automatic cleanup.** Cleanup runs exactly once when a value goes out of scope, eliminating the "forgot a `defer`/`free`" leak and the "ran cleanup twice in a rare error branch" double-free — the two failure modes that dominate manual-memory codebases.
- **The borrow checker encodes ownership in the type system** instead of in a 31,000-word style guide that best-effort linting can't fully enforce.

Rust is *not* automatically the answer. If your bugs are logic errors, concurrency-design errors, or API-design errors, Rust won't fix them. And a rewrite historically freezes feature/security/bugfix work for months — only worth it if you can de-risk it down to days, which is what the rest of this playbook is about. C++ is a reasonable alternative (constructors/destructors, fewer FFI wrappers) but still leans on style guides and still lets memory corruption through even with ASAN.

Concrete payoffs Bun measured after the Rust port: **~20% smaller binary**, **memory usage that levels off instead of leaking** (a 2,000-iteration build loop went from 6.7 GB to 0.6 GB), **less stack usage** in recursive parsers (LLVM reuses stack slots via lifetime intrinsics), and **2–5% higher throughput** (cross-language LTO inlines across the C/C++ boundary).

## The sequence

Run these stages in order. Each links to the skill that covers it in depth.

### 1. Plan (`port-planning`)
Decide **big-bang vs. incremental** (default big-bang for a whole codebase) and **mechanical vs. idiomatic** (default mechanical — make the Rust look like transpiled source, refactor toward idiomatic *after* it ships). Produce a `PORTING.md` mapping guide and a decision record. Do not skip this; a few hours here saves days.

### 2. Map the patterns (`zig-to-rust-mapping`)
Serialize how each source construct becomes Rust: error/optional types, tagged unions → enums, cleanup idioms → `Drop`, compile-time constructs → const generics or macros. This is what keeps thousands of files consistent.

### 3. Solve ownership up front (`rust-lifetimes-analysis`)
Rust's headline difficulty in a port from manual-memory or GC code is lifetimes. Trace every long-lived struct field's actual control flow, decide its ownership model, and write it into a `LIFETIMES.tsv` before translating. Review the mapping and lifetime guides together (adversarially) to resolve conflicts.

### 4. Translate in parallel loops (`porting-workflow-loops`)
Mechanically port every source file to a `.rs` file following the guides, using write→review→apply loops across worktree shards, with strict git discipline. None of it compiles yet — that's expected.

### 5. Split into crates (`rust-crate-decomposition`)
A single giant crate compiles slowly. Split into ~100 crates to parallelize compilation — while avoiding cyclic dependencies and minimizing divergence from the original structure.

### 6. Burn down compiler errors (`compiler-errors-as-work-queue`)
Rust's compiler is your work queue. Dump errors per crate, group, divide among workers, fix/review/apply crate by crate. Cyclic-dependency errors are the hard class — classify then refactor.

### 7. Get to green (`test-suite-driven-port`)
Reuse the original test suite (ideally language-independent). Progress smoke tests → local green → CI green on every platform, with cgroup isolation for resource-hungry tests.

### 8. Guard against semantic traps (`semantic-porting-pitfalls`, `rust-porting-mistakes`)
Throughout translation and review, watch the Rust-specific "looks identical, behaves differently" cases: `debug_assert!` erasing side effects, release-build bounds checks that Zig's `ReleaseFast` skipped, `bytemuck` panicking on odd-length slices, and comptime format strings that must become macros.

### 9. Verify and merge (`port-verification-checklist`)
Confirm the green is real — tests actually ran, nothing stubbed, no tests skipped or deleted — then merge. Merging to main commits you to the rewrite; it needn't be a versioned release yet.

## After it ships: harvest the Rust-native tooling

Once green, a Rust codebase unlocks stability tools worth scheduling follow-up work around: the borrow checker, [Miri](https://github.com/rust-lang/miri) for UB detection in CI, LeakSanitizer for tracking native allocations, and coverage-guided fuzzing for parsers. Plan an idiomatic-cleanup pass to reduce `unsafe` incrementally now that behavior is locked by the suite.
