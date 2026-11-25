---
name: swift-generics
description: "When to activate: Swift generics, type constraints, where clauses, generic algorithms, type erasure, conditional conformance"
origin: zakr
metadata:
  namespace: zakr/devtools-pack
  version: 1.0.0
  category: engineering
  language: swift
  platforms: [claude-code, codex, gemini-cli, cursor, aider, windsurf]
---

# Swift Generics

## Generic Functions

```swift
// Generic function with type constraint
func max<T: Comparable>(_ a: T, _ b: T) -> T {
    a >= b ? a : b
}

// Multiple constraints
func sortedUnique<T: Comparable & Hashable>(_ items: [T]) -> [T] {
    Array(Set(items)).sorted()
}

// Where clause for complex constraints
func zip<A: Collection, B: Collection>(
    _ a: A, _ b: B
) -> [(A.Element, B.Element)] where A.Index == B.Index {
    zip(a.indices, b.indices).map { (a[$0.0], b[$0.1]) }
}
```

## Generic Types

```swift
struct Stack<Element> {
    private var storage: [Element] = []

    mutating func push(_ element: Element) { storage.append(element) }

    mutating func pop() -> Element? { storage.popLast() }

    var top: Element? { storage.last }

    var isEmpty: Bool { storage.isEmpty }
}

// Conditional conformance — only Equatable when Element is
extension Stack: Equatable where Element: Equatable {}

// Usage
var stack = Stack<Int>()
stack.push(1)
stack.push(2)
print(stack.pop())  // Optional(2)
```

## Type Erasure

```swift
// Erase specific type behind AnyPublisher / AnyHashable pattern
struct AnyRepository<Entity: Identifiable>: Repository {
    private let _findAll: () async throws -> [Entity]
    private let _find:    (Entity.ID) async throws -> Entity?
    private let _save:    (Entity) async throws -> Void
    private let _delete:  (Entity) async throws -> Void

    init<R: Repository>(_ repository: R) where R.Entity == Entity {
        _findAll = repository.findAll
        _find    = repository.find
        _save    = repository.save
        _delete  = repository.delete
    }

    func findAll() async throws -> [Entity]         { try await _findAll() }
    func find(id: Entity.ID) async throws -> Entity? { try await _find(id) }
    func save(_ entity: Entity) async throws         { try await _save(entity) }
    func delete(_ entity: Entity) async throws       { try await _delete(entity) }
}
```

## Generic Algorithms Over Collections

```swift
extension Collection {
    // Safe subscript — returns nil instead of crashing
    subscript(safe index: Index) -> Element? {
        indices.contains(index) ? self[index] : nil
    }
}

extension Sequence {
    // Group by a key
    func grouped<Key: Hashable>(by keyPath: KeyPath<Element, Key>) -> [Key: [Element]] {
        reduce(into: [:]) { result, element in
            result[element[keyPath: keyPath], default: []].append(element)
        }
    }
}

// Usage
let grouped = articles.grouped(by: \.author.id)
```

## Result Builders (DSL)

```swift
@resultBuilder
struct ArrayBuilder<T> {
    static func buildBlock(_ components: [T]...) -> [T] {
        components.flatMap { $0 }
    }
    static func buildExpression(_ expression: T) -> [T] { [expression] }
    static func buildOptional(_ component: [T]?) -> [T] { component ?? [] }
    static func buildEither(first component: [T]) -> [T]  { component }
    static func buildEither(second component: [T]) -> [T] { component }
}

func makeItems(@ArrayBuilder<String> builder: () -> [String]) -> [String] {
    builder()
}

let items = makeItems {
    "Apple"
    "Banana"
    if includeOrange { "Orange" }
}
```

## Phantom Types

```swift
// Use phantom types to encode state in the type system
struct ID<T> { let value: UUID }

struct User {}
struct Order {}

// These types are incompatible — compiler prevents mixing
let userID: ID<User>  = ID(value: UUID())
let orderID: ID<Order> = ID(value: UUID())

// func findUser(id: ID<Order>) — compile error, catches bugs at zero runtime cost
func findUser(id: ID<User>) -> User? { ... }
```

## Common Anti-Patterns

- **Overusing `Any` or `AnyObject`** — use generics to preserve type information
- **Type erasure for everything** — only erase when you genuinely need heterogeneous storage
- **Unconstrained generics** — add constraints (`Sendable`, `Codable`, etc.) to catch bugs early
- **Complex `where` clauses in public API** — simplify with typealiases or protocol inheritance
- **`@discardableResult` on generic functions** — only suppress the warning if callers legitimately ignore the return
