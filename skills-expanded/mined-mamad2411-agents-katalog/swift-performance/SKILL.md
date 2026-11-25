---
name: swift-performance
description: "When to activate: Swift performance optimization, value types, COW, ARC, Instruments profiling, memory layout, compile-time optimization"
origin: zakr
metadata:
  namespace: zakr/devtools-pack
  version: 1.0.0
  category: engineering
  language: swift
  platforms: [claude-code, codex, gemini-cli, cursor, aider, windsurf]
---

# Swift Performance Patterns

## Value Type Performance — Copy-on-Write

Swift standard library containers (Array, Dictionary, String) use COW automatically.
Implement COW for your own types when they wrap heap-allocated storage.

```swift
final class Storage<T> {
    var elements: [T]
    init(_ elements: [T] = []) { self.elements = elements }
    func copy() -> Storage<T> { Storage(elements) }
}

struct MyArray<T> {
    private var storage = Storage<T>()

    mutating func append(_ element: T) {
        // Only copy if another owner has a reference
        if !isKnownUniquelyReferenced(&storage) {
            storage = storage.copy()
        }
        storage.elements.append(element)
    }

    var count: Int { storage.elements.count }
}
```

## ARC and Retain Cycle Prevention

```swift
// Avoid retain cycles with [weak self]
class DataLoader {
    var onCompletion: (() -> Void)?

    func load() {
        fetchData { [weak self] result in   // not [unowned] unless certain lifetime
            guard let self else { return }
            self.process(result)
            self.onCompletion?()
        }
    }
}

// Value types don't participate in ARC — prefer structs for hot data
struct Particle {   // no heap allocation, no reference counting
    var position: SIMD3<Float>
    var velocity: SIMD3<Float>
    var mass: Float
}
```

## SIMD for Numerical Work

```swift
import simd

// Process 4 floats in parallel using SIMD
func computeDistances(points: [SIMD2<Float>], from origin: SIMD2<Float>) -> [Float] {
    points.map { point in
        let delta = point - origin
        return sqrt(simd_dot(delta, delta))
    }
}

// Matrix math with simd
let transform = float4x4(translation: [1, 2, 3])
let position = SIMD4<Float>(1, 0, 0, 1)
let transformed = transform * position
```

## Optimizing Collections

```swift
// Reserve capacity for known sizes
var results = [Item]()
results.reserveCapacity(expectedCount)

// Use ContiguousArray for non-class element types (avoids bridging overhead)
var numbers = ContiguousArray<Int>()

// Use lazy for chained transformations that may short-circuit
let firstMatch = items.lazy.filter { $0.isValid }.map { $0.value }.first

// Prefer in-place mutation over creating new collections
items.sort()             // faster than: items = items.sorted()
items.removeAll { !$0.isValid }
```

## Whole-Module Optimization

```swift
// Package.swift: enable WMO for release builds
swiftSettings: [
    .unsafeFlags(["-whole-module-optimization"], .when(configuration: .release)),
]
```

## Instruments Profiling Workflow

1. **Time Profiler** — identify CPU hotspots
2. **Allocations** — find unexpected heap allocation in tight loops
3. **Leaks** — detect reference cycles
4. **SwiftUI** — use SwiftUI instrument to find redundant view updates

```swift
// Mark performance-sensitive paths for Instruments
os_signpost(.begin, log: .default, name: "ProcessBatch")
defer { os_signpost(.end, log: .default, name: "ProcessBatch") }
processBatch(items)
```

## Compile-Time Performance

```swift
// Break complex type inference for the compiler
// Bad — compiler may time out on complex expressions
let result = items
    .filter { $0.isValid }
    .map { $0.transform() }
    .reduce(0) { $0 + $1.score }

// Good — explicit intermediate types reduce inference work
let valid: [Item]    = items.filter { $0.isValid }
let transformed: [T] = valid.map { $0.transform() }
let total: Int       = transformed.reduce(0) { $0 + $1.score }
```

## Memory Layout Optimization

```swift
// Check struct memory layout
print(MemoryLayout<Particle>.size)      // bytes used
print(MemoryLayout<Particle>.stride)    // bytes including padding
print(MemoryLayout<Particle>.alignment) // byte alignment

// Reorder fields to minimize padding (largest to smallest alignment)
// Bad: Bool(1) + padding(7) + Double(8) = 16 bytes
struct Bad  { var flag: Bool; var value: Double }

// Good: Double(8) + Bool(1) + padding(7) = 16 bytes (same but intentional)
// Even better: group same-size fields together
struct Good { var value: Double; var score: Float; var flag: Bool; var kind: UInt8 }
```

## Common Anti-Patterns

- **Classes where structs suffice** — classes add heap allocation + ARC overhead
- **Closure captures in hot loops** — capture values, not references
- **Dynamic dispatch for hot paths** — use `final` or value types to enable static dispatch
- **Large value types** — structs >~16 bytes can be slower to copy; consider class or indirect enum
- **Profiling debug builds** — always profile release builds with `-O` optimizations
