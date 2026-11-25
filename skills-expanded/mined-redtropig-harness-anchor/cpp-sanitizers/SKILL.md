---
name: cpp-sanitizers
description: Use in C/C++ projects for crashes, hangs, UB, data races, memory errors. ASan/UBSan/TSan runtime checks. Build sanitizer config separately.
---

# C/C++ Sanitizers — Runtime Bug Catchers

Sanitizers are compiler-instrumented runtime checks. They catch what static analysis can't (path-sensitive errors, race conditions, memory errors discovered at runtime). They run your normal tests under instrumentation; failures abort with a precise report.

| Sanitizer | What it catches | Slowdown |
|---|---|---|
| **ASan** (Address) | Use-after-free, heap/stack overflow, leaks (leaks: Linux only) | 2-3x |
| **UBSan** (UB) | Signed overflow, null deref, misaligned, OOB shift, ... (MSVC: unavailable — see Platform notes) | ~1.1x |
| **TSan** (Thread) | Data races, deadlocks (not available on Windows — see Platform notes) | 5-10x |
| **MSan** (Memory) | Use of uninitialized memory | 3x (Linux only, Clang only) |

Note: ASan + UBSan are combinable. TSan is **mutually exclusive** with ASan/MSan.

## The `/sanitize` command

`/sanitize` automates the ASan+UBSan build+test flow below and reports findings in a fixed
structure (Build / Tests / Findings / Verdict / Recommendation) with a `.harness-anchor/sanitize-*.log`
evidence path. Reach for it for a one-shot run; read on to understand what it does, how to
read the output, and how to suppress known third-party noise. Run TSan separately — it cannot
share a build with ASan.

## Prerequisites

- Clang or recent GCC (`-fsanitize=` family supported since GCC 4.8 / Clang 3.1+)
- A separate sanitizer build directory (don't mix configs)
- Tests that actually exercise the suspect code paths — **and that the runner actually runs**: a
  sanitizer build only catches UB on paths its tests execute, so a binary built but never
  `add_test`-registered is silently skipped (a false "clean"). Use `/test-plan` to find such run-scope
  gaps before trusting a clean result.

## Standard build setup

### ASan + UBSan (most useful default)

```bash
# CMake
cmake -S . -B .build/asan \
    -DCMAKE_BUILD_TYPE=Debug \
    -DCMAKE_CXX_FLAGS="-fsanitize=address,undefined -fno-omit-frame-pointer -g -O1" \
    -DCMAKE_EXE_LINKER_FLAGS="-fsanitize=address,undefined"
cmake --build .build/asan
ctest --test-dir .build/asan --output-on-failure
```

```bash
# Meson
meson setup builddir-asan -Db_sanitize=address,undefined -Db_lundef=false
meson test -C builddir-asan
```

### LeakSanitizer (LSan) — the leak half of ASan

ASan's "leaks" row above **is** LeakSanitizer. Platform truth:

- **Linux**: leak detection is **on by default** with ASan.
- **macOS / Apple toolchains**: LeakSanitizer is **not supported** — setting
  `ASAN_OPTIONS=detect_leaks=1` makes every ASan binary **abort at startup** with
  `detect_leaks is not supported on this platform` (it is NOT a silent no-op). The
  generated `scripts/sanitizer-build.sh` selects per-OS (Darwin/MinGW/MSYS/Cygwin → 0,
  else → 1). For leak hunting on macOS use `leaks`(1) / Instruments, or run the ASan+LSan
  suite on Linux CI.
- **Windows (MSVC or clang)**: LeakSanitizer is likewise **not supported** — same
  startup abort if forced. The generated `scripts/sanitizer-build.sh` turns it off on
  MINGW*/MSYS*/CYGWIN* too. Substitute leak hunters: [platform/windows.md](platform/windows.md).

On Linux, when you want leaks *without* ASan's memory-error overhead, link the **standalone** detector:

```bash
clang -fsanitize=leak -g -O1 your_prog.c -o your_prog   # Linux; not available on Apple toolchains
```

Suppress known third-party leaks with the same `leak:` syntax as ASan, via LSan's own var:

```bash
LSAN_OPTIONS=suppressions=lsan-suppressions.txt ./your_test   # file holds e.g. leak:libfoo
```

For the in-code opt-out API (disabling leak checks for a region), invoke `docs-lookup` rather than guessing the symbol names.

### TSan (separately)

```bash
cmake -S . -B .build/tsan \
    -DCMAKE_BUILD_TYPE=Debug \
    -DCMAKE_CXX_FLAGS="-fsanitize=thread -fno-omit-frame-pointer -g -O1" \
    -DCMAKE_EXE_LINKER_FLAGS="-fsanitize=thread"
cmake --build .build/tsan
```

### valgrind (Linux, when sanitizers unavailable)

```bash
valgrind --tool=memcheck --leak-check=full ./your_test_binary
```

slower than ASan (10-50x) but works without recompiling.

## Platform notes (Windows)

> **Windows:** read [platform/windows.md](platform/windows.md) before choosing
> sanitizers or substitutes — it holds the substitute-tool preference table
> (TSan / LSan / MSVC-UBSan / Valgrind replacements).

What DOES work natively on Windows: **ASan** — MSVC (`cl /fsanitize=address`, VS 2019 16.9+)
and clang-on-Windows both support it; the generated ASan+UBSan script works under Git
Bash with a clang/MinGW toolchain. Substitute tools are recommendations to run yourself —
`/sanitize` never auto-runs them; a sanitizer that did not run is never reported CLEAN.

## Reading sanitizer output

ASan example:
```
==12345==ERROR: AddressSanitizer: heap-use-after-free on address 0x60200000001c
READ of size 4 at 0x60200000001c thread T0
    #0 main main.cpp:42
    #1 ...
freed by thread T0 here:
    #0 ...
    #1 main.cpp:30
previously allocated by thread T0 here:
    #0 ...
    #1 main.cpp:25
```

Reading order: **error class → access pattern → freed/allocated stack traces**. The use-after-free trio (allocated → freed → used) almost always tells you the bug.

## Suppressions

For known bugs in third-party code, use a suppression file (`asan-suppressions.txt`):

```
leak:libfontconfig
race:third_party/lib_with_known_race
```

Run: `ASAN_OPTIONS=suppressions=asan-suppressions.txt ./your_test`

## Anti-patterns

- ❌ Running sanitizers in production builds — they're for testing only
- ❌ Disabling a sanitizer check globally to silence a warning — fix the bug
- ❌ Mixing ASan and TSan in one build — they conflict
- ❌ Treating UBSan warnings as informational — UB is real, fix it

## When to invoke

- Test fails intermittently → likely a race (TSan)
- Crash with cryptic memory address → likely UAF or buffer overflow (ASan)
- Test passes but behavior is weird → maybe uninitialized read (MSan, or UBSan)
- Before any release / merge to main → run full ASan+UBSan suite

## See `ub-failure-patterns.md` for common UBSan signatures and their fixes — it doubles as the **C/C++ arm** of `test-coverage-design`'s risk-construct checklist.

## Looking up unfamiliar signatures

When a sanitizer report uses an error class outside `ub-failure-patterns.md` — invoke the `docs-lookup` skill. It tries Context7 first, then WebSearch (best for recent regressions or platform-specific issues), then calibrated uncertainty if both fail.

Typical entry query: `clang sanitizer <error-class>` or paste the exact runtime error string.
