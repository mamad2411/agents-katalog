---
name: zig-to-rust-mapping
description: >
  Concrete construct-by-construct mapping from Zig to Rust for a
  mechanical port — error/optional types, tagged unions, defer/errdefer →
  Drop, comptime → const generics or macros, allocators, and the idioms
  that DON'T map 1:1. Use when translating Zig code to Rust, building or
  filling in a PORTING.md for a Zig→Rust port, when the user asks "what's
  the Rust equivalent of Zig's X", "how do I port defer / comptime /
  tagged unions to Rust", or is mechanically translating .zig files to
  .rs. Part of the port-to-rust-playbook; feeds the PORTING.md that
  porting-workflow-loops follows. For non-Zig sources, adapt the same
  categories; see rust-porting-mistakes for the semantic traps.
---

# Zig → Rust mapping

This is the reference for translating Zig constructs into Rust during a mechanical port — the raw material for a `PORTING.md`. The aim is a structure-for-structure translation so anyone who understands the Zig understands the Rust, and reviewers can diff behavior directly. Idiomatic cleanup comes later (see `port-to-rust-playbook`).

Two guiding principles:

- **Preserve behavior over elegance.** Prefer the mapping that reproduces the Zig semantics exactly, even if the Rust looks verbose or uses `unsafe`.
- **Where a construct doesn't map 1:1, reproduce the *effect* deliberately.** The dangerous mappings are the ones that look faithful but aren't — those are called out below and cataloged in `rust-porting-mistakes`.

## Core type mappings

| Zig | Rust | Notes |
| --- | --- | --- |
| `?T` (optional) | `Option<T>` | `null` → `None`, `x` → `Some(x)` |
| `!T` / `E!T` (error union) | `Result<T, E>` | `try x` → `x?` |
| `try expr` | `expr?` | error propagation |
| `error{...}` set | `enum` implementing `Error` | one variant per error |
| tagged `union(enum)` | `enum` with data | Zig's tag payload → enum variant fields |
| `union` (bare) | `union` (`unsafe`) or refactor to enum | bare unions need `unsafe`; prefer enum if a tag exists |
| `struct` | `struct` | field-for-field |
| `[]T` / `[]const T` (slice) | `&mut [T]` / `&[T]` | carry the lifetime; see `rust-lifetimes-analysis` |
| `[*]T` (many-item pointer) | `*mut T` / `*const T` | raw pointer, `unsafe` at use |
| `*T` | `&T`/`&mut T` if owned lifetime is clear, else `*const/*mut T` | decided by the lifetime analysis |
| `anytype` param | generic `<T>` with trait bounds, or `impl Trait` | pick bounds that match how it's used |
| `enum` (plain) | `enum` (fieldless) | |
| integer types `u32`, `usize`, … | same names | Rust matches |
| `[N]T` (array) | `[T; N]` | |

## Cleanup: `defer`/`errdefer` → `Drop`

This is the highest-value mapping and the whole reason to target Rust.

- Zig runs cleanup explicitly at each call site with `defer` (always) and `errdefer` (on error only). It's easy to forget one (leak) or run one twice in a rare error branch (double-free).
- Rust runs cleanup automatically via `Drop` when a value leaves scope — once, guaranteed.

```zig
// Zig
const bytes: ArrayBuffer = try .fromPinned(global, value);
defer bytes.unpin();
```
```rust
// Rust — cleanup moves into the type, runs automatically
impl Drop for Bytes {
    fn drop(&mut self) {
        if !self.pinned.is_empty() {
            JSC__JSValue__unpinArrayBuffer(self.pinned);
        }
    }
}
```

Mapping rules:

- A value with a `defer cleanup()` at its call sites usually wants a `Drop` impl that does `cleanup()`. Then the explicit `defer` lines disappear.
- **Exception — escapes to FFI/async/callbacks.** If the value is handed to something that outlives the scope (a C library, an async close callback), automatic `Drop` will free memory the foreign side still holds — a use-after-free/double-free. Do **not** give those a naive `Drop`; use `Box::leak` (with the callback reclaiming) or `ManuallyDrop`, and record it in `LIFETIMES.tsv`.
- `errdefer` (cleanup only on the error path) maps naturally: `Drop` fires when the value is dropped by the `?` early-return, and not when the value is moved into the success result.

## `comptime` → const generics or macros (carefully)

Zig `comptime` has no single Rust equivalent; the right target depends on *what* the comptime did.

- **Comptime value/type parameter** → **const generic** or generic type parameter.
  ```zig
  fn can_merge(comptime is_ts_enabled: bool) ...
  ```
  ```rust
  fn can_merge<const IS_TS_ENABLED: bool>() ...
  ```
- **Comptime that transforms a value *before* other work happens (e.g. a `comptime fmt` string rewritten before args are substituted)** → **a macro**, not a function. A plain Rust function only ever sees the finished value and evaluates in the wrong order. `Output.pretty(comptime fmt, args)` had to become `pretty!(...)`. This is a top source of regressions — see `rust-porting-mistakes`.
- **Comptime used purely to generate code / specialize** → generics, macros, or (last resort) a build script. Note that heavy `comptime` in Zig tends to bloat the binary; the Rust port often shrinks it.

## `assert` → `debug_assert!` (watch side effects)

Zig `assert(expr)` is a **function**: `expr` runs in every build. Rust `debug_assert!(expr)` is a **macro**: the whole expression is erased in release builds. If `expr` had a side effect, it silently stops happening in release. Never put a side-effecting call inside `debug_assert!` — compute it on its own line first. (Detailed in `rust-porting-mistakes`.)

## Allocators and memory

- Zig passes an `Allocator` explicitly; Rust uses the global allocator by default. Most `allocator.alloc`/`allocator.free` pairs collapse into ordinary owned types (`Box`, `Vec`, `String`) whose `Drop` frees them.
- Where the source used a custom allocator/arena for a real reason (bump allocation for parser nodes), map to an arena crate or a slab/`Vec`-backed arena, and tie borrows to it.
- Zig `@ptrCast`/`@alignCast`/`@bitCast` → `as`, `.cast()`, `bytemuck`/`transmute` (`unsafe`). Beware slice casts on odd lengths — `bytemuck::cast_slice` panics where Zig silently truncated (see `rust-porting-mistakes`).

## Build-mode differences

Zig `ReleaseFast` removes bounds checks; Rust release keeps them. Ported indexing that "couldn't" go out of bounds in Zig may panic in Rust — which is the safe outcome, but means placeholder constants and off-by-ones become live. Don't leave stand-in constants in ported code.

## Filling in PORTING.md

Use these categories as the skeleton of the project's `PORTING.md`, then extend it as translation surfaces cases this list doesn't cover. Keep it a living document — when a file reveals a Zig idiom with no entry, decide the mapping once, write it down, and every subsequent worker inherits it.
