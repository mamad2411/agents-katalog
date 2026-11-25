---
name: combine-patterns
description: "When to activate: Combine framework, publishers, subscribers, sink, flatMap, debounce, merge, PassthroughSubject, CurrentValueSubject"
origin: zakr
metadata:
  namespace: zakr/devtools-pack
  version: 1.0.0
  category: engineering
  language: swift
  platforms: [claude-code, codex, gemini-cli, cursor, aider, windsurf]
---

# Combine Patterns

## Core Concepts

```swift
import Combine

// Subject — imperative publisher you push values into
let subject = PassthroughSubject<String, Never>()

// CurrentValueSubject — stores latest value, replays to new subscribers
let state = CurrentValueSubject<Bool, Never>(false)

// Subscription — always store to prevent cancellation
var cancellables = Set<AnyCancellable>()

subject
    .filter { !$0.isEmpty }
    .map { $0.uppercased() }
    .sink { print($0) }
    .store(in: &cancellables)

subject.send("hello")  // prints "HELLO"
```

## Search with Debounce

```swift
class SearchViewModel: ObservableObject {
    @Published var query = ""
    @Published private(set) var results: [Result] = []

    private var cancellables = Set<AnyCancellable>()

    init(service: SearchService) {
        $query
            .debounce(for: .milliseconds(300), scheduler: DispatchQueue.main)
            .removeDuplicates()
            .filter { $0.count >= 2 }
            .flatMap { query in
                Future<[Result], Never> { promise in
                    Task {
                        let r = (try? await service.search(query)) ?? []
                        promise(.success(r))
                    }
                }
            }
            .receive(on: DispatchQueue.main)
            .assign(to: \.results, on: self)
            .store(in: &cancellables)
    }
}
```

## Combining Publishers

```swift
// zip — pairs elements from two publishers
Publishers.Zip(userPublisher, settingsPublisher)
    .sink { user, settings in configure(user: user, settings: settings) }
    .store(in: &cancellables)

// merge — interleave events from multiple publishers of the same type
Publishers.Merge(tap1Publisher, tap2Publisher)
    .sink { handleTap($0) }
    .store(in: &cancellables)

// combineLatest — emits whenever any upstream emits, using latest from all
Publishers.CombineLatest(isLoggedIn, hasPermission)
    .map { $0 && $1 }
    .assign(to: \.canAccessFeature, on: self)
    .store(in: &cancellables)
```

## Error Handling

```swift
apiPublisher
    .catch { error -> AnyPublisher<[Item], Never> in
        print("Error: \(error)")
        return Just([]).eraseToAnyPublisher()
    }
    .retry(3)
    .sink { items in self.items = items }
    .store(in: &cancellables)
```

## Future for One-Shot Async Work

```swift
func fetchUser(id: UUID) -> AnyPublisher<User, APIError> {
    Future { promise in
        Task {
            do {
                let user = try await apiClient.getUser(id: id)
                promise(.success(user))
            } catch let error as APIError {
                promise(.failure(error))
            } catch {
                promise(.failure(.unknown))
            }
        }
    }
    .eraseToAnyPublisher()
}
```

## @Published with ObservableObject

```swift
class CartViewModel: ObservableObject {
    @Published var items: [CartItem] = []
    @Published var couponCode = ""
    @Published private(set) var total: Decimal = 0

    private var cancellables = Set<AnyCancellable>()

    init() {
        // Derive total reactively
        $items
            .map { items in items.reduce(0) { $0 + $1.price } }
            .assign(to: \.total, on: self)
            .store(in: &cancellables)
    }
}
```

## Migrate from Combine to async/await

```swift
// Combine → async/await bridge using values property
for await value in subject.values {
    process(value)
}

// Convert AnyPublisher to async
extension AnyPublisher where Failure == Never {
    var firstValue: Output {
        get async {
            await withCheckedContinuation { continuation in
                var cancellable: AnyCancellable?
                cancellable = first().sink { value in
                    continuation.resume(returning: value)
                    cancellable?.cancel()
                }
            }
        }
    }
}
```

## Common Anti-Patterns

- **Not storing subscriptions** — `AnyCancellable` deallocates immediately; store in `Set<AnyCancellable>`
- **`flatMap` without limiting** — use `flatMap(maxPublishers: .max(1))` for serial requests
- **Mixing `receive(on:)` late** — always switch to main queue before touching UI
- **`assign(to:on:)` causing retain cycles** — prefer `assign(to: &$published)` with Swift 5.6+
- **Using Combine for new code** — prefer `async/await` + `AsyncSequence` in Swift 5.9+; Combine for legacy UIKit
