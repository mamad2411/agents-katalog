---
name: follow-lang-zig
description: Write Zig per best practices and language conventions
argument-hint: "[scope|setup-project]"
related:
  - follow-lang-rust
  - follow-best-practice
  - run-bench
  - setup-cicd
  - use-scripts
  - deep-research
---

## Goal

Write Zig applications and libraries per best practices and language conventions

## Scope

For Zig applications, libraries, and build scripts. Package: `SKILL.md` entry + `references/toolchain.md` (ecosystem-tool table) + `workflows/setup-project/SKILL.md` (argument `setup-project` — first-time `zig init` scaffold). Zig is pre-1.0: verify the current language/toolchain breaking changes via `/deep-research` at use time before writing build scripts or C interop (official docs: https://ziglang.org/documentation/)

## Execute

### 1. Check Version And Setup Project

> Goal: set up the Zig project and build configuration for the installed toolchain

1. Run `/deep-research` + `/follow-best-practice` to confirm the installed `zig version`, the current `build.zig.zon`/module API, and latest Zig practices — the build-system API changes between minors; read the official Zig Guide section for that version before coding `build.zig`
2. New project → run the workflow `workflows/setup-project/SKILL.md` (argument `setup-project`): toolchain pin, `zig init` scaffold, build graph, dependencies, verify
3. Tool inventory (compiler, build selects, formatter, `zig fetch`, `translate-c`, `zls`) → `references/toolchain.md`
4. Build/run/test/fmt: `zig build`, `zig build run`, `zig build test`, `zig fmt`, `zig build --help`/`-l`

### 2. Write Zig Code

> Goal: write idiomatic Zig

1. `const` for immutable (including comptime-known) values, `var` only when mutation is needed
2. Errors as `error{ ... }` sets + error unions (`!T`), propagate with `try`/`catch`; optionals `?T` unwrapped with `orelse`
3. Cleanups with `defer` (always) and `errdefer` (only on error return) — RAII-style resource management
4. `@import("std")` for the standard library; a function returning `!void` for a fallible main

### 3. Memory Management

> Goal: manage memory explicitly and safely

1. Every heap allocation takes an allocator; prefer `GeneralPurposeAllocator` (debug leak detection via `deinit` result) and `ArenaAllocator` for batch lifetimes
2. Free with `defer allocator.free(...)`; with an arena, drop the batch instead of individual frees
3. Prefer stack values and slices over heap where possible; check leaks in tests (`std.testing` with a GPA)

### 4. Optimize Performance

> Goal: use compile-time features and SIMD

1. `comptime` for compile-time computation and generic code (types are values)
2. `inline` for small hot functions; `@Vector` for SIMD operations
3. Release builds with the appropriate optimize mode (`ReleaseFast`/`ReleaseSafe`/`ReleaseSmall`); inspect generated assembly when tuning
4. Profile before optimizing; measure with `/run-bench`

### 5. C Interop

> Goal: bind C correctly for the current toolchain

1. C headers are translated in the build system (e.g. `b.addTranslateC`) and imported as modules — the inline `@cImport` form was deprecated in recent 0.16-era releases; live-check which form the installed version supports and migrate if stale
2. `extern` functions/`extern fn` for linking C symbols; verify ABI compatibility for the target

## Rules

### 1. Conventions

- `camelCase` variables/functions, `PascalCase` types, `snake_case` files, `SCREAMING_SNAKE_CASE` constants; 4-space indent; 100-column style (`zig fmt` is the formatter — never fight it)

### 2. Error Handling

- Meaningful named errors, no silent `catch {}`; `errdefer` for cleanup on failure; `!T` in signatures, `try` inside

### 3. Memory Safety

- Explicit allocator passed down call chains; `defer` guaranteed cleanup; bounds checked by default; `@ptrCast`/`@alignCast` only with documented safety reasoning

### 4. Pre-1.0 Volatility

- Never hardcode Zig version numbers or removed-syntax workarounds in project code; `references/toolchain.md` holds commands/roles only — check breaking changes via `/deep-research` at use time

- Use /follow-lang-rust if needed
- Use /follow-best-practice if needed
- Use /setup-cicd if needed
- Use /use-scripts if needed

## Expected Outcome

- Idiomatic Zig code following official conventions and formatting
- Explicit, leak-checked memory management with allocators and defer/errdefer
- Robust error handling with error unions
- Performance tuned with comptime, SIMD, and optimize modes
- Clean, maintainable, and build-system-correct projects
