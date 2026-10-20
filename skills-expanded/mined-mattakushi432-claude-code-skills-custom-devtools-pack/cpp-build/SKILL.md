---
name: cpp-build
description: "When to activate: C++ build, CMake, sanitizers, ASan, UBSan, TSan, clang-tidy, clang-format, vcpkg, Conan, CI, static analysis"
origin: zakr
metadata:
  namespace: zakr/devtools-pack
  version: 1.0.0
  category: engineering
  language: cpp
  platforms: [claude-code, codex, gemini-cli, cursor, aider, windsurf]
---
# C++ Build and Tooling Patterns

## Sanitizers

```bash
# AddressSanitizer: heap/stack overflow, use-after-free, leaks
cmake -DCMAKE_BUILD_TYPE=Debug \
      -DCMAKE_CXX_FLAGS="-fsanitize=address,undefined -g -O1"

# ThreadSanitizer: data races, lock-order violations
cmake -DCMAKE_CXX_FLAGS="-fsanitize=thread -g -O1"

# MemorySanitizer: uninitialized reads (Clang only)
cmake -DCMAKE_CXX_FLAGS="-fsanitize=memory -fPIE -pie -g"

# Note: cannot combine ASan + TSan. Use separate CI jobs.
```

## CMake Sanitizer Preset

```cmake
# CMakePresets.json
{
  "configurePresets": [
    {
      "name": "asan",
      "binaryDir": "build/asan",
      "cacheVariables": {
        "CMAKE_BUILD_TYPE": "Debug",
        "CMAKE_CXX_FLAGS": "-fsanitize=address,undefined -fno-omit-frame-pointer -g"
      }
    },
    {
      "name": "release",
      "binaryDir": "build/release",
      "cacheVariables": {
        "CMAKE_BUILD_TYPE": "Release",
        "CMAKE_INTERPROCEDURAL_OPTIMIZATION": "ON"
      }
    }
  ]
}
```

## clang-tidy Static Analysis

```yaml
# .clang-tidy
Checks: >
  clang-diagnostic-*,
  clang-analyzer-*,
  cppcoreguidelines-*,
  modernize-*,
  performance-*,
  readability-*,
  -modernize-use-trailing-return-type
WarningsAsErrors: "cppcoreguidelines-*"
HeaderFilterRegex: "src/.*"

CheckOptions:
  - key: readability-identifier-naming.ClassCase
    value: CamelCase
  - key: readability-identifier-naming.FunctionCase
    value: lower_case
```

```bash
# Run in CI
cmake -DCMAKE_EXPORT_COMPILE_COMMANDS=ON ..
clang-tidy -p build src/**/*.cpp
```

## clang-format Configuration

```yaml
# .clang-format
BasedOnStyle: Google
IndentWidth: 4
ColumnLimit: 100
AllowShortFunctionsOnASingleLine: Inline
PointerAlignment: Left
SortIncludes: CaseInsensitive
```

```bash
# Format all source files
find src -name "*.cpp" -o -name "*.h" | xargs clang-format -i

# Check in CI (non-destructive)
clang-format --dry-run --Werror src/**/*.cpp
```

## vcpkg Package Manager

```json
// vcpkg.json (manifest mode)
{
  "name": "my-app",
  "version": "1.0.0",
  "dependencies": [
    "fmt",
    "spdlog",
    { "name": "boost-asio", "version>=": "1.82.0" },
    "nlohmann-json",
    "gtest"
  ]
}
```

```cmake
# CMakeLists.txt — vcpkg toolchain handles find_package
find_package(fmt CONFIG REQUIRED)
find_package(spdlog CONFIG REQUIRED)
target_link_libraries(myapp PRIVATE fmt::fmt spdlog::spdlog)
```

## GitHub Actions CI Pipeline

```yaml
name: CI
on: [push, pull_request]

jobs:
  build-test:
    runs-on: ubuntu-24.04
    strategy:
      matrix:
        preset: [debug, asan, release]
    steps:
      - uses: actions/checkout@v4
      - uses: lukka/run-vcpkg@v11

      - name: Configure
        run: cmake --preset ${{ matrix.preset }}

      - name: Build
        run: cmake --build build/${{ matrix.preset }} -j$(nproc)

      - name: Test
        run: ctest --test-dir build/${{ matrix.preset }} --output-on-failure

  static-analysis:
    runs-on: ubuntu-24.04
    steps:
      - uses: actions/checkout@v4
      - run: cmake -B build -DCMAKE_EXPORT_COMPILE_COMMANDS=ON
      - run: clang-tidy -p build $(find src -name "*.cpp")
```

## Conan Package Manager

```python
# conanfile.py
from conan import ConanFile
from conan.tools.cmake import CMakeToolchain, CMake

class MyApp(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    requires = ["fmt/10.1.1", "spdlog/1.12.0", "gtest/1.14.0"]

    def generate(self):
        tc = CMakeToolchain(self)
        tc.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()
```
