---
name: cpp-style-ref
description: "C++ coding style reference. Select the appropriate reference based on the project build system: xmake projects use references-xmake (C++20 modules), CMake + vcpkg projects use references-cmake-vcpkg (.hpp/.cpp). Applies when writing or reviewing C++ code, naming identifiers, organizing modules or headers, or when the user mentions C++ style."
---

# cpp-style-ref

C++ coding style reference. Select the appropriate reference directory based on the project build system:

- **xmake** → `references-xmake/` (C++20 modules, `.cppm` / `.cpp`)
- **CMake + vcpkg** → `references-cmake-vcpkg/` (traditional headers, `.hpp` / `.cpp`)

## Quick Reference

### Naming

| Category          | Style         | Examples                         |
| ----------------- | ------------- | -------------------------------- |
| Types/Classes     | PascalCase    | `StyleRef`, `HttpServer`         |
| Objects/Members   | snake_case    | `file_name`, `config_text`       |
| Public functions  | PascalCase    | `LoadConfigFile()`, `Parse()`    |
| Private functions | camelCase     | `loadConfigFile()`, `parse()`    |
| Free functions    | snake_case    | `load_config_file()`, `parse_()` |
| Private members   | `m_` prefix   | `m_file_name`, `m_config_text`   |
| Constants         | UPPER_SNAKE   | `MAX_SIZE`, `DEFAULT_TIMEOUT`    |
| Globals           | `g_` prefix   | `g_style_ref`                    |
| Statics           | `s_` prefix   | `s_style_ref`                    |
| Namespaces        | all lowercase | `mcpplibs`, `mylib`              |
| Nested namespaces | all lowercase | `mcpp::style_ref`, `mcpp::utils` |
| Enums             | PascalCase    | `enum class StyleRef { ... };`   |

### Build Systems

- **xmake** — native C++20 module support, uses `.cppm` / `.cpp` (see `references-xmake/`)
- **CMake + vcpkg** — traditional header organization, uses `.hpp` / `.cpp` (see `references-cmake-vcpkg/`)

### Module Basics

- Use `import std` instead of `#include <print>` and `#include <xxx>`
- Use `.cppm` for module interfaces; use `.cpp` for separated implementations
- `export module module_name;` — module declaration
- `export import :partition;` — export partition
- `import :partition;` — internal partition (not exported)

### Module Structure

```
// .cppm
export module a;

export import a.b;
export import :a2;   // exportable partition

import std;
import :a1;          // internal partition
```

### Module Naming

- Modules: `topdir.subdir.filename` (e.g., `a.b`, `a.c`)
- Partitions: `module_name:partition` (e.g., `a:a1`, `a.b:b1`)
- Use directory paths to distinguish identical names: `a/c.cppm` → `a.c`, `b/c.cppm` → `b.c`

### Class Layout

```cpp
class StyleRef {
private:
    std::string m_file_name;  // data members with m_ prefix

public:  // Big Five
    StyleRef() = default;
    StyleRef(const StyleRef&) = default;
    // ...

public:  // public interface
    void LoadConfigFile(std::string file_name);  // PascalCase function, snake_case parameter

private:
    void loadConfigFile(std::string config);  // camelCase for private functions
};
```

### Practice Rules

- **Initialization**: use `{}` — `int n { 42 }`, `std::vector<int> v { 1, 2, 3 }`
- **Strings**: use `std::string_view` for read-only parameters
- **Errors**: use `std::optional` / `std::expected` instead of int error codes
- **Memory**: use `std::unique_ptr`, `std::shared_ptr`; avoid raw `new`/`delete`
- **RAII**: bind resources to object lifetimes
- **auto**: use for iterators, lambdas, complex types; keep explicit types when intent clarity matters
- **Macros**: prefer `constexpr`, `inline`, `concept` over macros

### Interface and Implementation

Both styles are supported.

**Style A: Combined** — interface and implementation in a single `.cppm`:

```cpp
// mylib.cppm
export module mylib;

export auto add(int a, int b) -> int {
    return a + b;
}
```

**Style B: Separated** — interface in `.cppm`, implementation in `.cpp` (hides implementation at compile time):

```cpp
// error.cppm (interface)
export module error;

export struct Error {
    void test();
};
```

```cpp
// error.cpp (implementation)
module error;

import std;

auto Error::test() -> void {
    std::println("Hello");
}
```

Use Style A for simple modules; use Style B when hiding implementation or reducing compile dependencies.

## Applicable Scenarios

- Writing new C++ code (modules `.cppm`/`.cpp` or headers `.hpp`/`.cpp`)
- Reviewing or refactoring C++ code in a project
- When the user asks about "C++ style", "module C++ style", or "modern C++ conventions"

## Limitations

For existing projects, this skill does not apply unless the user explicitly requests format changes. Do not proactively apply this style to existing code or suggest renames/refactoring.
