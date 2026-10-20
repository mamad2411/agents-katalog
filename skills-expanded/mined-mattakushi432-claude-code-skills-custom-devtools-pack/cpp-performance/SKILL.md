---
name: cpp-performance
description: "When to activate: C++ performance, profiling, cache, SIMD, branch prediction, LTO, PGO, perf, vtune, benchmarking, optimization"
origin: zakr
metadata:
  namespace: zakr/devtools-pack
  version: 1.0.0
  category: engineering
  language: cpp
  platforms: [claude-code, codex, gemini-cli, cursor, aider, windsurf]
---
# C++ Performance Patterns

## Profiling Tools

```bash
# Linux perf — low overhead sampling
perf record -g ./app && perf report

# Valgrind/Callgrind — detailed call graph
valgrind --tool=callgrind ./app
kcachegrind callgrind.out.*

# Google Benchmark — microbenchmarks
# Intel VTune — hardware counter analysis (microarchitecture bottlenecks)
# Instruments (macOS) — sampling profiler with call tree
```

## Google Benchmark Micro-benchmarks

```cpp
#include <benchmark/benchmark.h>

static void BM_VectorSum(benchmark::State& state) {
    std::vector<int> v(state.range(0));
    std::iota(v.begin(), v.end(), 0);
    for (auto _ : state) {
        benchmark::DoNotOptimize(std::reduce(v.begin(), v.end()));
    }
    state.SetItemsProcessed(state.iterations() * state.range(0));
}
BENCHMARK(BM_VectorSum)->Range(64, 1 << 16);
BENCHMARK_MAIN();
```

## Cache-Friendly Data Layouts

```cpp
// BAD: Array of Structs (AoS) — poor spatial locality for partial access
struct Particle { float x, y, z, vx, vy, vz, mass; };
std::vector<Particle> particles(N);

// GOOD: Struct of Arrays (SoA) — vectorizer-friendly
struct Particles {
    std::vector<float> x, y, z, vx, vy, vz, mass;
};

// Hot/cold data split — keep frequently accessed data together
struct Entity {
    // Hot data (accessed every frame)
    float x, y, z;
    uint32_t flags;
    // Cold data (accessed rarely) — store separately or via pointer
    std::string name;
    std::vector<std::string> tags;
};
```

## SIMD Intrinsics (x86)

```cpp
#include <immintrin.h>

// AVX2: process 8 floats at once
void add_arrays(const float* a, const float* b, float* out, int n) {
    int i = 0;
    for (; i <= n - 8; i += 8) {
        __m256 va = _mm256_loadu_ps(a + i);
        __m256 vb = _mm256_loadu_ps(b + i);
        _mm256_storeu_ps(out + i, _mm256_add_ps(va, vb));
    }
    for (; i < n; ++i) out[i] = a[i] + b[i];  // scalar remainder
}
// Prefer auto-vectorization first; use intrinsics only when profiling shows need
```

## Compiler Flags for Performance

```cmake
# Release build flags
target_compile_options(myapp PRIVATE
    -O3                    # aggressive optimization
    -march=native          # target current CPU (AVX2, etc.)
    -flto                  # Link-Time Optimization
    -fno-exceptions        # if exceptions not used
    -fno-rtti              # if RTTI not used
)

# Profile-Guided Optimization (PGO)
# Step 1: Instrument build
# -fprofile-generate
# Step 2: Run with representative workload
# Step 3: Optimize with profile
# -fprofile-use
```

## Branch Prediction Hints

```cpp
// C++20 [[likely]] / [[unlikely]]
if (ptr == nullptr) [[unlikely]] {
    handle_error();
    return;
}
// Hot path continues here

// Avoid branch misprediction in tight loops
// BAD: branch inside loop
for (int i = 0; i < N; ++i)
    if (data[i] > 0) sum += data[i];

// BETTER: branchless
for (int i = 0; i < N; ++i)
    sum += data[i] * (data[i] > 0);
```

## Move Semantics and RVO

```cpp
// Return Value Optimization (RVO) — compiler elides copy automatically
std::vector<int> make_data(int n) {
    std::vector<int> v(n);
    std::iota(v.begin(), v.end(), 0);
    return v;  // NRVO — no copy
}

// Pass sink arguments by value (enables move)
class Builder {
    std::string name_;
public:
    Builder& set_name(std::string name) {
        name_ = std::move(name);  // move if caller passes rvalue
        return *this;
    }
};
```
