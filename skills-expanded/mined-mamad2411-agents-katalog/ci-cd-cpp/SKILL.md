---
name: ci-cd-cpp
description: "Applies when creating or modifying CI/CD pipelines for C/C++ projects. Covers ccache, gcov/lcov coverage, cppcheck/clang-tidy, and sanitizers (ASan/UBSan)."
---

# C / C++ CI/CD

## Setup and caching

Use `hendrikmuhs/ccache-action@v1` for compilation caching:

```yaml
- uses: hendrikmuhs/ccache-action@v1
  with:
    key: ${{ runner.os }}-ccache
```

Pass ccache as the compiler launcher in CMake:

```bash
cmake -B build \
  -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_C_COMPILER_LAUNCHER=ccache \
  -DCMAKE_CXX_COMPILER_LAUNCHER=ccache
cmake --build build --parallel
```

## Coverage

Compile with coverage flags, run tests, generate report:

```bash
cmake -B build -DCMAKE_BUILD_TYPE=Debug \
  -DCMAKE_C_FLAGS="--coverage" -DCMAKE_CXX_FLAGS="--coverage"
cmake --build build --parallel
ctest --test-dir build --output-on-failure

# Generate Cobertura XML
gcovr --root . --filter src/ --xml coverage.xml
# Or HTML via lcov:
lcov --capture --directory build --output-file coverage.info
lcov --remove coverage.info '/usr/*' '*/test/*' --output-file coverage.info
```

Tools: `gcov` (GCC built-in), `gcovr` (Cobertura XML output), `lcov`/`genhtml` (HTML reports).

## Linting and static analysis

```bash
# cppcheck
cppcheck --enable=all --error-exitcode=1 --suppress=missingInclude src/

# clang-tidy (needs compile_commands.json)
cmake -B build -DCMAKE_EXPORT_COMPILE_COMMANDS=ON
run-clang-tidy -p build src/
```

## Sanitizers

Add as a separate CI job — compile with sanitizer flags and run tests:

```bash
cmake -B build-sanitize \
  -DCMAKE_C_FLAGS="-fsanitize=address,undefined -fno-omit-frame-pointer" \
  -DCMAKE_CXX_FLAGS="-fsanitize=address,undefined -fno-omit-frame-pointer"
cmake --build build-sanitize --parallel
ctest --test-dir build-sanitize --output-on-failure
```

Any memory error or undefined behavior causes a non-zero exit.

## Dependency audit

No single standard tool. Use:
- `osv-scanner` for known CVEs in vendored or system dependencies.
- Trivy for container images that bundle C/C++ binaries.

## C/C++-specific gotchas

1. ccache provides 5-10x speedup on incremental builds — always enable it in CI.
2. Use `-DCMAKE_EXPORT_COMPILE_COMMANDS=ON` for clang-tidy; it needs the exact compiler invocations.
3. Run ASan and UBSan in a **separate job** from normal tests — sanitizer builds are 2-3x slower.
4. Don't combine ASan with coverage flags — they conflict. Use separate build configurations.
5. Set `ASAN_OPTIONS=detect_leaks=1` and `UBSAN_OPTIONS=print_stacktrace=1` for better diagnostics.
6. For header-only libraries, generate coverage only for the test binary, not system headers (`--filter src/`).

## Sources

- https://github.com/hendrikmuhs/ccache-action
- https://gcovr.com/en/stable/
- https://clang.llvm.org/extra/clang-tidy/
