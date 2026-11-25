---
name: retrofit-networking
description: Project-specific Retrofit + OkHttp + kotlinx.serialization conventions — the `toOutcome(::toDomainError)` rule at the repository boundary, the shared-`OkHttpClient`-with-Coil pattern, debug-only logging, and the `ignoreUnknownKeys = true` rationale. Load when adding or editing any API call, interceptor, or serializer.
---

# Networking (project delta)

For Retrofit / OkHttp / kotlinx.serialization fundamentals — `@GET`/`@POST` annotations, suspend functions, converter factory setup, `Interceptor` mechanics — read the [Retrofit docs](https://square.github.io/retrofit/) and the [OkHttp docs](https://square.github.io/okhttp/). The canonical templates for `NetworkModule`, `SampleApi`, and `OrderRepositoryImpl` live in `.claude/skills/android-app-skeleton/references/core-data.md`. This file documents only the project's specific decisions.

## When this applies

Retrofit + OkHttp + kotlinx.serialization. On an existing app:

- **Ktor client** (`io.ktor.client.*`) → skip; Ktor's plugin model is different. Apply only the principles below: one shared HTTP client with image loading, DTOs separated from domain, error mapping at the repository boundary.
- **Apollo GraphQL** (`com.apollographql.apollo3`) → GraphQL types replace REST DTOs; the `runCatching → toOutcome` wrap still applies.
- **Moshi or Gson** → don't migrate; adapt the converter setup to the existing serializer.
- **Retrofit without Hilt** → wiring is the same, hand-roll the singleton instead of `@Provides`.

## The pipeline

```
<feature>/domain/Repository       returns Outcome<DomainType>
   ↑
<feature>/data/RepositoryImpl     calls API, maps DTO → domain, lifts via toOutcome
   ↓
<feature>/data/remote/Api         Retrofit interface — suspend, returns DTO
   ↓
core/data/network/OkHttpClient    interceptors, timeouts, logging — provided once, shared with Coil
```

## Repository boundary — `toOutcome(::toDomainError)`

The single most important rule in this skill:

```kotlin
override suspend fun getOrder(id: OrderId): Outcome<Order> = withContext(io) {
    runCatching { api.getOrder(id.raw).toDomain() }.toOutcome(::toDomainError)
}
```

- **`withContext(io)` in the repository, not the ViewModel.** The repository owns its concurrency policy; the VM just launches into `viewModelScope`.
- **`runCatching { ... }.toOutcome(::toDomainError)`** — the canonical helpers in `core/data/network/Outcomes.kt`. `toOutcome` rethrows `CancellationException`; open-coded `runCatching { ... }.fold(...)` swallows it and silently breaks coroutine cancellation. The reviewer flags this every time.
- **`HttpException` / `IOException` never escape `data/`.** They map to `DomainError.Network` / `Unauthorized` / `NotFound` / `Server` / `Unknown` inside `toDomainError`.

Why not `Result<T>` all the way up? (a) `Result.failure` requires a `Throwable`, which forces `DomainError` to extend `Throwable` and leaks an exception type into the domain; (b) `runCatching` swallows `CancellationException`. `toOutcome` does both correctly in one place.

### Feature-local mapper

When a feature has a custom error envelope (e.g. an `OrderConflictException` distinct from a 409), pass a feature-local mapper instead of editing the global `toDomainError`:

```kotlin
private fun toOrderError(t: Throwable): DomainError = when (t) {
    is OrderConflictException -> DomainError.Server(409, t)
    else -> toDomainError(t)
}

runCatching { api.getOrder(id.raw).toDomain() }.toOutcome(::toOrderError)
```

## Service definitions

Project rules on top of standard Retrofit:

- **Always `suspend`.** No `Call<T>`, no `Single<T>`, no `Observable<T>`. The reviewer flags non-suspend service methods.
- **Return the DTO directly.** Let Retrofit throw `HttpException` on non-2xx; the repository catches it.
- **Typed `@Path`/`@Query`/`@Body`.** Avoid `@Body Map<String, Any>` — define a typed request class.

## DTOs

- **Suffix `Dto`**, kept in `<feature>/data/remote/`.
- `@Serializable` (kotlinx.serialization). Use `@SerialName("snake_case_name")` for fields whose wire name differs from the Kotlin name.
- **Nullability reflects the wire format**, not what the domain wants. Map nullable wire fields to domain defaults in the `toDomain()` mapper.
- One-way `DtoX.toDomain(): X` mapper colocated with the DTO. **Never expose DTOs beyond `data/`.** Promote to a `mapper/` package only when several DTOs map to the same domain type.

## OkHttp configuration (project shape)

- **One `OkHttpClient` singleton** shared between Retrofit and Coil. Coil's `OkHttpNetworkFetcherFactory` (wired in `{{APP_CLASS}}.newImageLoader`) reuses this client so any future `AuthInterceptor` reaches image requests automatically.
- **Logging only in `BuildConfig.DEBUG`.** `Level.BODY` in release would leak PII into Logcat. The scaffold's `NetworkModule` already gates this — don't remove the guard.
- **Auth header via `Interceptor`**, reading from a token store. Never put the token in the URL.

## kotlinx.serialization configuration

```kotlin
Json {
    ignoreUnknownKeys = true   // critical — a new server field must not break parsing
    explicitNulls = false      // omit nulls when serializing
    coerceInputValues = true   // missing → use default rather than throwing
}
```

The Retrofit converter is `com.squareup.retrofit2:converter-kotlinx-serialization` (Retrofit 2.10+). The older `com.jakewharton.retrofit:retrofit2-kotlinx-serialization-converter` artifact does **not** export `asConverterFactory` and is incompatible with the scaffolded `NetworkModule`. See `.claude/skills/android-app-skeleton/references/root-files.md` → "Compatibility traps" for the symptom.

## Hard nos

- **No open-coded `runCatching { ... }.fold(...)`** at any data-layer boundary — use `toOutcome(::toDomainError)`.
- **No `HttpException` / `IOException` leaking out of `data/`.**
- **No `Result<T>`** in any `domain/` interface signature — `Outcome<T>` only.
- **No `HttpLoggingInterceptor` at `Level.BODY` reachable in release.**
- **No Retrofit instance per call.** It's a `@Singleton`; building it is expensive.
- **No `Call<T>` / `Single<T>` / `Observable<T>`** on Retrofit services — `suspend` only.
