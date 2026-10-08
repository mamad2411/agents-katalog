---
name: ios-concurrency
description: >
  Swift Concurrency expert skill covering async/await, structured concurrency (Task, TaskGroup),
  actors and @MainActor, Sendable protocol and checking, AsyncSequence/AsyncStream, continuations
  for bridging callback APIs, Swift 6 strict concurrency mode, and common concurrency patterns
  (debouncing, throttling, actor-based shared state, background processing). Use this skill whenever
  the user writes concurrent Swift code, works with async/await, actors, or Sendable, migrates to
  Swift 6 concurrency, or needs to handle background work and thread safety. Triggers on: async,
  await, Task, TaskGroup, actor, @MainActor, Sendable, @Sendable, concurrency, AsyncSequence,
  AsyncStream, continuation, withCheckedContinuation, nonisolated, GlobalActor, Swift 6, strict
  concurrency, data race, thread safety, background task, parallel, concurrent, dispatch queue
  migration, or any Swift concurrency question.
---

# iOS Concurrency Skill

## Core Rules

1. **Use async/await for ALL new asynchronous code.** Do not use completion handlers or Combine for async operations in new code.
2. **Use structured concurrency (Task, TaskGroup).** Avoid unstructured task leaks. Prefer `async let` or `TaskGroup` over spawning loose `Task {}` blocks.
3. **Mark UI-updating code with @MainActor.** SwiftUI views are already `@MainActor`-isolated. UIKit code that touches UI must run on `@MainActor`.
4. **Use actors for shared mutable state** instead of locks, semaphores, or serial dispatch queues.
5. **All types crossing actor boundaries must be Sendable.** The compiler enforces this in strict concurrency mode.
6. **Prefer value types (struct, enum) for Sendable.** They are implicitly Sendable when all stored properties are Sendable.
7. **Use `withCheckedContinuation` to bridge callback-based APIs** to async/await. Never resume a continuation more than once.
8. **Use `AsyncStream` for bridging delegate/callback patterns** to `AsyncSequence`.
9. **`Task.detached` is rarely needed.** Use `Task {}` with explicit actor isolation instead. Detached tasks lose actor context and priority inheritance.
10. **Always handle Task cancellation cooperatively.** Check `Task.isCancelled` or call `try Task.checkCancellation()` at appropriate points.

## Decision Guide

| Scenario | Solution |
|----------|----------|
| Single async operation | `async func` / `Task {}` |
| Multiple independent operations | `TaskGroup` / `async let` |
| Sequential dependent operations | `await` one after another |
| Shared mutable state | `actor` |
| UI updates from background | `@MainActor` / `MainActor.run {}` |
| Bridge callback API | `withCheckedContinuation` / `withCheckedThrowingContinuation` |
| Bridge delegate pattern | `AsyncStream` with continuation |
| Streaming data | `AsyncSequence` / `AsyncStream` |
| Debounce user input | Task cancellation pattern |
| Non-Sendable legacy type | `@preconcurrency import` / `@unchecked Sendable` (last resort) |
| Combine publisher to async | `.values` property on publisher |
| Timer / periodic work | `AsyncTimerSequence` (from swift-async-algorithms) or `AsyncStream` |
| Parallel with limit | `TaskGroup` with semaphore-like counter |

## Quick Reference: async/await

```swift
// Basic async function
func fetchUser(id: String) async throws -> User {
    let (data, response) = try await URLSession.shared.data(from: url)
    guard let httpResponse = response as? HTTPURLResponse,
          httpResponse.statusCode == 200 else {
        throw APIError.invalidResponse
    }
    return try JSONDecoder().decode(User.self, from: data)
}

// Calling from SwiftUI
.task {
    do {
        user = try await fetchUser(id: "123")
    } catch {
        errorMessage = error.localizedDescription
    }
}

// Parallel execution with async let
async let profile = fetchProfile(id: userId)
async let posts = fetchPosts(userId: userId)
async let followers = fetchFollowers(userId: userId)
let result = try await (profile, posts, followers)

// TaskGroup for dynamic parallelism
func fetchAllUsers(ids: [String]) async throws -> [User] {
    try await withThrowingTaskGroup(of: User.self) { group in
        for id in ids {
            group.addTask { try await self.fetchUser(id: id) }
        }
        var users: [User] = []
        for try await user in group {
            users.append(user)
        }
        return users
    }
}
```

## Quick Reference: Actors

```swift
// Actor for shared state
actor ImageCache {
    private var cache: [URL: UIImage] = [:]

    func image(for url: URL) -> UIImage? {
        cache[url]
    }

    func store(_ image: UIImage, for url: URL) {
        cache[url] = image
    }
}

// Usage — await is required to cross isolation boundary
let cache = ImageCache()
await cache.store(image, for: url)
let cached = await cache.image(for: url)

// @MainActor for UI
@MainActor
final class ViewModel: ObservableObject {
    @Published var items: [Item] = []
    @Published var isLoading = false

    func loadItems() async {
        isLoading = true
        defer { isLoading = false }
        do {
            items = try await api.fetchItems()
        } catch {
            // handle error
        }
    }
}
```

## Quick Reference: Sendable

```swift
// Value types — automatically Sendable if all members are
struct UserDTO: Sendable {
    let id: String
    let name: String
}

// Reference types — must be final with immutable stored properties
final class Configuration: Sendable {
    let apiKey: String
    let baseURL: URL
    init(apiKey: String, baseURL: URL) {
        self.apiKey = apiKey
        self.baseURL = baseURL
    }
}

// @unchecked Sendable — escape hatch (use with caution)
final class LegacyManager: @unchecked Sendable {
    private let lock = NSLock()
    private var _state: State = .idle
    var state: State {
        lock.withLock { _state }
    }
}
```

## Quick Reference: Continuations

```swift
// Bridge completion handler to async/await
func fetchData() async throws -> Data {
    try await withCheckedThrowingContinuation { continuation in
        legacyAPI.fetch { result in
            switch result {
            case .success(let data):
                continuation.resume(returning: data)
            case .failure(let error):
                continuation.resume(throwing: error)
            }
        }
    }
}

// Bridge delegate to AsyncStream
func locationUpdates() -> AsyncStream<CLLocation> {
    AsyncStream { continuation in
        let delegate = LocationDelegate { location in
            continuation.yield(location)
        }
        continuation.onTermination = { _ in
            delegate.stop()
        }
        delegate.start()
    }
}
```

## Quick Reference: Task Cancellation

```swift
// Cooperative cancellation
func processItems(_ items: [Item]) async throws {
    for item in items {
        try Task.checkCancellation()  // throws CancellationError
        await process(item)
    }
}

// Manual check
func fetchWithFallback() async -> Data {
    if Task.isCancelled { return Data() }
    // ... continue work
}

// Debounce pattern
@MainActor
final class SearchViewModel: ObservableObject {
    @Published var query = ""
    @Published var results: [Result] = []
    private var searchTask: Task<Void, Never>?

    func search() {
        searchTask?.cancel()
        searchTask = Task {
            try? await Task.sleep(for: .milliseconds(300))
            guard !Task.isCancelled else { return }
            results = await api.search(query)
        }
    }
}
```

## Swift 6 Strict Concurrency Quick Guide

```swift
// Enable in Package.swift
.target(
    name: "MyTarget",
    swiftSettings: [.swiftLanguageMode(.v6)]
)

// Or in Xcode: Build Settings → Swift Language Version → 6

// Common fixes:
// 1. Non-Sendable type crossing isolation boundary
//    → Make type Sendable or use @unchecked Sendable

// 2. Mutable capture in @Sendable closure
//    → Use actor or move state inside Task

// 3. Global variable not concurrency-safe
//    → Use actor, nonisolated(unsafe), or make it let

// 4. Legacy framework types not Sendable
//    → @preconcurrency import FrameworkName
```

## Anti-Patterns to Avoid

```swift
// BAD: Using Task.detached without good reason
Task.detached {
    await self.doWork()  // loses actor isolation and priority
}

// GOOD: Use Task {} — inherits actor context
Task {
    await doWork()
}

// BAD: Blocking an actor with synchronous work
actor DataProcessor {
    func process(_ data: Data) -> Result {
        heavySyncComputation(data)  // blocks the actor's executor
    }
}

// GOOD: Move heavy sync work off the actor
actor DataProcessor {
    func process(_ data: Data) async -> Result {
        await Task.detached(priority: .utility) {
            heavySyncComputation(data)  // runs on cooperative pool
        }.value
    }
}

// BAD: Ignoring cancellation
Task {
    for item in hugeList {
        await process(item)  // never checks cancellation
    }
}

// GOOD: Cooperative cancellation
Task {
    for item in hugeList {
        try Task.checkCancellation()
        await process(item)
    }
}

// BAD: Resuming continuation multiple times (CRASH)
withCheckedContinuation { continuation in
    api.fetch { data in
        continuation.resume(returning: data)
    }
    api.fetch { data in  // second resume — CRASH
        continuation.resume(returning: data)
    }
}

// BAD: Never resuming continuation (LEAK — task hangs forever)
withCheckedContinuation { continuation in
    api.fetch { data in
        if let data = data {
            continuation.resume(returning: data)
        }
        // if data is nil, continuation is never resumed!
    }
}
```

## Performance Considerations

- **Task creation overhead**: ~1-2 microseconds. Do not create tasks in tight loops for trivial work.
- **Actor contention**: If many tasks await the same actor, they serialize. Keep actor methods fast.
- **MainActor bottleneck**: Do not run heavy computation on `@MainActor`. Offload to a non-isolated async function or `Task.detached`.
- **async let**: Creates a child task immediately. Only use when you actually need parallelism.
- **TaskGroup**: Prefer over multiple `async let` when the number of operations is dynamic.
- **Sendable checking**: Zero runtime cost. It is compile-time only.
- **When NOT to use async/await**: Pure synchronous computation, simple property access, performance-critical inner loops.

## Reference Files

- [async-await.md](references/async-await.md) — async/await, Task, TaskGroup, continuations, AsyncSequence
- [actors.md](references/actors.md) — actor, @MainActor, GlobalActor, nonisolated, Sendable
- [patterns.md](references/patterns.md) — common patterns, Swift 6 migration, Combine vs async/await
