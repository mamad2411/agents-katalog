---
name: dio
description: Dio API service standards for Flutter — abstract service contracts, a single ApiClient with interceptors, request-time auth and tenant headers, single-flight 401 refresh, idempotent retry, timeouts and CancelToken, the sealed AppError hierarchy, offline cache policy with staleness, and media upload. Load when writing data services, API clients, network setup, or error mapping.
user-invocable: false
stack: api-style/dio
paths:
  - "**/data/services/*.dart"
  - "**/data/api/*.dart"
  - "**/core/network/*.dart"
  - "**/core/error/*.dart"
---

Full standards in [dio.md](dio.md). Always-on summary:

**Service contract:**
- Every service is an `abstract interface class` contract plus a `Rest…Service` implementation. Features depend on the contract, never on `Dio`.
- Cacheable resources return `Cached<T>` from the contract — staleness reaches the UI.
- Every method takes an optional `CancelToken`; the caller binds it to provider disposal.

**ApiClient:**
- One private `_request`; `get/post/put/patch/delete` are thin wrappers. Cross-cutting concerns live in interceptors, never at call sites.
- Set all four timeouts: `connectTimeout`, `sendTimeout`, `receiveTimeout`, and an overall `.timeout()` that cancels the token.
- Auth and tenant headers are read from the token store **inside `onRequest`**, per request. Never a mutable field with a public setter, never `dio.options.headers`.
- One `QueuedInterceptor` refreshes on 401 and replays exactly once (guarded by `options.extra`); a second failure signs out.
- Retry idempotent verbs only, with exponential backoff plus jitter. POST retries only when it carries an `Idempotency-Key`.

**Errors:**
- `sealed class AppError`; convert `DioException` at the boundary exactly once, classifying with a `switch` on `DioExceptionType` and status code — never on a `toString()` substring.
- `isReportable` is a property of the error type. An expected 4xx is UI state, not a crash report.

**Offline and media:**
- Declare a `CachePolicy` per resource in a decorator. Fall back to cache only on `NetworkError`/`TimeoutError` — never on 4xx or a parse failure, so never a bare `catch`.
- Before upload: `bakeOrientation`, resize, `encodeJpg`, generated filename, `MultipartFile.fromBytes` — plus progress, cancel, and an idempotency key.

**Related:** `language/dart-models` (model shape), `state/riverpod` (provider wiring), `logging/flutter-observability` (logging).
