---
name: rxswift-concurrency-bridge
description: "Use RxSwift's built-in Swift Concurrency bridging APIs instead of manual withCheckedThrowingContinuation wrappers. MUST trigger whenever Swift code bridges between RxSwift (Observable, Single, Maybe, Completable, Infallible, Driver, Signal) and async/await, or when you see withCheckedThrowingContinuation/withCheckedContinuation used alongside RxSwift subscribe patterns. Also trigger when converting async work back into Observables or Singles."
---

# RxSwift ↔ Swift Concurrency Bridge

RxSwift 6.5+ has built-in support for bridging between reactive and async/await code. Never use `withCheckedThrowingContinuation` or `withCheckedContinuation` to manually wrap RxSwift subscriptions — the framework provides cleaner, safer APIs that handle disposal, error propagation, and completion correctly out of the box.

Manual continuations are error-prone: they can resume twice, leak subscriptions, or miss edge cases around completion vs. error delivery. The built-in APIs avoid all of these pitfalls.

## Consuming RxSwift values in async/await

### Iterating over an Observable's values

Use `.values` to get an `AsyncThrowingStream` you can iterate with `for try await`:

```swift
do {
    for try await value in observable.values {
        print("Got a value:", value)
    }
} catch {
    print("Got an error:", error)
}
```

The Observable must complete, or the async task will suspend indefinitely.

### Iterating over non-throwing sequences

`Infallible`, `Driver`, and `Signal` never emit errors, so you can iterate without `try`:

```swift
for await value in infallible.values {
    print("Got a value:", value)
}
```

### Awaiting a single value

For `Single`, `Maybe`, and `Completable` — sequences that emit at most one value — await `.value` directly:

```swift
let value1 = try await single.value   // Element
let value2 = try await maybe.value     // Element? (nil if completed without value)
let value3 = try await completable.value // Void
```

This is the most common pattern when bridging service calls that return a Single or Observable-that-emits-once.

## Converting async work into RxSwift

### AsyncSequence → Observable

```swift
let stream = AsyncStream { ... }

stream.asObservable()
    .subscribe(
        onNext: { ... },
        onError: { ... }
    )
```

### Async function → Single

Use the `Single.create` overload that takes an `async throws` closure:

```swift
func doWork() async throws -> Response { ... }

let single = Single.create {
    try await doWork()
} // Single<Response>
```

## Observables that emit a single value (common in networking)

Many RxSwift networking layers wrap API calls as `Observable<T>` even though they only ever emit one value and complete. When you know an Observable is semantically single-valued (e.g., a network request/response), convert it to a `Single` with `.asSingle()` and then await `.value`:

```swift
// The network layer returns Observable<Response>, but it's always exactly one emission.
func sendCode(_ phone: String) async throws -> SendCodeResponse {
    try await loginService.sendCode(phone).asSingle().value
}
```

This is the preferred pattern because it's concise, expressive about intent (one value expected), and `.value` handles errors and disposal automatically.

If the Observable also materializes its events (i.e., emits `Event<T>` values via `.materialize()`), dematerialize first:

```swift
try await loginService.sendCode(phone).dematerialize().asSingle().value
```

## Before / After example

**Bad** — manual continuation wrapping (verbose, error-prone):

```swift
func sendCode(_ phone: String) async throws -> SendCodeResponse {
    return try await withCheckedThrowingContinuation { continuation in
        var disposable: Disposable?
        disposable = loginService.sendCode(phone)
            .subscribe(onNext: { event in
                switch event {
                case .next(let response):
                    continuation.resume(returning: response)
                case .error(let error):
                    continuation.resume(throwing: error)
                case .completed:
                    break
                @unknown default:
                    break
                }
            }, onCompleted: {
                _ = disposable
            })
    }
}
```

**Good** — `.asSingle().value`:

```swift
func sendCode(_ phone: String) async throws -> SendCodeResponse {
    try await loginService.sendCode(phone).asSingle().value
}
```

## Quick reference

| You have | You want | Use |
|---|---|---|
| `Observable<T>` | Iterate all values in async context | `for try await value in observable.values` |
| `Observable<T>` (single-valued, e.g. network call) | Get the one value | `try await observable.asSingle().value` |
| `Infallible<T>` / `Driver<T>` / `Signal<T>` | Iterate all values (no throws) | `for await value in infallible.values` |
| `Single<T>` | Get the one value | `try await single.value` |
| `Maybe<T>` | Get optional value | `try await maybe.value` → `T?` |
| `Completable` | Wait for completion | `try await completable.value` → `Void` |
| `AsyncSequence` | Convert to Observable | `asyncSequence.asObservable()` |
| `async throws → T` | Wrap as Single | `Single.create { try await work() }` |