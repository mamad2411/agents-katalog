# Modern C++ Engineering & Zero-Defect Safety Contract

## 1. Purpose
Author, refactor, and verify mission-critical, high-performance systems software adhering to modern **C++20** and **C++23** standards. This skill enforces strict Resource Acquisition Is Initialization (RAII), the Rule of Zero/Five, lifetime and boundary safety, eradication of raw pointer arithmetic and naked manual memory management, zero-warning compilation with `-Werror`, and mandatory sanitization via AddressSanitizer (ASan), UndefinedBehaviorSanitizer (UBSan), and ThreadSanitizer (TSan).

---

## 2. Use When
- Developing, refactoring, or optimizing native C++ engines, low-level runtime systems, GPU backends, or desktop infrastructure.
- Interfacing with OS system calls, memory-mapped files, hardware abstraction layers, or high-throughput concurrency primitives.
- Upgrading legacy C++ (C++98/C++03/C++11/C++14/C++17) codebases to modern C++20/C++23 idioms.
- Writing unit tests and benchmarks using Catch2, GoogleTest, or Boost.UT with sanitizer integration.
- Operating in mode(s): `implementation`, `review`, `testing`, `audit`.

---

## 3. Do Not Use When
- The project is purely implemented in C (use `lang-c`), Rust (use `lang-rust`), or Go (use `lang-go`).
- The task is constrained to high-level web frontend logic without WebAssembly/C++ compilation.
- The user explicitly requires legacy dialect compliance (e.g. strict C++98 compatibility) without permitting modern safety abstractions.

---

## 4. Required Context
Before writing or modifying C++ code, determine:
- **Language Standard**: Strict C++20 (`-std=c++20`) or C++23 (`-std=c++23`).
- **Compiler Toolchain**: Clang 16+ or GCC 13+ with standard library implementation (libc++ / libstdc++).
- **Error Handling Strategy**: Zero-exception systems (`-fno-exceptions` with `std::expected<T, E>` / `std::optional<T>`) vs standard exception hierarchy (`std::system_error`).
- **Memory & Concurrency Model**: Cache line alignment requirements (`std::hardware_destructive_interference_size`), atomic memory orderings (`std::memory_order_relaxed/acquire/release/seq_cst`).

---

## 5. Procedure

```
[Design / API Contract]
         |
         v
[1. Static Typing & Concepts] ------> Enforce template constraints via `requires`
         |
         v
[2. RAII & Ownership Topology] -----> Rule of Zero/Five, unique_ptr, span views
         |
         v
[3. Fallible Operations Design] ----> Return std::expected<T, E> (no raw errnos)
         |
         v
[4. Static Analysis Gate] ----------> clang-tidy (-warnings-as-errors=*), cppcheck
         |
         v
[5. Dynamic Sanitizer Gauntlet] ----> ASan, UBSan, TSan determinism validation
```

### Step 1: Enforce Modern Typing & Concepts
- Constrain all generic templates using C++20 Concepts:
  ```cpp
  template <typename T>
  concept Serializable = requires(T a) {
      { a.serialize() } -> std::same_as<std::span<const std::uint8_t>>;
  };
  ```
- Use `std::span<T>` and `std::string_view` for non-owning contiguous sequences instead of `(const T* ptr, size_t len)`.
- Use `std::byte` instead of `char` or `unsigned char` for raw memory buffers.

### Step 2: Resource Lifecycle & The Rule of Zero
- Adhere strictly to the **Rule of Zero**: let smart resource wrappers (`std::unique_ptr`, `std::vector`, `std::string`) handle lifetime semantics automatically.
- When custom resource handles are required (e.g., POSIX `fd`, `VkDeviceMemory`), implement the **Rule of Five**: destructor, copy constructor, copy assignment operator, move constructor, and move assignment operator (deleting copy if resource is unique).
- Naked `new`, `delete`, `malloc`, and `free` are strictly forbidden. Use `std::make_unique<T>()` or custom arena allocators.

### Step 3: Explicit Error Handling without Leaks
- For fallible operations, return `std::expected<Value, Error>` (C++23) or a monadic `std::optional<T>`:
  ```cpp
  auto read_config(const std::filesystem::path& p) noexcept -> std::expected<Config, ConfigError>;
  ```
- Functions that do not throw must be explicitly qualified with `noexcept` to permit compiler move-elision optimizations.

### Step 4: Concurrency & Atomic Safety
- Guard shared mutable state with `std::scoped_lock` (RAII deadlock avoidance) or `std::shared_lock` for read-heavy workloads.
- Avoid naked atomic flags without specifying explicit memory order:
  - Acquire-Release semantics for producer-consumer pipelines (`std::memory_order_release` upon write, `std::memory_order_acquire` upon read).
  - Explicitly pad atomic counters to prevent false sharing:
    ```cpp
    alignas(std::hardware_destructive_interference_size) std::atomic<std::uint64_t> counter;
    ```

### Step 5: Static Analysis & Dynamic Sanitizer Verification
1. Compile with maximal warning flags:
   `-Wall -Wextra -Wpedantic -Wconversion -Wshadow -Wnon-virtual-dtor -Wold-style-cast -Wcast-align -Wunused -Woverloaded-virtual -Werror`.
2. Run Clang-Tidy:
   `clang-tidy --checks="modernize-*,readability-*,bugprone-*,performance-*,cppcoreguidelines-*" --warnings-as-errors=*`.
3. Execute test suite with ASan/UBSan:
   `-fsanitize=address,undefined -fno-omit-frame-pointer`.
4. Execute concurrent tests with TSan:
   `-fsanitize=thread`.

---

## 6. Decision Rules & Invariants
- **RULE 1 (Zero Naked Ownership)**: Naked pointers (`T*`) can only exist as non-owning, nullable references. They must never be deleted, created via `new`, or subjected to arithmetic.
- **RULE 2 (No C-Style Casts)**: C-style casts `(type)val` and raw `reinterpret_cast` are strictly prohibited. Use `static_cast`, `std::bit_cast` (for bitwise reinterpretation), or type-safe std variants.
- **RULE 3 (constexpr by Default)**: Any computation, lookup table, or string formatting computable at compile time must be qualified with `constexpr` or `consteval`.
- **RULE 4 (Explicit Ownership Transfer)**: Pass sink parameters by value and `std::move()` into place; pass non-sink parameters by `const&` or non-owning view (`std::string_view`, `std::span`).

---

## 7. Evidence Required
- **Compiler Evidence**: Clean compilation under `-std=c++20` or `-std=c++23` with `-Werror`.
- **Static Analysis Evidence**: Zero diagnostic errors reported by `clang-tidy` and `cppcheck`.
- **Sanitizer Evidence**: Zero memory leaks, out-of-bounds reads/writes, or undefined behavior diagnostics under ASan and UBSan test runs.

---

## 8. Output Contract
- High-integrity C++ headers (`.hpp`) and implementation files (`.cpp`).
- Build configuration (`CMakeLists.txt` or `Meson`) enforcing compiler flags and sanitizer presets.
- C++ Verification Report (`templates/cpp-verification-report.md`) detailing sanitizer results.

---

## 9. Stop Conditions
- All tests pass cleanly under both ASan/UBSan and TSan builds.
- Clang-tidy static analysis produces zero warnings.
- Token budget exhausted.
- Blocked on missing hardware / SDK dependency.

---

## 10. Escalation Rules
- Escalate immediately if an unavoidable third-party C library dependency violates strict aliasing or memory safety.
- Escalate to systems architect if ABI compatibility constraints conflict with modern C++20 standard library updates.
