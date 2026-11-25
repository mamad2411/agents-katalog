---
name: stl-patterns
description: "When to activate: STL, standard library, containers, algorithms, iterators, ranges, views, vector, map, unordered_map, string_view"
origin: zakr
metadata:
  namespace: zakr/devtools-pack
  version: 1.0.0
  category: engineering
  language: cpp
  platforms: [claude-code, codex, gemini-cli, cursor, aider, windsurf]
---
# C++ STL Patterns

## Container Selection

| Need | Container | Notes |
|---|---|---|
| Dynamic array | `std::vector` | Cache-friendly, O(1) amortized push_back |
| Sorted unique keys | `std::set` | O(log n), ordered |
| Fast lookup | `std::unordered_map` | O(1) avg, needs hashable key |
| FIFO | `std::queue` | deque-backed |
| Priority queue | `std::priority_queue` | max-heap by default |
| Fixed-size | `std::array<T,N>` | Stack-allocated, zero overhead |

## Algorithms

```cpp
#include <algorithm>
#include <numeric>
#include <ranges>

std::vector<int> v = {5, 3, 1, 4, 2};

std::ranges::sort(v);
std::ranges::sort(v, std::greater{});  // descending

auto it = std::ranges::find(v, 3);
bool found = std::ranges::binary_search(v, 3);

int sum = std::reduce(v.begin(), v.end(), 0);

// C++20 erase_if
std::erase_if(v, [](int x) { return x % 2 == 0; });
```

## C++20 Ranges / Views (Lazy)

```cpp
auto result = nums
    | std::views::filter([](int x) { return x % 2 == 0; })
    | std::views::transform([](int x) { return x * x; })
    | std::views::take(3);

auto reversed = nums | std::views::reverse;
auto iota     = std::views::iota(1, 11);   // 1..10
auto keys     = mymap | std::views::keys;
```

## String Patterns

```cpp
// string_view for read-only args (zero copy)
void process(std::string_view sv) {
    auto pos = sv.find('.');
    auto ext = sv.substr(pos + 1);
}

// C++20 formatting
#include <format>
auto msg = std::format("User {} at {}", name, ts);
```

## Custom Hash for Unordered Containers

```cpp
struct Point { int x, y; };
struct PointHash {
    std::size_t operator()(const Point& p) const {
        return std::hash<int>{}(p.x) ^ (std::hash<int>{}(p.y) << 1);
    }
};
std::unordered_map<Point, int, PointHash> grid;
```

## Performance Tips

```cpp
v.reserve(1000);               // avoid reallocations
v.emplace_back(42);            // construct in-place

// find before [] to avoid unintended insert
if (auto it = m.find(key); it != m.end()) use(it->second);

// Sort by member projection (C++20)
std::ranges::sort(data, {}, &Pair::first);
```
