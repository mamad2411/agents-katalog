---
name: kmm-testing
description: Testing patterns for the shared Kotlin Multiplatform module — `kotlin.test` + `kotlinx-coroutines-test`. Covers use cases, ViewModels, Ktor repositories (with MockEngine), and how to keep tests running on both JVM and iOS simulator targets.
---

# KMM testing

## Stack

- **Assertions:** `kotlin.test` (`assertEquals`, `assertTrue`, `assertFailsWith`, `assertIs`, `assertNotNull`).
- **Coroutines:** `kotlinx-coroutines-test` (`runTest`, `TestDispatcher`, `advanceUntilIdle`).
- **Ktor:** `MockEngine` from `ktor-client-mock` — multiplatform, no real network.

This skill deliberately stays within those two (plus `MockEngine` when the test touches an `HttpClient`). MockK is JVM-only — don't reach for it in `commonTest`.

## Where tests live

```
shared/src/commonTest/       # runs on every target — default home
shared/src/androidUnitTest/  # JVM-only; okay to use MockK / JUnit here
shared/src/iosTest/          # iOS-only; rarely needed
```

Default to `commonTest`. Promote a test to a platform test set only when the code under test is also platform-specific.

## Use case tests

```kotlin
import kotlin.test.*
import kotlinx.coroutines.test.runTest

class GetOrderUseCaseTest {
    private val repo = FakeOrderRepository()
    private val useCase = GetOrderUseCase(repo)

    @Test
    fun returnsOrderWhenRepositoryAccepts() = runTest {
        repo.nextResult = Result.success(SAMPLE_ORDER)

        val result = useCase(OrderId("42"))

        assertTrue(result.isSuccess)
        assertEquals(SAMPLE_ORDER, result.getOrThrow())
    }

    @Test
    fun returnsFailureWhenRepositoryRejects() = runTest {
        repo.nextResult = Result.failure(DomainError.Network)

        val result = useCase(OrderId("42"))

        assertIs<DomainError.Network>(result.exceptionOrNull())
    }
}
```

## ViewModel tests

ViewModels use `viewModelScope`, which requires `Dispatchers.Main` to be set. Use `Dispatchers.setMain(dispatcher)` in `@BeforeTest`, reset in `@AfterTest`. This works in `commonTest` on both JVM and Native (the Native test runtime supports it).

```kotlin
class OrderViewModelTest {
    private val dispatcher = StandardTestDispatcher()

    @BeforeTest fun setUp() { Dispatchers.setMain(dispatcher) }
    @AfterTest fun tearDown() { Dispatchers.resetMain() }

    @Test
    fun loadTransitionsToSuccess() = runTest(dispatcher) {
        val submit = FakeGetOrderUseCase(Result.success(SAMPLE_ORDER))
        val vm = OrderViewModel(submit)

        vm.onAction(OrderAction.Load(OrderId("42")))
        advanceUntilIdle()

        assertIs<OrderUiState.Success>(vm.state.value)
    }

    @Test
    fun loadTransitionsToError() = runTest(dispatcher) {
        val submit = FakeGetOrderUseCase(Result.failure(DomainError.Network))
        val vm = OrderViewModel(submit)

        vm.onAction(OrderAction.Load(OrderId("42")))
        advanceUntilIdle()

        assertIs<OrderUiState.Error>(vm.state.value)
    }
}
```

Pattern:
- `StandardTestDispatcher` (not `UnconfinedTestDispatcher`) for realistic scheduling.
- `runTest(dispatcher)` drives the same test dispatcher.
- `advanceUntilIdle()` after triggering work; then assert.
- No Turbine needed — `state.value` is the current StateFlow value.

## Ktor repository tests (MockEngine)

```kotlin
@Test
fun getOrderMapsDtoToDomain() = runTest {
    val engine = MockEngine { request ->
        assertEquals("/orders/42", request.url.encodedPath)
        respond(
            content = """{"id":"42","items":[],"totalCents":1999,"createdAt":"2026-04-22T00:00:00Z"}""",
            status = HttpStatusCode.OK,
            headers = headersOf(HttpHeaders.ContentType, "application/json"),
        )
    }
    val http = HttpClient(engine) {
        install(ContentNegotiation) { json(Json { ignoreUnknownKeys = true }) }
    }
    val repo = OrderRepositoryImpl(OrderApi(http), io = StandardTestDispatcher(testScheduler))

    val result = repo.getOrder(OrderId("42"))

    assertTrue(result.isSuccess)
    assertEquals(OrderId("42"), result.getOrThrow().id)
}
```

MockEngine lets you assert on the request and script the response — everything stays in `commonTest`.

## Hand-rolled fakes

```kotlin
class FakeOrderRepository : OrderRepository {
    var nextResult: Result<Order> = Result.failure(IllegalStateException("not set"))
    val submittedIds = mutableListOf<OrderId>()

    override suspend fun getOrder(id: OrderId): Result<Order> {
        submittedIds += id
        return nextResult
    }
}
```

- Add state only as the test needs.
- Spy on calls by recording them.
- Don't reach for MockK in `commonTest`.

## Rules of thumb

- **One concept per test.** Long tests with five loosely-related assertions are a smell.
- **No real IO.** Ktor: MockEngine. SQLDelight: skip or use its in-memory driver in `commonTest`. No real filesystem.
- **Deterministic time.** Inject a `Clock` (`kotlinx.datetime.Clock`) or `() -> Instant`; don't call `Clock.System.now()` in production without a seam.
- **Name tests as sentences.** `returnsOrderWhenRepositoryAccepts()`.
- **`commonTest` first.** Promote out only when necessary.

## Run tests

```bash
./gradlew :shared:allTests                  # JVM + iOS simulator
./gradlew :shared:jvmTest                   # JVM-only
./gradlew :shared:iosSimulatorArm64Test     # Apple Silicon simulator
./gradlew :shared:jvmTest --tests 'com.example.GetOrderUseCaseTest'
```

## Don'ts

- No JUnit imports in `commonTest` — use `kotlin.test.*`.
- No `MockK` in `commonTest` — it's JVM-only.
- No `Thread.sleep` or bare `delay` outside `runTest`.
- No `runBlocking` — use `runTest`.
- No test depending on another test's side effects.
