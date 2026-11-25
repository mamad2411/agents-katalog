---
name: semantic-porting-pitfalls
description: >
  Catalogs the "looks identical, behaves differently" traps that cause
  most port regressions — code that is syntactically the same in both
  languages but semantically different (assert-as-function vs. assert-as-
  macro, comptime/const evaluation, release-vs-debug bounds checks, slice
  and numeric edge cases, eager vs. lazy evaluation). Use when translating
  code between languages and wanting to avoid subtle regressions, when
  reviewing ported code for behavioral divergence, when the user asks
  "what breaks when porting from X to Y", "why does the ported code behave
  differently", or is debugging a regression that only appears in release
  builds or edge cases. Pairs with adversarial-code-review; see
  rust-porting-mistakes for the Rust-target specifics.
---

# Semantic porting pitfalls

The dangerous bugs in a mechanical port are almost never the code that fails to compile. They're the code that compiles cleanly, reads like a faithful translation, and quietly does something different at runtime. Bun's Rust rewrite shipped 19 known regressions despite heavy review — **most from code that is syntactically identical in both languages but semantically different.**

This skill is a checklist of those divergence classes. Use it while translating, and hand it to adversarial reviewers so they look for the right things. The specific manifestations below are Zig→Rust, but every language pair has its own version of each class — the *categories* are what transfer.

## The divergence classes

### 1. Function vs. macro (side effects that vanish)

A construct that is a **function** in the source language evaluates its arguments in every build. The "same" construct as a **macro** in the target may erase the whole expression in release builds — taking any side effects with it.

- Zig `assert(x)` is a function: `x` runs in every build. Rust `debug_assert!(x)` is a macro: in release builds the entire expression is erased, including any function calls inside it.
- Bun regression: `debug_assert!(dev.client_graph.insert_stale(...)? == idx)` — `insert_stale` had a real side effect (registering a file in the hot-reload graph). In release builds it stopped running, and HMR broke. Debug builds worked, which made it hard to catch.

**Rule:** any expression with a side effect must not live inside an assertion (or any construct) that the target may compile out. If you need the effect, compute it on its own line, then assert on the result.

### 2. Compile-time vs. runtime evaluation

Source languages with compile-time evaluation (`comptime`, `constexpr`, macros over literals) may resolve something *before* other work happens; the target's ordinary runtime code resolves it *after*. Ordering changes meaning.

- Zig `Output.pretty(comptime fmt, args)` rewrites color markers like `<r>`/`<d>` into ANSI escapes at compile time — *before* arguments are substituted. Ported to a plain Rust function, `pretty` only ever saw the finished, already-substituted string, so it rewrote markers that appeared inside the *arguments* too. A hyperlink argument ending in `\` collided with a trailing `<r>` and printed a stray `r`.
- **Fix pattern:** when the source relied on compile-time-before-substitution ordering, the target usually needs a **macro**, not a function, to preserve it (`pretty!("<r>{}<r>", x)`).

Audit every `comptime`/`constexpr`/const-generic construct: does the port preserve *when* it evaluates, or just *what* it computes?

### 3. Release-vs-debug safety checks

The source and target may default to different safety in release builds. Code that "can't overflow" or "can't go out of bounds" because the source silently wrapped or skipped the check will **panic** in a target that keeps the check — or vice versa.

- Bun compiled Zig with `ReleaseFast` (no bounds checks) on macOS/Linux; Rust release builds keep bounds checks. A placeholder constant lowered an interned-filename ceiling from 8.4M to 270,272, which real projects hit, and made a ported `ptrs[4095]` off-by-one reachable — Rust panicked where Zig had written past the end silently.
- **Lesson:** the target keeping a check is the *safe* outcome — it converts latent corruption into a visible crash. But it means placeholder constants and off-by-ones that were invisible in the source become live. Don't leave `// stand-in until later` constants in ported code (see also stubbing in `compiler-errors-as-work-queue`).

### 4. Slice / buffer edge cases

Helpers that silently tolerate an edge case in the source may **panic or assert** in the target's stricter standard library.

- Zig's `reinterpretSlice(u16, bytes)` used `@divTrunc` and silently ignored a trailing odd byte. Rust's `bytemuck::cast_slice` panics on a length that isn't a clean multiple. `Blob.text()` on a UTF-16 BOM followed by an odd number of bytes went from returning a string to panicking the process. Fix: replicate the old tolerance explicitly — `&buf[..buf.len() & !1]`.
- Audit every cast/reinterpret/chunk over raw bytes for: odd lengths, zero length, unaligned pointers, and trailing remainders.

### 5. Numeric and sign edge cases

Truncation vs. flooring, signedness, and rounding differ subtly and bite hardest on negative or boundary inputs.

- `trunc()` rounds toward zero; `floor()` rounds toward negative infinity. Splitting a negative float time into `{sec, nsec}` with `trunc` yields a negative `nsec` — an invalid timespec. Use `floor` so the fractional part stays in `[0, 1e9)`.
- Check: negative inputs, zero, min/max of the integer type, and values right at a boundary.

### 6. Eager vs. lazy evaluation

The "or-default" and short-circuit constructs may or may not evaluate their fallback.

- Rust `unwrap_or(expr)` evaluates `expr` eagerly — even on the `Some` path. If `expr` can panic or is expensive, it runs when it shouldn't. `unwrap_or_else(|| expr)` stays lazy. The same distinction exists between `||`/`&&` and non-short-circuiting boolean ops, and between eager and lazy default-argument idioms across languages.

## How to use this

- **While translating:** when you hit any of these constructs, stop and ask whether the target preserves the *semantics*, not just the syntax. A faithful-looking line is exactly where these hide.
- **While reviewing:** give this list to adversarial reviewers as their search targets (see `adversarial-code-review`). Reviewers seeing only the diff should specifically probe assertions with side effects, comptime constructs, release-only behavior, byte-slice casts, negative/boundary numerics, and eager fallbacks.
- **When a regression appears only in release or only on some inputs:** that pattern (debug works, release doesn't; most inputs work, one edge case crashes) is the fingerprint of a class-1, class-3, or class-5 bug. Start here.
