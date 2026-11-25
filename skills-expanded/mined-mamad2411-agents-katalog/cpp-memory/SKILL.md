---
name: cpp-memory
description: "When to activate: smart pointers, unique_ptr, shared_ptr, weak_ptr, memory management, custom allocators, RAII, memory leaks, heap, stack, pmr"
origin: zakr
metadata:
  namespace: zakr/devtools-pack
  version: 1.0.0
  category: engineering
  language: cpp
  platforms: [claude-code, codex, gemini-cli, cursor, aider, windsurf]
---
# C++ Memory Management Patterns

## Smart Pointer Ownership Model

```cpp
// unique_ptr: sole ownership, zero overhead
std::unique_ptr<Widget> make_widget(int id) {
    return std::make_unique<Widget>(id);  // never use new directly
}

// Transfer ownership
auto w1 = make_widget(1);
auto w2 = std::move(w1);  // w1 is now nullptr

// shared_ptr: shared ownership with ref counting
std::shared_ptr<Config> cfg = std::make_shared<Config>("app.json");
auto cfg2 = cfg;  // ref count = 2

// weak_ptr: break cycles, observer pattern
class Node {
    std::shared_ptr<Node> next;
    std::weak_ptr<Node> prev;  // avoid cycle
};

// Observe without extending lifetime
std::weak_ptr<Widget> observer = shared_widget;
if (auto locked = observer.lock()) {
    locked->draw();  // safe to use
}
```

## RAII: Resource Acquisition Is Initialization

```cpp
class FileHandle {
    FILE* handle_;
public:
    explicit FileHandle(const char* path, const char* mode)
        : handle_(std::fopen(path, mode)) {
        if (!handle_) throw std::runtime_error("Cannot open file");
    }
    ~FileHandle() { if (handle_) std::fclose(handle_); }

    FileHandle(const FileHandle&) = delete;
    FileHandle& operator=(const FileHandle&) = delete;
    FileHandle(FileHandle&& o) noexcept : handle_(std::exchange(o.handle_, nullptr)) {}
    FileHandle& operator=(FileHandle&& o) noexcept {
        if (this != &o) {
            if (handle_) std::fclose(handle_);
            handle_ = std::exchange(o.handle_, nullptr);
        }
        return *this;
    }
    FILE* get() const { return handle_; }
};
```

## Custom Deleters

```cpp
// unique_ptr with custom deleter for C APIs
auto buf = std::unique_ptr<uint8_t[], decltype(&std::free)>(
    static_cast<uint8_t*>(std::malloc(1024)), std::free);

// Lambda deleter
auto conn = std::unique_ptr<PGconn, decltype(&PQfinish)>(
    PQconnectdb("host=localhost"), PQfinish);

// Shared deleter for mapped memory
auto mapped = std::shared_ptr<void>(
    mmap(nullptr, size, PROT_READ, MAP_PRIVATE, fd, 0),
    [size](void* p) { munmap(p, size); });
```

## Memory Arenas / Pool Allocators

```cpp
// Simple arena allocator
class Arena {
    std::vector<std::byte> buffer_;
    std::size_t offset_ = 0;
public:
    explicit Arena(std::size_t size) : buffer_(size) {}

    void* alloc(std::size_t n, std::size_t align = alignof(std::max_align_t)) {
        auto ptr = reinterpret_cast<uintptr_t>(buffer_.data() + offset_);
        auto aligned = (ptr + align - 1) & ~(align - 1);
        auto new_offset = (aligned - reinterpret_cast<uintptr_t>(buffer_.data())) + n;
        if (new_offset > buffer_.size()) return nullptr;
        offset_ = new_offset;
        return reinterpret_cast<void*>(aligned);
    }
    void reset() { offset_ = 0; }
};

// C++17 std::pmr polymorphic allocators
#include <memory_resource>

std::array<std::byte, 4096> buf;
std::pmr::monotonic_buffer_resource pool(buf.data(), buf.size());
std::pmr::vector<std::pmr::string> v(&pool);  // no heap allocation
```

## Detecting Memory Issues

```bash
# AddressSanitizer (ASan) — catches use-after-free, heap overflow, leaks
g++ -fsanitize=address,undefined -g -O1 -o app main.cpp

# Valgrind — comprehensive leak detection
valgrind --leak-check=full --show-leak-kinds=all --track-origins=yes ./app

# LeakSanitizer standalone
g++ -fsanitize=leak -g -o app main.cpp
```

## Stack vs Heap Guidelines

| Scenario | Recommendation |
|---|---|
| Small, fixed-size, local | Stack |
| Large buffers (>~1MB) | Heap via `unique_ptr` |
| Shared ownership | `shared_ptr` |
| Optional / nullable | `unique_ptr` or `std::optional` |
| Performance-critical hot path | Arena/pool allocator |
| C API resource | `unique_ptr` with custom deleter |

## Common Anti-patterns

```cpp
// BAD: raw owning pointer
Widget* w = new Widget();  // who deletes?

// GOOD: unique_ptr
auto w = std::make_unique<Widget>();

// BAD: shared_ptr everywhere (ref cycles, overhead)
// GOOD: unique_ptr by default, shared_ptr only for genuine shared ownership

// BAD: dangling reference
std::string& get_name() {
    std::string local = "hello";
    return local;  // UB: reference to destroyed object
}

// BAD: double free — prevented by smart pointers
```
