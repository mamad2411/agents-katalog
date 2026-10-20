---
name: swift-protocols
description: "When to activate: Swift protocols, protocol extensions, associated types, protocol composition, existentials, primary associated types, opaque types"
origin: zakr
metadata:
  namespace: zakr/devtools-pack
  version: 1.0.0
  category: engineering
  language: swift
  platforms: [claude-code, codex, gemini-cli, cursor, aider, windsurf]
---

# Swift Protocols

## Protocol-Oriented Design

Prefer protocols over inheritance for polymorphism.

```swift
protocol Drawable {
    func draw(in context: CGContext)
    var bounds: CGRect { get }
}

protocol Animatable {
    func animate(duration: TimeInterval)
}

// Composition without inheritance
struct AnimatedShape: Drawable & Animatable {
    var bounds: CGRect
    func draw(in context: CGContext) { ... }
    func animate(duration: TimeInterval) { ... }
}
```

## Protocol Extensions — Default Implementations

```swift
protocol Identifiable {
    var id: UUID { get }
}

extension Identifiable {
    // All conforming types get this for free
    func matches(_ other: Self) -> Bool { id == other.id }
}

protocol Persistable: Identifiable {
    func save(to store: Store) throws
    func delete(from store: Store) throws
}

extension Persistable {
    // Default delete by ID
    func delete(from store: Store) throws {
        try store.remove(id: id)
    }
}
```

## Associated Types

```swift
protocol Repository {
    associatedtype Entity: Identifiable
    func findAll() async throws -> [Entity]
    func find(id: Entity.ID) async throws -> Entity?
    func save(_ entity: Entity) async throws
    func delete(_ entity: Entity) async throws
}

// Constrained to Codable entities stored in JSON
struct JSONRepository<T: Codable & Identifiable>: Repository {
    func findAll() async throws -> [T] { ... }
    func find(id: T.ID) async throws -> T? { ... }
    func save(_ entity: T) async throws { ... }
    func delete(_ entity: T) async throws { ... }
}
```

## Opaque Types (some Protocol)

```swift
// Concrete return type hidden behind protocol — enables ABI stability
func makeButton(title: String) -> some View {
    Button(title) {}
        .padding()
        .background(.blue)
        .foregroundStyle(.white)
}

// Function can return different concrete types as long as they match the protocol
// But: a single function body must return ONE concrete type
```

## Existential Types (any Protocol) — Swift 5.7+

```swift
// any Protocol — heterogeneous collection, runtime dispatch
var drawables: [any Drawable] = [Circle(), Square(), Triangle()]

// some Protocol — opaque type, compile-time dispatch, single concrete type
func render(_ shape: some Drawable) { ... }

// Primary associated types for constrained existentials
protocol Collection<Element> {
    associatedtype Element
}

var numbers: any Collection<Int> = [1, 2, 3]
```

## Protocol Composition

```swift
typealias PersistableDrawable = Persistable & Drawable

func saveAndRender(_ item: some PersistableDrawable, store: Store, context: CGContext) throws {
    try item.save(to: store)
    item.draw(in: context)
}

// Conditional conformance
extension Array: Drawable where Element: Drawable {
    var bounds: CGRect { reduce(.zero) { $0.union($1.bounds) } }
    func draw(in context: CGContext) { forEach { $0.draw(in: context) } }
}
```

## Dependency Injection via Protocols

```swift
protocol HTTPClient: Sendable {
    func data(for request: URLRequest) async throws -> (Data, URLResponse)
}

extension URLSession: HTTPClient {}  // URLSession conforms for free

struct UserService {
    let client: any HTTPClient  // or `some HTTPClient` if the type is fixed

    func getUser(id: UUID) async throws -> User {
        let request = URLRequest(url: URL(string: "https://api.example.com/users/\(id)")!)
        let (data, _) = try await client.data(for: request)
        return try JSONDecoder().decode(User.self, from: data)
    }
}

// In tests
struct MockHTTPClient: HTTPClient {
    var responseData: Data
    func data(for request: URLRequest) async throws -> (Data, URLResponse) {
        let response = HTTPURLResponse(url: request.url!, statusCode: 200, httpVersion: nil, headerFields: nil)!
        return (responseData, response)
    }
}
```

## Common Anti-Patterns

- **Protocol with too many requirements** — split into focused protocols (Interface Segregation)
- **Using `any Protocol` everywhere** — prefer `some Protocol` for better performance
- **Overusing inheritance** — protocols + extensions compose more flexibly
- **Retroactive conformances in libraries** — they can conflict with other packages; use `extension` in app code only
- **Self or associated type requirements without `any`** — you'll get compile errors; use `some` or constrain generics
