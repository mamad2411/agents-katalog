---
name: kp-testing-coroutines
description: Use when writing tests for code that uses coroutines — phrases like "runTest", "TestDispatcher", "StandardTestDispatcher", "UnconfinedTestDispatcher", "virtual time", "advanceTimeBy", "Dispatchers.setMain", "test coroutines", "kotlinx-coroutines-test". Defines the kotlinx-coroutines-test idioms for fast, deterministic tests of suspending and concurrent code — runTest, virtual time, dispatcher injection.
---

## One-line summary

Use `runTest { … }` + a `TestDispatcher` for fast, deterministic tests of coroutine code — virtual time replaces real `delay`, and dispatcher injection makes your production code testable without `runBlocking`.

## When to use this skill

- Writing unit tests for `suspend fun` or `Flow`.
- Testing time-dependent behavior (timeouts, delays, debounce, sample) without real waiting.
- Testing concurrent coroutines and their interactions.
- Replacing slow / flaky `runBlocking` test setups.

## When NOT to use this skill

- The code isn't actually suspending and no coroutines are involved — use a regular test.
- Integration tests that genuinely need real time and threads — `runBlocking` may still be appropriate (rarely).

## Core content

**`runTest { … }`** is the canonical entry point from `kotlinx-coroutines-test`. It runs your test body as a coroutine with a `TestScope` that has a `TestDispatcher` and a virtual clock.

```kotlin
@Test
fun `loads user`() = runTest {
    val repo = FakeUserRepo()
    val sut = UserUseCase(repo)
    val user = sut.load(UserId("1"))
    assertEquals("Alice", user.name)
}
```

**Virtual time.** `delay(10.minutes)` inside `runTest` completes immediately; `runTest` *skips* the delay and advances the virtual clock. Test runs in milliseconds regardless of how much in-coroutine time elapses. This is the killer feature for testing timeouts, debouncing, polling, scheduled work.

**Two TestDispatcher flavors.**

- **`StandardTestDispatcher`** (default in `runTest`) — coroutines launched in the scope are queued, not run eagerly. Use `advanceUntilIdle()` to run them, or `advanceTimeBy(d)` to advance time and run anything scheduled within that window. Reflects how production dispatchers work; preserves order.
- **`UnconfinedTestDispatcher`** — eager execution. Each new coroutine runs immediately on the calling thread until it suspends. Easier for simple tests; less faithful to real dispatcher behavior. Use when execution order doesn't matter.

**Injecting a dispatcher into production code.** Production code should accept its dispatcher as a constructor parameter (or use a `CoroutineDispatcherProvider` indirection). Tests pass the test dispatcher; production passes `Dispatchers.IO` / `Default`.

```kotlin
class UserUseCase(private val repo: UserRepo, private val io: CoroutineDispatcher) {
    suspend fun load(id: UserId): User = withContext(io) { repo.find(id) }
}
// Test: pass StandardTestDispatcher() instead of Dispatchers.IO
```

**`Dispatchers.setMain(testDispatcher)`.** For code that hardcodes `Dispatchers.Main` (mostly Android), replace it for the test:

```kotlin
@Before fun setUp() { Dispatchers.setMain(StandardTestDispatcher()) }
@After fun tearDown() { Dispatchers.resetMain() }
```

**Testing Flow.** Use `flow.toList()` to collect a finite flow, or Turbine (`app.cash.turbine`) — a popular third-party library — for richer assertion DSL on hot flows and emissions over time.

## Decision heuristics

- Default to `runTest` + `StandardTestDispatcher`. Switch to `UnconfinedTestDispatcher` only if order-dependence isn't a concern and eager execution simplifies the test.
- Inject the dispatcher into production code; don't hardcode `Dispatchers.IO` inside business logic.
- Use virtual time aggressively — `delay(10.minutes)` in a test should run in milliseconds. If your test actually sleeps, you're not in `runTest` properly.
- Prefer `runTest` over `runBlocking` for test code — `runBlocking` blocks a real thread and doesn't honour the test scope.

## Anti-patterns

- `runBlocking` inside tests — slow, no virtual time, no test-scope cancellation.
- Hardcoding `Dispatchers.IO` / `Dispatchers.Main` inside production code so tests can't substitute — make dispatchers injectable.
- Real `Thread.sleep` in suspending code — not cancellable, defeats virtual time.
- `GlobalScope.launch` from inside `runTest` — coroutine escapes the test scope; failure isn't observed.
- Forgetting `advanceUntilIdle()` with `StandardTestDispatcher` — queued coroutines never run; test passes incorrectly.

## See also

- `kp-coroutine-scope` — `TestScope` is a `CoroutineScope` for tests.
- `kp-dispatchers` — what `TestDispatcher` replaces during a test.
- `kp-flow-operators` — testing flow pipelines via collection or Turbine.
- `kp-anti-patterns` — runBlocking and hardcoded-dispatcher smells.

## References

- *Kotlin Coroutines* (Marcin Moskała) — chapter on testing Kotlin Coroutines.
- `kotlinx-coroutines-test` official docs.
- Turbine (`app.cash.turbine`) — popular Flow testing library.
