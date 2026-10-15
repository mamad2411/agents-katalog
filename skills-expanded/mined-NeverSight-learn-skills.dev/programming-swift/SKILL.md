---
name: programming-swift
user-invocable: false
description: Internal skill invoked by /programming chain. Use when writing, reviewing, or refactoring Swift code (.swift files). Use when encountering Sendable conformance errors, actor isolation warnings, @MainActor issues, "cannot convert value of type 'any X' to expected type 'some X'", or Swift 6 strict concurrency migration. Use when choosing struct vs class vs actor, designing protocols, handling errors with typed throws, managing SwiftUI state (@Observable vs @ObservableObject), writing Swift Testing tests (@Test, #expect), or reviewing Swift API naming conventions. Use when designing Metal compute/render pipelines for Apple Silicon — tile shaders, imageblocks, TBDR, memoryless textures, storage modes. Use when working with macOS AppKit/SwiftUI interop — NSViewRepresentable, NSHostingController, NSSlider wrappers, real-time controls, event tracking mode, NSTrackingArea, NSWindow management, CADisplayLink, CVDisplayLink.
---

# Swift Expert Patterns

Idiomatic Swift 6 patterns for building correct, performant, and maintainable code on Apple platforms and beyond. NOT for: Vapor/Hummingbird server deployment, SPM CI/CD pipelines, SwiftUI layout debugging, or Xcode project configuration.

## 1. Value Types & Type Selection

**Default to struct.** Swift's type system favors value semantics.

| Type   | Use when                                                                   |
| ------ | -------------------------------------------------------------------------- |
| struct | Data model, no identity needed, thread-safe by default, small or has COW   |
| class  | Shared mutable state with identity (`===`), NSObject subclass, need deinit |
| enum   | Closed set of cases, state machines, errors, associated values             |
| actor  | Shared mutable state with concurrency safety, serialized resource access   |

```swift
// struct: coordinates, configs, DTOs
struct Measurement { var value: Double; var unit: Unit }

// enum: state machines with associated data
enum LoadState<T> {
    case idle, loading
    case loaded(T)
    case failed(Error)
}

// actor: concurrent shared state
actor ImageCache {
    private var cache: [URL: Image] = [:]
    func image(for url: URL) -> Image? { cache[url] }
    func store(_ image: Image, for url: URL) { cache[url] = image }
}
```

**Copy-on-write.** Array, Dictionary, Set, String use COW automatically. Avoid holding extra references to collections you're about to mutate -- it forces a full copy. For custom value types with large storage, implement COW with `isKnownUniquelyReferenced(&_storage)`.

## 2. Protocol-Oriented Design

Prefer composition over inheritance. Small, focused protocols composed together.

```swift
// Good: small, composable protocols
protocol Identifiable { associatedtype ID: Hashable; var id: ID { get } }
protocol Persistable { func save() throws }
protocol Expirable { var expiresAt: Date { get } }

// Compose at use site
func cleanup<T: Persistable & Expirable>(_ items: [T]) throws { ... }

// Bad: God protocol
protocol DataManageable {
    var id: String { get }
    func save() throws
    func delete() throws
    func validate() -> Bool
    func export() -> Data
    // 10+ more requirements...
}
```

**Default implementations** via extensions provide shared behavior without inheritance. Override only what differs.

**Protocol vs concrete type decision:**
1. Start with concrete types
2. Extract a protocol only when you have 2+ conformers or need testability
3. Prefer `some Protocol` (opaque) over `any Protocol` (existential)

## 3. Generics & Type System

### some vs any Decision

```
Concrete type  →  some Protocol  →  any Protocol
(prefer)          (hide type)       (heterogeneous collections only)
```

- **`some`** (opaque): fixed underlying type, zero-cost, static dispatch. `func makeView() -> some View`
- **`any`** (existential): type-erased box, heap allocation if >24 bytes, dynamic dispatch. `var handlers: [any EventHandler]`

Swift 6 requires explicit `any` -- intentional friction to prefer `some`.

### Conditional Conformance

```swift
// Array is Equatable only when its elements are
extension Array: Equatable where Element: Equatable { }

// Your types can do the same
extension Cache: Sendable where Key: Sendable, Value: Sendable { }
```

**Parameter packs** (Swift 5.9+): variadic generics (`func zip<each T>(_ value: repeat each T)`). Used by SwiftUI internally; rare in app code.

## 4. Error Handling

### Choosing a Strategy

| Mechanism           | Use when                                                     |
| ------------------- | ------------------------------------------------------------ |
| `throws`            | Default for fallible functions. Callers choose how to handle |
| `throws(ErrorType)` | Internal modules with closed, stable error domains           |
| `Result<T, E>`      | Storing outcomes, callback APIs. Avoid in async code         |
| `Optional` (nil)    | Failure carries no diagnostic information                    |

```swift
// Typed throws (Swift 6) -- exhaustive catching
enum ValidationError: Error { case empty, tooLong(max: Int), invalidFormat }

func validate(_ input: String) throws(ValidationError) -> Validated {
    guard !input.isEmpty else { throw .empty }
    guard input.count <= 256 else { throw .tooLong(max: 256) }
    guard input.matches(pattern) else { throw .invalidFormat }
    return Validated(input)
}

// Caller gets exhaustive switch -- no catch-all needed
do { let v = try validate(raw) }
catch .empty { /* handle */ }
catch .tooLong(let max) { /* handle */ }
catch .invalidFormat { /* handle */ }
```

**Error propagation.** Wrap errors at layer boundaries. Use enums for closed error sets, structs for extensible ones.

```swift
// Layer boundary wrapping
func loadUser(_ id: String) throws -> User {
    do { return try repository.fetch(id) }
    catch { throw ServiceError.loadFailed(id: id, underlying: error) }
}
```

## 5. Concurrency (Swift 6)

The largest and most critical section. Swift 6 makes data race safety a compiler guarantee.

### Sendable

Values crossing isolation boundaries must be `Sendable`. Value types with all-Sendable fields auto-conform. Classes must be `final` with immutable stored properties. Use `@unchecked Sendable` only when you've manually verified thread safety (lock, atomic, etc).

### Actor Isolation

```swift
actor DatabaseManager {
    private var connections: [Connection] = []

    func acquire() async throws -> Connection {
        if let conn = connections.popLast() { return conn }
        return try await Connection.open()
    }

    // nonisolated -- no mutable state access, no await needed
    nonisolated var maxConnections: Int { 10 }
}
```

**Actor hop cost.** Each `await` to an actor is a suspension point. In loops, batch operations:

```swift
// Bad: N actor hops
for item in items { await cache.store(item) }

// Good: 1 actor hop
await cache.storeAll(items)
```

### @MainActor

UI work must be on `@MainActor`. Apply to types, methods, or closures.

```swift
@MainActor
@Observable final class ViewModel {
    var title = ""
    func load() async {
        let data = await service.fetch()  // hops off main
        title = data.title                // back on main (implicit)
    }
}
```

**Swift 6.2 approachable concurrency:** `defaultIsolation: MainActor` makes the entire module default to main actor. Use `@concurrent` to opt individual functions into background execution.

### Structured Concurrency

```swift
// Parallel work with TaskGroup
func fetchAll(_ urls: [URL]) async throws -> [Data] {
    try await withThrowingTaskGroup(of: (Int, Data).self) { group in
        for (i, url) in urls.enumerated() {
            group.addTask { (i, try await fetch(url)) }
        }
        var results = Array<Data?>(repeating: nil, count: urls.count)
        for try await (i, data) in group { results[i] = data }
        return results.compactMap { $0 }
    }
}
```

**Cancellation is cooperative.** Check `Task.isCancelled` or call `try Task.checkCancellation()` in long-running work.

### Migration from Swift 5

1. Enable strict concurrency per-target: `targeted` → `complete` → Swift 6 mode
2. Use `@preconcurrency import` for un-updated dependencies
3. Use `nonisolated(unsafe)` sparingly for known-safe legacy globals
4. Address `Sendable` conformance from leaf types inward

### Concurrency Anti-Patterns

- **Ignoring Sendable warnings.** They are not noise. They prevent data races.
- **`@unchecked Sendable` without proof.** Must document why it's safe.
- **Sequential awaits when parallel is possible.** Use `async let` or `TaskGroup`.
- **Holding actor-isolated state across suspension points.** State may change between awaits.

## 6. Memory & Performance

### ARC and Capture Lists

```swift
// Escaping closure stored by self -- needs [weak self]
class NetworkManager {
    var onComplete: (() -> Void)?

    func start() {
        onComplete = { [weak self] in
            guard let self else { return }
            self.handleComplete()
        }
    }
}
```

**Rule: `weak` over `unowned`.** Performance difference is negligible; safety gain is significant.

**Task closures.** `Task { }` within a method captures `self` strongly but does not create a retain cycle because `Task` is not stored by `self`. Use `[weak self]` only when the task outlives the object or is stored.

### Stack vs Heap

- Structs with concrete types: stack-allocated
- Structs in `any Protocol` existentials: heap-allocated if >24 bytes
- Classes: always heap
- `some Protocol`: zero-cost, static dispatch, stack-eligible

**Prefer `some` over `any` for performance.** Existentials have 5-word overhead (3 value buffer + VWT + PWT).

### Optimization Hints

- `@inlinable` -- exports function body for cross-module optimization. Body becomes ABI.
- `ContiguousArray` -- outperforms `Array` when elements are class types (avoids NSArray bridging).
- `.lazy` chains -- avoid intermediate array allocations in transformation pipelines.

## 7. Testing (Swift Testing)

Use Swift Testing for all new tests. Keep XCTest for UI tests and performance benchmarks.

```swift
import Testing

@Test("User creation validates email")
func userValidation() throws {
    let user = try User(name: "Alice", email: "alice@example.com")
    #expect(user.isValid)
}

// Parameterized -- each argument is an independent test case
@Test("Email validation", arguments: [
    ("valid@email.com", true),
    ("no-at-sign", false),
    ("@no-local", false),
])
func emailCheck(_ email: String, _ expected: Bool) {
    #expect(isValidEmail(email) == expected)
}
```

### Testing Async / Actors

```swift
@Test func actorState() async {
    let counter = Counter()
    await counter.increment()
    #expect(await counter.value == 1)
}

// confirmation replaces XCTestExpectation
@Test func delegateNotified() async {
    await confirmation("called", expectedCount: 1) { confirm in
        let mock = MockDelegate(onUpdate: { confirm() })
        let engine = Engine(delegate: mock)
        await engine.run()
    }
}
```

### Dependency Injection for Testability

```swift
protocol DataFetching: Sendable {
    func fetch(id: String) async throws -> Data
}

struct LiveFetcher: DataFetching { /* real implementation */ }
struct MockFetcher: DataFetching {
    let result: Data
    func fetch(id: String) async throws -> Data { result }
}

// Default parameter -- production uses live, tests inject mock
actor Service {
    private let fetcher: DataFetching
    init(fetcher: DataFetching = LiveFetcher()) { self.fetcher = fetcher }
}
```

## 8. API Design & Naming

Follow Apple's API Design Guidelines (swift.org). Non-negotiable in Swift.

**Clarity at point of use** is the overriding goal.

| Rule                          | Example                                      |
| ----------------------------- | -------------------------------------------- |
| Mutating: imperative verb     | `sort()`, `append(_:)`, `removeAll()`        |
| Non-mutating: noun/-ed/-ing   | `sorted()`, `appending(_:)`, `removingAll()` |
| Bool properties: assertions   | `isEmpty`, `isValid`, `hasChanges`           |
| Capability protocols: -able   | `Equatable`, `Sendable`, `Decodable`         |
| Noun protocols: what it is    | `Collection`, `View`, `Sequence`             |
| Omit label for grammar phrase | `addSubview(y)`, `contains(element)`         |
| Label for prepositions        | `move(from: a, to: b)`, `remove(at: index)`  |

**Property vs method:** Use property when O(1), no side effects, no significant computation.

**Configurable defaults** (Swift's functional options):

```swift
struct Config {
    var timeout: TimeInterval = 30
    var retries: Int = 3
}
func fetch(_ url: URL, config: Config = .init()) async throws -> Data
```

## 9. Package & Module Organization

Split targets: `MyAppCore` (business logic, testable) + `MyAppUI` (views) + `MyApp` (entry point). Use `package` access level (SE-0386) for package-scoped visibility (broader than `internal`, narrower than `public`). Use `Bundle.module` for SPM resources. Build tool plugins run codegen during build (swift-openapi-generator is canonical).

## 10. Property Wrappers

### When to Write One

Write a property wrapper when the same get/set logic repeats across 3+ properties. Otherwise use a computed property.

```swift
@propertyWrapper
struct Clamped<V: Comparable> {
    private var value: V
    let range: ClosedRange<V>

    var wrappedValue: V {
        get { value }
        set { value = min(max(newValue, range.lowerBound), range.upperBound) }
    }

    init(wrappedValue: V, range: ClosedRange<V>) {
        self.range = range
        self.value = min(max(wrappedValue, range.lowerBound), range.upperBound)
    }
}

// Usage
@Clamped(range: 0...1) var opacity: Double = 0.5
```

**projectedValue** exposes additional state via `$property`. Used by SwiftUI (@State → Binding, @Published → Publisher).

### The @Atomic Anti-Pattern

A lock-based `@Atomic` wrapper is fundamentally flawed: `x += 1` is read-then-write with a gap between lock acquisitions. Use `Mutex.withLock` or actors instead.

## 11. Platform Integration

### UIKit Interop

```swift
struct MapView: UIViewRepresentable {
    let region: MKCoordinateRegion

    func makeUIView(context: Context) -> MKMapView { MKMapView() }
    func updateUIView(_ view: MKMapView, context: Context) {
        view.setRegion(region, animated: true)  // Update only changed properties
    }
    func makeCoordinator() -> Coordinator { Coordinator() }
}
```

**In updateUIView, update only changed properties** -- setting everything causes flicker/scroll resets.

**Incremental adoption:** Use `UIHostingController` to embed SwiftUI in UIKit (start with leaf screens). Use `UIViewRepresentable` for the reverse.

### Objective-C Interop

- `@objc` -- exposes to Obj-C runtime. Required for `#selector`, KVO, `@IBAction`.
- `@objcMembers` on a class -- infers `@objc` on all compatible members. Use selectively.
- `NSObject` subclass -- only when Obj-C frameworks demand it. Swift-native classes use faster vtable dispatch.
- `dynamic` -- forces full Obj-C message dispatch. Required for KVO and method swizzling.

**Cannot cross the bridge:** Swift structs, enums with associated values, generic classes, tuples, protocols with associated types.

## 12. Anti-Patterns

| Anti-Pattern                               | Fix                                                           |
| ------------------------------------------ | ------------------------------------------------------------- |
| Force unwrap (`!`)                         | `guard let`, `if let`, `??`, `compactMap`                     |
| Massive ViewModels                         | Extract into services, repositories, coordinators             |
| God protocols (10+ reqs)                   | Small protocols + composition                                 |
| Stringly-typed keys                        | Enums, `CodingKeys`, typed identifiers                        |
| Ignoring Sendable warnings                 | Make types `Sendable` or isolate them to an actor             |
| Premature `any`                            | Use concrete types or `some` first                            |
| Pyramid of doom                            | `guard let a, let b, let c else { return }`                   |
| `try!` in production                       | `try` + propagation or `try?` when failure is truly ignorable |
| `@unchecked Sendable` cargo                | Prove safety with locks/atomics or use actors                 |
| Class when struct suffices                 | Default to struct; class only for identity/reference needs    |
| Sequential awaits                          | `async let` or `TaskGroup` for parallel work                  |
| Storing `context` from UIViewRepresentable | SwiftUI manages lifecycle -- don't retain it                  |

## 13. Metal GPU Design (Apple Silicon)

TBDR architecture, tile shaders, imageblocks, storage modes, kernel protocol design. Read `references/metal-gpu-design.md`.

## 14. AppKit + SwiftUI Hybrid Patterns

NSViewRepresentable lifecycle, update loop prevention, event tracking mode, real-time visualization (CADisplayLink, CVDisplayLink, MTKView), window management, when to use AppKit vs SwiftUI. Read `references/appkit-swiftui-hybrid.md`. For on-demand MTKView rendering, read `references/mtkview-on-demand.md`.

## 15. Running Apps

- When the user says "run it" and the project has a buildable app (macOS, iOS, etc.), launch it via the debugger (build with xcodebuild, then `open` the .app from DerivedData) rather than just running tests.
- If a debugger/launch approach makes sense for the context, always prefer it over a headless run.
