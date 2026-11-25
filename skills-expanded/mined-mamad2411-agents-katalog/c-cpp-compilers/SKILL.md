---
name: c-cpp-compilers
description: C and C++ compiler toolchain skill covering GCC, Clang/LLVM, build modes, warnings, sanitizers, static analysis, LTO, PGO, C++20/23/26 features, and debugging. Use when writing or reviewing C/C++ code, choosing compiler flags, interpreting errors or warnings, enabling sanitizers, running clang-tidy or cppcheck, optimizing builds, working with C++20 modules or C23 features, or troubleshooting linker issues.
---

# C/C++ Compilers

Guidance for compiling, analyzing, and optimizing C and C++ code with GCC and Clang in 2026.

## Reference files

- **GCC specifics**: [gcc.md](reference/gcc.md) -- flags, diagnostics, PGO, LTO, error triage
- **Clang specifics**: [clang.md](reference/clang.md) -- diagnostics, optimization remarks, clang-tidy, macOS
- **Sanitizers**: [sanitizers.md](reference/sanitizers.md) -- ASan, UBSan, TSan, MSan, LSan decision tree and reports
- **Static analysis**: [static-analysis.md](reference/static-analysis.md) -- clang-tidy, cppcheck, scan-build, CI integration
- **Modern C/C++**: [modern-cpp.md](reference/modern-cpp.md) -- C++20 modules, C++23/26 features, C23, migration

## Standards baseline (2026)

| Language | Preferred standard | GCC support | Clang support |
|----------|--------------------|-------------|---------------|
| C | `-std=c23` (or `-std=c17` for broad compat) | GCC 15+ | Clang 18+ |
| C++ | `-std=c++23` (or `-std=c++20` minimum) | GCC 14+ | Clang 18+ |

Always pass the standard flag explicitly. Never rely on compiler defaults.

## Build modes

| Goal | Flags |
|------|-------|
| Debug | `-g -O0 -Wall -Wextra -Wpedantic` |
| Debug (GDB-friendly optimized) | `-g -Og -Wall -Wextra` |
| Release | `-O2 -DNDEBUG -Wall` |
| Release (max throughput, native) | `-O3 -march=native -DNDEBUG -flto` |
| Release (min binary size) | `-Os -DNDEBUG` (Clang: `-Oz`) |
| Sanitizer build | `-g -O1 -fsanitize=address,undefined -fno-omit-frame-pointer` |

## Warning discipline

Start with `-Wall -Wextra -Wpedantic`. Add `-Werror` in CI.

Suppress narrow scopes only:

```c
#pragma GCC diagnostic push
#pragma GCC diagnostic ignored "-Wunused-parameter"
void callback(int ctx, int unused) { (void)ctx; }
#pragma GCC diagnostic pop
```

Clang equivalent works the same. For project-wide suppression, prefer `.clang-tidy` config or `-Wno-<flag>` in build system, not in source.

## Optimization decision tree

```
Need max throughput on known hardware?
  yes -> -O3 -march=native -flto
  no  -> Have profiling data?
           yes -> -O2 -fprofile-use (GCC) / -fprofile-instr-use (Clang)
           no  -> -O2

Size-constrained (embedded, shared lib)?
  yes -> -Os (GCC/Clang) or -Oz (Clang only)

Numerical code that tolerates IEEE relaxation?
  yes -> -Ofast (enables -ffast-math; breaks NaN/inf handling)
  no  -> stay with -O2/-O3
```

`-O3` vs `-O2`: `-O3` adds aggressive loop transforms and wider inlining. Benchmark before committing -- i-cache pressure can cause regressions.

## LTO

```bash
# GCC
gcc -O2 -flto=auto -c foo.c bar.c
gcc -O2 -flto=auto foo.o bar.o -o prog

# Clang (ThinLTO preferred for large projects)
clang -O2 -flto=thin -fuse-ld=lld -c foo.c bar.c
clang -O2 -flto=thin -fuse-ld=lld foo.o bar.o -o prog
```

Use `gcc-ar` / `gcc-ranlib` for GCC LTO archives. Clang ThinLTO links 5-10x faster than full LTO with comparable code quality.

## PGO (profile-guided optimization)

**GCC:**

```bash
gcc -O2 -fprofile-generate prog.c -o prog_inst
./prog_inst < workload.input
gcc -O2 -fprofile-use -fprofile-correction prog.c -o prog
```

**Clang (LLVM instrumentation):**

```bash
clang -O2 -fprofile-instr-generate prog.c -o prog_inst
./prog_inst < workload.input
llvm-profdata merge -output=prog.profdata default.profraw
clang -O2 -fprofile-instr-use=prog.profdata prog.c -o prog
```

## Sanitizer quick reference

| Bug class | Sanitizer | Flag |
|-----------|-----------|------|
| Heap/stack/global OOB, use-after-free, double-free | ASan | `-fsanitize=address` |
| Signed overflow, null deref, bad shift, misaligned access | UBSan | `-fsanitize=undefined` |
| Data races | TSan | `-fsanitize=thread` |
| Uninitialised reads (Clang only, all-instrumented build) | MSan | `-fsanitize=memory` |
| Memory leaks | LSan | via ASan (`detect_leaks=1`) or standalone |

Common combo: `-fsanitize=address,undefined -fno-sanitize-recover=all -fno-omit-frame-pointer -g -O1`

TSan and MSan are mutually exclusive with ASan. See [sanitizers.md](reference/sanitizers.md) for report interpretation.

## Static analysis (quick start)

```bash
# Generate compilation database
cmake -S . -B build -DCMAKE_EXPORT_COMPILE_COMMANDS=ON

# Run clang-tidy (recommended checks)
clang-tidy -checks='bugprone-*,clang-analyzer-*,performance-*,modernize-*' \
  -p build src/foo.cpp

# Run cppcheck
cppcheck --enable=warning,performance,portability --error-exitcode=1 src/
```

See [static-analysis.md](reference/static-analysis.md) for `.clang-tidy` config, CI integration, and suppression patterns.

## Common error triage

| Symptom | Likely cause | Fix |
|---------|-------------|-----|
| `undefined reference to 'foo'` | Missing `-lfoo` or wrong link order | Libraries after objects: `gcc main.o -lfoo` |
| `multiple definition of 'x'` | Defined in header without `static`/`inline` | `extern` in header, define in one `.c` |
| `implicit declaration of function` | Missing `#include` or wrong standard | Add the header; check `-std=` |
| `incompatible pointer types` | Wrong cast or missing prototype | Fix type; enable `-Wall` |
| ABI errors in C++ | Mixed `-std=` or different `libstdc++` | Unify standard across all TUs |
| `relocation truncated` | 32-bit relocation overflow | `-mcmodel=large` or restructure |

## CMake integration

```cmake
cmake_minimum_required(VERSION 3.28)
project(myproject LANGUAGES C CXX)

set(CMAKE_C_STANDARD 23)
set(CMAKE_CXX_STANDARD 23)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

option(SANITIZE "Build with ASan+UBSan" OFF)
if(SANITIZE)
    set(san_flags -fsanitize=address,undefined -fno-sanitize-recover=all
                  -fno-omit-frame-pointer -g -O1)
    add_compile_options(${san_flags})
    add_link_options(${san_flags})
endif()
```

## Useful one-liners

```bash
# Show all optimizations enabled at -O2 (GCC)
gcc -Q --help=optimizers -O2 | grep enabled

# Assembly output (Intel syntax)
gcc -S -masm=intel -O2 foo.c -o foo.s

# Preprocess and dump macros
gcc -dM -E - < /dev/null

# Clang optimization remarks (missed vectorization)
clang -O2 -Rpass-missed=loop-vectorize src.c

# Clang save all remarks to YAML
clang -O2 -fsave-optimization-record src.c

# Show include search path
gcc -v -E - < /dev/null 2>&1 | grep -A20 '#include <...>'
```

## Compiler-specific details

For GCC-specific flags, PGO nuances, and error patterns, see [gcc.md](reference/gcc.md).
For Clang diagnostics, optimization remarks, macOS toolchain, and clang-tidy, see [clang.md](reference/clang.md).
For C++20 modules, C++23/26, and C23 features, see [modern-cpp.md](reference/modern-cpp.md).
