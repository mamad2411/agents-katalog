---
name: c-to-rust-migration
description: "Complete C/C++ to Rust migration pipeline. Analyzes code difficulty, converts to idiomatic safe Rust, and validates the result. Covers memory management, pointer translation, error handling, unsafe minimization, and differential testing. Use when: migrate C to Rust, rewrite in Rust, C to Rust conversion, Rust migration, convert C code, C2Rust, unsafe Rust reduction."
license: MIT
metadata:
  version: 1.0.0
  category: migration
  tags: [rust, c, cpp, migration, safety, systems, memory-safety]
---

# C to Rust Migration

Complete pipeline for migrating C/C++ codebases to safe, idiomatic Rust. Covers analysis, conversion, and validation in three phases.

## Pipeline

```
C/C++ Source
    |
Phase 1: ANALYZE
    | Classify difficulty (easy/medium/hard)
    | Detect patterns (pointers, macros, goto, unions)
    | Plan conversion strategy
    |
Phase 2: CONVERT
    | Apply migration patterns
    | Memory management → ownership/borrowing
    | Error codes → Result<T, E>
    | Pointer arithmetic → slices/iterators
    | Quality gate: re-translate if >5 unsafe blocks
    |
Phase 3: VALIDATE
    | Compilation check (edition 2024)
    | Unsafe minimization (target: 0 for easy/medium)
    | Clippy with 0 warnings
    | Differential testing (same I/O as original C)
    | Idiomatic score calculation
    |
Safe, Idiomatic Rust
```

## Phase 1: Analysis

Classify each function by migration difficulty:

| Difficulty | Patterns | Strategy |
|---|---|---|
| **Easy** | Pure functions, simple arithmetic, no pointers, <30 lines | Direct translation, should produce 0 unsafe |
| **Medium** | Pointer parameters, simple structs, bounded arrays, malloc with clear ownership | Translate with ownership patterns, minimize unsafe |
| **Hard** | void*, function pointers, unions, goto, complex lifetimes, macro-heavy | May need C2Rust as starting point, then iterative cleanup |

**Hard signals** (any one → Hard): `goto`, `setjmp`/`longjmp`, variadic functions, inline assembly, complex `#define` macros with side effects.

See `references/analysis-patterns.md` for the complete pattern catalog.

## Phase 2: Conversion Patterns

Core translations:

| C Pattern | Rust Pattern |
|---|---|
| `malloc`/`free` | `Vec`, `Box`, or stack allocation |
| `char*` strings | `&str`, `String`, `CStr` |
| `int` error codes | `Result<T, Error>` with `thiserror` |
| `NULL` checks | `Option<T>` |
| Array + length params | Slices (`&[T]`) |
| `void*` | Generics or `enum` dispatch |
| Function pointers | `Fn` traits or enum dispatch |
| `struct` with `init`/`free` | `impl` with `new()` + `Drop` |
| Global mutable state | `OnceLock`, `Mutex`, or dependency injection |
| `goto` cleanup | `Drop` guards or `?` operator |

**Quality gate**: If translation produces >5 `unsafe` blocks, re-attempt with lower temperature (0.5) focusing on the unsafe sections.

See `references/conversion-patterns.md` for detailed examples from real migrations.

## Phase 3: Validation

Checklist (in order):

1. **Compilation**: `cargo build` with edition 2024, zero errors
2. **Clippy**: `cargo clippy` with zero warnings
3. **Unsafe audit**: Count `unsafe` blocks. Every one needs a `// SAFETY:` comment explaining why it's sound
4. **Differential testing**: Same inputs → same outputs as original C code
5. **Idiomatic score**: `(1 - unsafe_blocks/total_functions) * 0.4 + clippy_clean * 0.3 + has_tests * 0.2 + has_docs * 0.1`

**Quality floor**: Never accept a version that scores lower than the current best. If a fix attempt reduces the score, discard it.

See `references/validation-checklist.md` for the complete validation protocol.

## Example Output

```
C-to-Rust Migration Report — http_parser.c

Analysis:
  Total functions: 23
  Easy: 8 | Medium: 11 | Hard: 4
  Hard patterns: 2 goto statements, 1 union, 1 function pointer dispatch

Conversion:
  Functions migrated: 23/23
  Unsafe blocks: 2 (both in FFI boundary — justified)
  Idiomatic patterns applied: Result<T,E>, Option<T>, iterators, Drop guards

Validation:
  ✅ Compiles (edition 2024)
  ✅ Clippy: 0 warnings
  ✅ Unsafe: 2 blocks, both with SAFETY comments
  ✅ Diff tests: 47/47 passing (100%)
  Idiomatic score: 0.91/1.0

Quality: EXCELLENT — ready for production use
```

## Error Handling

- **C code doesn't compile**: Need the original build system info (Makefile, CMakeLists.txt) to understand dependencies and flags
- **Too many unsafe blocks**: Re-attempt conversion focusing on the unsafe sections. Consider if some are FFI boundaries (justified) vs unnecessary
- **Diff tests fail**: Compare output byte-by-byte. Common causes: endianness, floating point precision, uninitialized memory in C
- **Circular dependencies**: Rust doesn't allow circular module deps. Restructure with traits or merge modules

## Origin

Patterns extracted from real-world C-to-Rust migrations of open-source libraries: cJSON, genann, http-parser, picohttpparser, olive.c.
