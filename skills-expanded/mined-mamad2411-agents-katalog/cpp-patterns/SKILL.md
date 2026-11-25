---
name: cpp-patterns
description: "When to activate: C++, modern C++23, RAII, smart pointers, move semantics, concepts, ranges, structured bindings, value semantics"
origin: zakr
metadata:
  namespace: zakr/devtools-pack
  version: 1.0.0
  category: engineering
  language: cpp
  platforms: [claude-code, codex, gemini-cli, cursor, aider, windsurf]
---
# Modern C++ Patterns

## RAII

```cpp
// Resource lifetime tied to object lifetime
class FileHandle {
    FILE* fp_;
public:
    explicit FileHandle(const char* path, const char* mode)
        : fp_(std::fopen(path, mode)) {
        if (!fp_) throw std::system_error(errno, std::generic_category());
    }
    ~FileHandle() { if (fp_) std::fclose(fp_); }
    FileHandle(const FileHandle&) = delete;
    FileHandle& operator=(const FileHandle&) = delete;
    FileHandle(FileHandle&& o) noexcept : fp_(std::exchange(o.fp_, nullptr)) {}
    FILE* get() const noexcept { return fp_; }
};
```

## Smart Pointers

```cpp
// unique_ptr — sole ownership
auto buf = std::make_unique<std::byte[]>(1024);
auto obj = std::make_unique<Widget>(42);

// shared_ptr — shared ownership
auto shared = std::make_shared<Config>();
std::weak_ptr<Config> weak = shared; // no ownership, no cycle

// Custom deleter
auto mapped = std::unique_ptr<void, decltype(&munmap)>(
    mmap(nullptr, size, PROT_READ, MAP_SHARED, fd, 0), munmap);
```

## Move Semantics

```cpp
class Buffer {
    std::byte* data_;
    std::size_t size_;
public:
    Buffer(std::size_t n) : data_(new std::byte[n]), size_(n) {}
    ~Buffer() { delete[] data_; }

    // Move constructor: steal resources
    Buffer(Buffer&& o) noexcept
        : data_(std::exchange(o.data_, nullptr))
        , size_(std::exchange(o.size_, 0)) {}

    // Move assignment
    Buffer& operator=(Buffer&& o) noexcept {
        if (this != &o) {
            delete[] data_;
            data_ = std::exchange(o.data_, nullptr);
            size_ = std::exchange(o.size_, 0);
        }
        return *this;
    }
};
```

## Concepts (C++20)

```cpp
template<typename T>
concept Numeric = std::integral<T> || std::floating_point<T>;

template<Numeric T>
T clamp(T value, T lo, T hi) {
    return std::max(lo, std::min(value, hi));
}

// Concept for range-like types
template<typename R>
concept StringRange = std::ranges::input_range<R>
    && std::same_as<std::ranges::range_value_t<R>, std::string>;
```

## Ranges (C++20)

```cpp
#include <ranges>
#include <algorithm>

std::vector<int> nums = {1, 5, 2, 8, 3, 7};

// Pipeline with views (lazy, zero-copy)
auto result = nums
    | std::views::filter([](int n) { return n > 3; })
    | std::views::transform([](int n) { return n * 2; })
    | std::views::take(3);

// Collect to vector
std::vector<int> out(result.begin(), result.end());

// C++23: std::ranges::to
auto vec = nums | std::views::filter([](int n){ return n%2==0; })
                | std::ranges::to<std::vector>();
```

## Structured Bindings

```cpp
// With tuple/pair
auto [min, max] = std::minmax({3, 1, 4, 1, 5, 9});

// With struct (C++17)
struct Point { double x, y; };
auto [x, y] = Point{1.0, 2.0};

// With map iteration
std::map<std::string, int> scores;
for (auto& [name, score] : scores) {
    score += 10; // modifiable reference
}
```

## Error Handling with std::expected (C++23)

```cpp
#include <expected>

std::expected<int, std::string> parse_int(std::string_view s) {
    try {
        return std::stoi(std::string(s));
    } catch (...) {
        return std::unexpected(std::format("Invalid integer: '{}'", s));
    }
}

auto result = parse_int("42");
if (result) std::cout << *result;
else        std::cerr << result.error();

// Chaining
auto doubled = parse_int(input)
    .transform([](int n) { return n * 2; })
    .value_or(0);
```

## Deduction Guides

```cpp
// C++17: class template argument deduction
std::vector v = {1, 2, 3};       // vector<int>
std::pair   p = {42, "hello"s};  // pair<int, string>
std::lock_guard lk{mutex_};       // lock_guard<mutex>
```
