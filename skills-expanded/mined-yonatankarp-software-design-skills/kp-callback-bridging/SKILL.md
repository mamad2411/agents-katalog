---
name: kp-callback-bridging
description: Use when wrapping a callback-based API in a suspending function — phrases like "suspendCancellableCoroutine", "suspendCoroutine", "bridge callback to suspend", "wrap a listener as a coroutine", "convert Java async to suspend", "callback to Deferred", "register a one-shot callback as a suspend function". Defines the suspendCancellableCoroutine builder as the canonical way to expose a callback API as an idiomatic `suspend fun` while honouring cancellation.
---

## One-line summary

Wrap a callback-based API in `suspendCancellableCoroutine { … }` so callers can use it as an idiomatic `suspend fun` — and the wrapper deregisters the callback when the coroutine is cancelled.

## When to use this skill

- Wrapping a third-party library that uses callbacks / listeners (Java SDKs, network clients, hardware APIs).
- Bridging an Android API (`OnClickListener`, `LocationListener`, sensor callbacks) into a coroutine API.
- Converting a one-shot future-style API (`CompletableFuture`, `ListenableFuture`) into a `suspend fun`.
- Turning a polling/event loop into a `Flow` (where each emission comes from a callback).

## When NOT to use this skill

- The API already returns a `Deferred`, a `CompletableFuture`, or a coroutine — use `.await()` or the existing bridge function.
- The callback fires *many times* and you want to react to every invocation — that's not a `suspend fun` (one-shot); it's a `Flow`. Use `callbackFlow { … }` instead.

## Core content

**`suspendCancellableCoroutine<T> { cont -> … }`** is a coroutine builder that:

1. Suspends the calling coroutine.
2. Hands you a `CancellableContinuation<T>` (`cont`).
3. Resumes the caller when you call `cont.resume(value)` or `cont.resumeWithException(e)`.
4. Calls a registered `invokeOnCancellation { … }` block if the parent coroutine is cancelled — letting you deregister the callback cleanly.

```kotlin
suspend fun fetchUser(id: UserId): User = suspendCancellableCoroutine { cont ->
    val request = api.fetchUser(id, object : Callback<User> {
        override fun onSuccess(user: User) { cont.resume(user) }
        override fun onError(e: Throwable)  { cont.resumeWithException(e) }
    })
    cont.invokeOnCancellation { request.cancel() }
}
```

The `invokeOnCancellation` hook is the key part. Without it, cancelling the calling coroutine leaks the callback — the third-party API keeps holding a reference until it fires (which may be never).

**Prefer `suspendCancellableCoroutine` over `suspendCoroutine`.** Both exist; the non-cancellable variant has no `invokeOnCancellation` hook and shouldn't be used for anything that owns external resources.

**For event-style (many-shot) callbacks: `callbackFlow`.**

```kotlin
fun sensorReadings(): Flow<Reading> = callbackFlow {
    val listener = object : SensorListener {
        override fun onReading(r: Reading) { trySend(r) }
    }
    sensor.register(listener)
    awaitClose { sensor.unregister(listener) }
}
```

`callbackFlow` gives you a `Flow<T>` whose emissions come from callbacks. The `awaitClose` block runs when the flow is cancelled — that's where deregistration goes.

**Resume exactly once.** A `CancellableContinuation` can only be resumed once (otherwise `IllegalStateException`). If your callback might fire multiple times, you have an event-stream — use `callbackFlow`, not `suspendCancellableCoroutine`.

## Decision heuristics

- One-shot callback (success or failure, fires once) → `suspendCancellableCoroutine`.
- Many-shot callback (events arriving over time) → `callbackFlow`.
- Always register a cancellation handler (`invokeOnCancellation` / `awaitClose`) that deregisters the callback.
- Test the wrapper by cancelling the calling coroutine and asserting the underlying callback was deregistered.

## Anti-patterns

- Forgetting `invokeOnCancellation` — when the caller cancels, the callback lingers indefinitely. Memory leak.
- Using `suspendCoroutine` (non-cancellable variant) for anything that owns external resources — no chance to clean up.
- Resuming the continuation more than once — throws and crashes the coroutine.
- Wrapping a stream of events with `suspendCancellableCoroutine` (one-shot) — silently drops every emission after the first.
- Calling third-party code that runs the callback on a different thread without considering whether the receiving coroutine context cares (most don't, but UI threads do).

## See also

- `kp-coroutine-scope` — the scope that owns the lifecycle of the wrapped call.
- `kp-flow-cold-vs-hot` — `callbackFlow` produces a cold `Flow`.
- `kp-anti-patterns` — registering callbacks without paired unregistration is a classic Kotlin smell.

## References

- *Kotlin Coroutines* (Marcin Moskała) — chapter on `suspendCancellableCoroutine` and bridging.
- Kotlin coroutines official guide — coroutine cancellation; `callbackFlow` documentation.
