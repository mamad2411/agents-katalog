---
name: rust-porting-mistakes
description: >
  A concrete catalog of real regressions from porting Zig/C/C++ code to
  Rust, where the Rust looks like a faithful translation but behaves
  differently — debug_assert! erasing side effects, ReleaseFast-vs-Rust
  bounds checks, bytemuck panics on odd-length slices, comptime format
  strings that must become macros, and eager unwrap_or. Use when
  translating code to Rust and wanting to avoid these specific traps, when
  reviewing a Rust port for behavioral divergence, when debugging a Rust
  regression that only shows up in release builds or on edge-case inputs,
  or when the user asks "what breaks when porting to Rust" / "why does my
  ported Rust behave differently than the original". The Rust-specific
  companion to semantic-porting-pitfalls; give it to adversarial reviewers.
---

# Rust porting mistakes

A stability-focused port still ships regressions — Bun's Zig→Rust rewrite introduced 19 known ones, each since fixed, and **most came from code that is syntactically identical in both languages but semantically different in Rust.** This skill is the concrete catalog of those traps with the real bugs, so you can avoid them while translating and target them while reviewing (hand this to adversarial reviewers — see `adversarial-code-review`). For the language-agnostic version of these categories, see `semantic-porting-pitfalls`.

## 1. `debug_assert!` erases side effects in release

Zig's `assert(expr)` is a **function** — `expr` runs in every build. Rust's `debug_assert!(expr)` is a **macro** — in release builds the entire expression is erased, side effects included.

```zig
// Zig — insertStale runs in every build
assert(try dev.client_graph.insertStale(rfr.import_source, false) == react_refresh_index);
```
```rust
// Rust — insert_stale is COMPILED OUT in release builds
debug_assert!(dev.client_graph.insert_stale(&rfr.import_source, false)? == react_refresh_index);
```
`insert_stale` registered a file in the dev server's hot-reload graph. In release builds it stopped running and HMR broke for React projects with HTML routes (`Cannot destructure property 'isLikelyComponentType'`). Debug builds worked, which hid it.

**Rule:** never put a side-effecting call inside `debug_assert!`/`assert!`. Compute the effect on its own line, then assert on the result:
```rust
let idx = dev.client_graph.insert_stale(&rfr.import_source, false)?;
debug_assert!(idx == react_refresh_index);
```
Fingerprint: works in debug, broken in release.

## 2. Release-build bounds checks (ReleaseFast vs. Rust)

Zig compiled with `ReleaseFast` **removes bounds checks**; Rust release builds **keep them**. Indexing that silently ran off the end in Zig will **panic** in Rust.

Bun's resolver interned filenames into overflow blocks sized `count / 4` (≈2048). The port left a placeholder:
```rust
/// nonzero stand-in until Phase B threads the real value through
pub const BSS_OVERFLOW_BLOCK_SIZE: usize = 64;
```
That dropped the ceiling from 8.4M interned filenames to 270,272, which real projects hit, and made a ported `ptrs[4095]` off-by-one reachable — Rust panicked where Zig had written past the end. (Zig would also have panicked under `ReleaseSafe`, which Bun only used on Windows.)

**Rules:** the panic is the *safe* outcome — treat it as Rust surfacing a latent bug, not as Rust being annoying. Never leave placeholder/"stand-in until later" constants in ported code; they become live limits. Re-derive size constants from the source exactly rather than guessing.

## 3. `bytemuck::cast_slice` panics on odd lengths

A Zig helper that silently tolerated a bad length maps to a Rust std/crate function that **panics** on it.

Zig's `reinterpretSlice(u16, bytes)` used `@divTrunc` and ignored a trailing odd byte. `bytemuck::cast_slice` panics when the byte length isn't a clean multiple of the element size. `Blob.text()` on a UTF-16 BOM followed by an odd number of bytes went from returning a string to panicking the process.

**Fix:** replicate the original tolerance explicitly.
```rust
let usable = &buf[..buf.len() & !1]; // drop the trailing odd byte, like the Zig did
```
**Rule:** audit every cast/reinterpret over raw bytes for odd length, zero length, and alignment. Don't assume the Rust cast helper has the same tolerance as the source.

## 4. `comptime` format strings must become macros

Zig `comptime fmt` is rewritten **before** arguments are substituted; a plain Rust function only ever sees the already-substituted string, so any transformation it does runs over the arguments too.

`Output.pretty` rewrites color markers `<r>`/`<d>` into ANSI escapes. In Zig, `fmt` is `comptime`, so markers are processed before args are filled in.
```zig
pub inline fn pretty(comptime fmt: string, args: anytype) void;
Output.pretty("<r>{f}<r>", .{hyperlink});
```
Ported to a Rust function taking a finished string, `pretty` also rewrote markers that appeared inside the arguments. A `bun update -i` OSC 8 hyperlink ends in `ESC \`; the `\` sat right before a trailing `<r>`, the marker parser ate it, and `r` printed as literal text (`oxfmtr` instead of `oxfmt`).

**Fix:** it has to be a macro so the format string is processed at the call site before substitution: `bun_core::pretty!("<r>{}<r>", hyperlink)`.

**Rule:** any Zig `comptime`-string API whose behavior depends on transforming the template *before* args are filled in must become a Rust **macro**, not a function. See `zig-to-rust-mapping`.

## 5. Eager `unwrap_or` (and eager fallbacks generally)

`unwrap_or(expr)` evaluates `expr` **eagerly**, even when the value is `Some`.
```rust
// panics when only `second.percentage` is None — the arg runs on the Some path too
let p1 = first.percentage.unwrap_or(1.0 - second.percentage.unwrap());
```
`color-mix(in srgb, red 40%, blue)` (only the second percentage omitted) panicked inside the argument before `unwrap_or` could ignore it.

**Fix:** use the lazy form.
```rust
let p1 = first.percentage.unwrap_or_else(|| 1.0 - second.percentage.unwrap());
```
**Rule:** if a fallback can panic or is expensive, use `unwrap_or_else` / `ok_or_else` / `get_or_insert_with` (lazy), not `unwrap_or` / `ok_or` (eager). The same eager-vs-lazy care applies to `.map_or`, default arguments, and any "or" combinator.

## Using this catalog

- **While translating:** when you write a `debug_assert!`, an index, a byte-slice cast, a color/format helper, or an `unwrap_or`, stop and check it against the matching entry above.
- **While reviewing:** these five are the reviewer's primary search targets for a Rust port. A reviewer seeing only the diff should grep for `debug_assert!` with a call inside, raw indexing near ported size constants, `cast_slice`, format helpers that reinterpret markers, and eager `unwrap_or`.
- **While debugging:** "works in debug, fails in release" → #1 or #2. "works on most inputs, panics on one edge case" → #2, #3, or #5.
