---
name: apple-engineer-superpowers
description: Use when writing Swift code for Apple platforms - iOS, macOS, visionOS. Covers Swift 6 concurrency, actors, Sendable, async/await, SwiftUI, MVVM architecture, Metal GPU programming, RealityKit ECS, visionOS scenes, interpolation/animation, advanced collection types, property wrappers, Combine bridging, error handling, testing, and API design patterns.
---

# Apple Platform Engineering

Comprehensive Swift engineering standards for building production-quality Apple platform applications.

## Core Principles

1. **No Force Unwrapping (`!`)** - Use `guard let`, `if let`, nil coalescing (`??`), or optional chaining. Never crash on nil.
2. **Actor-First Concurrency** - Use actors as the default for stateful components. Prefer actor isolation over manual locking.
3. **Async/Await Always** - Never use completion handlers in new code. Use `async throws` functions.
4. **Sendable Everything** - All shared types must conform to `Sendable`. All closures crossing concurrency boundaries must be `@Sendable`.
5. **Swift 6 Strict Concurrency** - Enable `StrictConcurrency` from the start. No data races.
6. **Protocol-Oriented Design** - Define contracts through protocols. Use dependency injection for testability.
7. **LocalizedError for Errors** - Domain-specific error enums conforming to `LocalizedError, Sendable`.

## Quick Reference

### Safe Optional Handling

| Instead of | Use |
|------------|-----|
| `value!` | `guard let value else { return }` |
| `string.data(using: .utf8)!` | `string.data(using: .utf8) ?? Data()` |
| `url!` | `guard let url = URL(string: s) else { return }` |
| `object.property!` | `object.property?.method()` or `if let prop = object.property { }` |

### Concurrency Primitives

| Need | Use |
|------|-----|
| Stateful shared component | `actor` |
| Simple value protection | `Mutex<State>` |
| Low-level sync | `OSAllocatedUnfairLock` |
| UI state management | `@MainActor` on ViewModels |
| Progress/events stream | `AsyncStream` / `AsyncThrowingStream` |
| Multi-subscriber broadcast | `AsyncBroadcastChannel` or `AsyncNotifier` |

### Actor vs @MainActor Decision

| Scenario | Use |
|----------|-----|
| API service, data operations | `actor` |
| ViewModel with `@Published` | `@MainActor final class: ObservableObject` |
| Service with `@Published` properties Views observe | `@MainActor ObservableObject` (rare) |
| Pure data model | `struct: Sendable` |

### Error Handling Pattern

```swift
enum ServiceError: LocalizedError, Sendable {
    case operationFailed(String)

    var errorDescription: String? {
        switch self {
        case .operationFailed(let msg): return "Operation failed: \(msg)"
        }
    }
}
```

### API Design

| Pattern | Use |
|---------|-----|
| `func work() async throws -> T` | Standard async operation |
| `func work() -> AsyncThrowingStream<Event, Error>` | Progress/event reporting |
| `func work(progress: @Sendable (Float) -> Void) async throws -> T` | Simple progress callback |

### Metal GPU Quick Reference

| Need | Use |
|------|-----|
| Compute pipeline | `MTLComputePipelineDescriptor` + `device.makeComputePipelineState` |
| Render pipeline | `MTLRenderPipelineDescriptor` + vertex/fragment functions |
| Buffer management | `MetalBuffer<Element>` generic wrapper |
| Multi-frame pipelining | Ring buffer (pool of 3) with `tick()` |
| Texture from IOSurface | `device.makeTexture(descriptor:iosurface:plane:)` |
| Threadgroup sizing | `min(elementCount, pipelineState.maxTotalThreadsPerThreadgroup)` |

### RealityKit/visionOS Quick Reference

| Need | Use |
|------|-----|
| Custom entity data | `struct: Component` |
| Per-frame logic | `class: System` with scene subscriptions |
| Show entities in SwiftUI | `RealityView { content in content.add(entity) }` |
| Observe component changes | `entity.componentChangePublisher(T.self)` |
| Full immersion | `ImmersiveSpace(id:) { }.immersionStyle(.full)` |
| Multi-window | `WindowGroup(id:)` with `WindowPlacement` |

### Advanced Patterns Quick Reference

| Need | Use |
|------|-----|
| Smooth value tracking | `ExponentialDamper<T: Lerpable>` |
| Generic interpolation | `Lerpable` protocol with `lerp(from:to:blend:)` |
| Non-empty guarantee | `NonEmpty<C: Collection>` |
| Enum-keyed storage | `Table<E: CaseIterable, V>` |
| Multi-consumer async | `AsyncBroadcastChannel` with back-pressure |
| Combine to async | `publisher.sinkSingleValue() async throws` |
| Custom defaults | `@DefaultValue<T>` property wrapper |

## Detailed References

- **swift-concurrency.md** — Swift 6 concurrency patterns: actors, Sendable, AsyncSequence, task cancellation, synchronization, state machines, reactive patterns, generics, persistence, networking, testing, diagnostics
- **swiftui-architecture.md** — SwiftUI app architecture: MVVM, ViewModel/View guidelines, service layer patterns, data flow, App Intents, file organization
- **metal-graphics.md** — Metal GPU programming: pipelines, buffers, textures, compute dispatch, ring buffers, shaders, frame pacing
- **realitykit-visionos.md** — RealityKit ECS and visionOS: entities, components, systems, scene subscriptions, immersive spaces, windows, hand tracking
- **advanced-swift-patterns.md** — Property wrappers, interpolation/animation, collection types, Combine bridging, advanced async abstractions, @dynamicMemberLookup
