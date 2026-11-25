---
name: systems-c-cpp
description: "C and modern C++ done safely: RAII and smart pointers, move semantics and the rule of zero, views and their lifetimes, error handling, the undefined behaviour that bites most, CMake with modern targets, warnings as errors, sanitizers, fuzzing, static analysis, tests, ABI stability and portability. Read when writing or reviewing C or C++."
---

# C and modern C++, safely

Default C++ reads like 1998 with `auto`: `new` and `delete` by hand, a
destructor and copy constructor for a class that only holds a
`std::vector`, `const char*` everywhere, return codes ignored, warnings
off, a crash on a string one byte longer than the test. Default C forgets
a `free` on one error path and calls `sprintf`. This is the version that
survives review, sanitizers and a fuzzer: ownership in types, undefined
behaviour avoided by construction, a build that fails on warnings. Rules
in `systems`, threads in `systems-concurrency`, other languages in
`systems-ffi`.

## 1. Baseline

New C++ targets C++20, C++17 at least; C++23 library pieces
(`std::expected`, `std::print`) only where every CI compiler has them
(test `__cpp_lib_expected`, `__cpp_lib_print`). C: C17, C23 only if all
compilers agree. The project's standard, exception policy, naming, error
scheme and formatting come first.

## 2. Ownership: RAII for every resource

- Every resource (memory, file, socket, lock, C library handle) is owned
  by an object whose destructor releases it. Raw pointers and references
  only observe: `T*` when it may be null, `T&` when it may not.
- `std::unique_ptr<T>` by default (`std::make_unique<T>(...)`);
  `std::shared_ptr` only for truly shared ownership; `std::weak_ptr` for
  back-references and caches, so cycles free. No `new` or `delete`
  outside a class that owns the resource; locks through
  `std::scoped_lock`, never `mutex.lock()` by hand.
- C handles get a deleter. A file you wrote is still closed explicitly
  and checked (`fclose` reports delayed write errors); the deleter is the
  error-path fallback:

```cpp
struct FileCloser {
    void operator()(std::FILE* f) const noexcept { std::fclose(f); }
};
using File = std::unique_ptr<std::FILE, FileCloser>;

File open_file(const char* path, const char* mode) {
    return File{std::fopen(path, mode)};  // null on failure: check before use
}
```

## 3. Rule of zero, then five; moves

- Rule of zero: a class whose members manage themselves (`std::vector`,
  `std::string`, `std::unique_ptr`) declares no destructor, copy or move
  members; most classes. Rule of five: a class managing a resource
  directly declares, or `= delete`s, all five, with `noexcept` moves (or
  `std::vector` copies on growth). A polymorphic base has a virtual or
  protected destructor (`-Wnon-virtual-dtor`).
- `std::move` only casts; assign to or destroy a moved-from object,
  nothing else. `std::move` of a `const` object copies; `return
  std::move(local);` blocks copy elision (`-Wpessimizing-move`).
- Pass `std::string_view` and `std::span<const T>` for read-only views,
  `const T&` for large objects, by value then `std::move` for sinks,
  `std::unique_ptr<T>` by value to hand over ownership.

## 4. Views and their lifetimes

`std::string_view`, `std::span`, iterators, and pointers or references
into containers do not own; they dangle when the owner dies or moves its
storage:

```cpp
std::string_view name = make_name();        // make_name returns std::string: dangles
std::span<const int> v = get_vector();       // same with a temporary vector
auto& first = items[0]; items.push_back(x);  // push_back may reallocate: first dangles
for (auto& c : get_config().items()) {}      // before C++23 (P2718) the temporary dies first
```

- Views are parameters and short-lived locals, not members, unless the
  owner is documented to outlive the object; a `string_view` is not
  null-terminated, so never pass its `.data()` to a C API. A lambda stored
  or run on another thread captures by value or `shared_ptr`, never `[&]`.
- Clang warns on the first two by default (`-Wdangling-gsl`), GCC 13 has
  `-Wdangling-reference`, `[[clang::lifetimebound]]` extends the checks;
  ASan catches the rest at run time.

## 5. Errors

- One written policy per project: exceptions, or none (`-fno-exceptions`).
  Exceptions are thrown by value and caught by `const&`, and nothing
  throws out of a destructor, a C API or a thread function.
- Expected failures as values: `std::expected<T, Error>` (C++23,
  `tl::expected` before), `std::optional<T>` for absent,
  `std::error_code` for system errors, on `[[nodiscard]]` functions;
  `std::variant` with `std::visit` instead of a tag and a union.
- C: an `int` status (0 success, negative error), results through
  pointers, every return value checked (`close`, `fclose` and `snprintf`
  too), `errno` read only right after a failed call.

## 6. C that does not leak or overflow

Ownership in the API (`foo_create`/`foo_destroy`, each pointer documented
as borrowed or taken), and one exit through a cleanup label:

```c
int load_config(const char *path, struct config *out) {
    int rc = -1;
    char *buf = NULL;
    size_t n = 0;
    FILE *f = fopen(path, "rb");
    if (!f) goto out;
    buf = malloc(MAX_CONFIG);
    if (!buf) goto out;
    n = fread(buf, 1, MAX_CONFIG, f);
    if (ferror(f)) goto out;
    rc = parse_config(buf, n, out);
out:
    free(buf);
    if (f) fclose(f);
    return rc;
}
```

- `size_t` for sizes, fixed widths (`uint32_t`) for data formats;
  `calloc(n, size)` checks the product, `malloc(n * size)` does not (C23
  `ckd_mul` or `__builtin_mul_overflow`). `snprintf` with its result
  checked (`n < 0 || (size_t)n >= size` means error or truncation); never
  `sprintf`, `strcpy`, `strcat`, `gets`, or `strncpy` (no terminator).

## 7. The undefined behaviour that bites most

| UB | Typical form | Prevent | Detect |
|---|---|---|---|
| Signed overflow | `len * 4` on `int` | wider type, `ckd_mul` | UBSan |
| Out of bounds | `buf[n]`, `memcpy` past the end | `std::span`, hardened library | ASan |
| Use after free | a view or iterator past its owner | RAII, no stored views | ASan |
| Uninitialised read | `int x; if (c) x = 1; use(x);` | initialise at declaration | MSan, `-Wuninitialized` |
| Strict aliasing | `*(float*)&bits` | `std::bit_cast`, `memcpy` | review |
| Data race | two threads, one writes, no lock | a lock or an atomic | TSan |
| Null dereference | unchecked `malloc` or lookup | check, references | ASan, UBSan |
| Bad shift | `x << 32` on 32 bits, negative count, `1 << 31` in C | unsigned, checked count | UBSan |
| Invalidated iterator | erase or push while iterating | `std::erase_if`, indices | ASan, `-D_GLIBCXX_DEBUG` |
| Missing return | non-void function falls off the end | `-Werror=return-type` | compiler |
| Overlapping `memcpy` | source and destination overlap | `memmove` | ASan |

## 8. CMake with targets

```cmake
cmake_minimum_required(VERSION 3.25)
project(parser VERSION 1.4.0 LANGUAGES CXX)

add_library(project_warnings INTERFACE)
target_compile_options(project_warnings INTERFACE
  "$<$<CXX_COMPILER_ID:GNU,Clang,AppleClang>:-Wall;-Wextra;-Wpedantic;-Wconversion;-Wsign-conversion;-Wshadow;-Wnon-virtual-dtor;-Wold-style-cast>"
  "$<$<CXX_COMPILER_ID:MSVC>:/W4;/permissive-;/utf-8>")

add_library(parser src/parser.cpp)
add_library(parser::parser ALIAS parser)
target_compile_features(parser PUBLIC cxx_std_20)
target_include_directories(parser PUBLIC
  $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
  $<INSTALL_INTERFACE:include>)
target_link_libraries(parser PRIVATE $<BUILD_INTERFACE:project_warnings>)

if(PROJECT_IS_TOP_LEVEL)
  include(CTest)
  add_subdirectory(tests)
endif()
```

- Targets and properties, never global `CMAKE_CXX_FLAGS`,
  `include_directories()` or `add_definitions()`; `PUBLIC` for what
  consumers need, `PRIVATE` for what they do not. A generator expression
  with several flags is quoted and `;`-separated, or CMake splits it.
- Dependencies via `find_package(fmt CONFIG REQUIRED)` and
  `target_link_libraries(parser PRIVATE fmt::fmt)`, supplied by vcpkg
  (`vcpkg.json`) or Conan 2 as the project does; `FetchContent` pinned to
  a commit or a `URL_HASH`.
- Build variants live in a committed `CMakePresets.json` (version 6):
  `dev` (Ninja, Debug, `"binaryDir": "build/${presetName}"`,
  `CMAKE_EXPORT_COMPILE_COMMANDS=ON`), `ci` inheriting it with
  `CMAKE_COMPILE_WARNING_AS_ERROR=ON`, and `asan` with `CMAKE_CXX_FLAGS`
  set to `-fsanitize=address,undefined -fno-omit-frame-pointer
  -fno-sanitize-recover=all`: the one global flag, since every
  translation unit must be instrumented.

## 9. Warnings, hardening, sanitizers

- The CMake warning set plus `-Wformat=2 -Wimplicit-fallthrough
  -Woverloaded-virtual`; errors in CI (`CMAKE_COMPILE_WARNING_AS_ERROR`),
  not forced onto every developer's newer compiler.
- Release hardening (OpenSSF's compiler hardening guide):
  `-D_FORTIFY_SOURCE=3` (glibc, with optimisation), `-D_GLIBCXX_ASSERTIONS`
  or `-D_LIBCPP_HARDENING_MODE=_LIBCPP_HARDENING_MODE_FAST` (libc++ 18+)
  for checked `operator[]`, `-fstack-protector-strong`,
  `-fstack-clash-protection`, `-ftrivial-auto-var-init=zero`, `-fPIE -pie`,
  `-Wl,-z,relro,-z,now`. GCC 14 on Linux bundles these as `-fhardened`.
- Sanitizers in CI test jobs, one build per group (ASan and TSan do not
  combine), with `-g -O1 -fno-omit-frame-pointer`:
  `-fsanitize=address,undefined` (leaks too, on Linux), `-fsanitize=thread`,
  `-fsanitize=memory -fsanitize-memory-track-origins=2` (Clang on Linux,
  every library instrumented). MSVC has `/fsanitize=address`; Apple's
  toolchain has no LeakSanitizer (`leaks --atExit -- ./test` instead).

## 10. Fuzzing

Every parser, decoder and protocol handler fed outside bytes has a fuzz
target, run in CI for minutes and locally for hours:

```cpp
extern "C" int LLVMFuzzerTestOneInput(const std::uint8_t* data, std::size_t size) {
    auto result = parser::parse({data, size});      // takes std::span<const std::uint8_t>
    if (result) (void)parser::serialize(*result);   // exercise the round trip too
    return 0;
}
```

```sh
clang++ -std=c++20 -g -O1 -fsanitize=fuzzer,address,undefined \
  fuzz_parse.cpp src/parser.cpp -Iinclude -o fuzz_parse
./fuzz_parse -max_total_time=600 -max_len=65536 corpus/
```

Apple's clang has no libFuzzer: use Homebrew LLVM or Linux. AFL++
(`afl-clang-fast++`, `afl-fuzz -i seeds -o findings -- ./target @@`) is
the alternative; OSS-Fuzz or ClusterFuzzLite run it continuously. Seed
the corpus with real samples; every crash becomes a regression test.

## 11. Static analysis, formatting, tests

- clang-tidy with a committed `.clang-tidy` (`bugprone-*`, `cert-*`,
  `clang-analyzer-*`, `concurrency-*`, `cppcoreguidelines-*`,
  `modernize-*`, `performance-*`, minus what the team rejects) run on the
  compile database; cppcheck (`--project=compile_commands.json
  --error-exitcode=1`) as a second opinion; GCC's `-fanalyzer` for C;
  clang-format with a committed `.clang-format`, checked in CI.
- Tests in the project's framework (GoogleTest with
  `gtest_discover_tests`, Catch2 v3 with `catch_discover_tests`, doctest)
  under CTest: one per bug fixed, and the edges (empty, maximum, one past).

## 12. ABI stability and portability

- A shared library's ABI breaks when a public class changes size or
  layout, a virtual function is added or reordered, an inline function
  changes, or a signature changes. Keep the surface small: pimpl (a
  `std::unique_ptr<Impl>` member, destructor defined in the `.cpp`), or a
  C API over opaque handles (`systems-ffi`).
- No standard library types across a shared-library boundary between
  different compilers or standard libraries (libstdc++, libc++ and MSVC's
  differ; libstdc++ has two `std::string` ABIs).
- Hidden by default (`CXX_VISIBILITY_PRESET hidden`, an export macro from
  `generate_export_header()`), `VERSION` and `SOVERSION` set, each release
  checked with `abidiff` (libabigail).
- Portability: `<cstdint>` types in interfaces (`long` is 32 bits on
  Windows, 64 on Linux and macOS); `char` is unsigned on Linux on Arm;
  binary files opened `"rb"`/`"wb"`; `NOMINMAX` before `<windows.h>`;
  `std::filesystem::path`; byte order explicit on disk (`systems-formats`).

## Check it

```sh
cmake --preset ci && cmake --build build/ci && ctest --test-dir build/ci --output-on-failure
cmake --preset asan && cmake --build build/asan && ctest --test-dir build/asan --output-on-failure
run-clang-tidy -p build/ci -quiet
git diff --name-only -- '*.c' '*.cc' '*.cpp' '*.h' '*.hpp' | xargs clang-format --dry-run --Werror
```

No new warnings on any CI compiler, sanitizer runs without a report, the
fuzz target run for at least 10 minutes after a parser change. Say which
compilers and sanitizers could not be run here.

## Avoid

Raw `new` and `delete`; `shared_ptr` by default; hand-written copy and
move members where none are needed; views stored past their owner;
`return std::move(local)`; exceptions escaping destructors, threads or a C
API; unchecked return values; `sprintf`, `strcpy`, `strncpy`; `malloc(n *
size)`; type punning through pointer casts; global `CMAKE_CXX_FLAGS`;
warnings off; sanitizers never run; parsers never fuzzed; standard
library types in a stable ABI.
