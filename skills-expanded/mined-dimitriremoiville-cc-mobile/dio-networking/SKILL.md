---
name: dio-networking
description: Networking patterns for this Flutter project — dio configuration, auth interceptor, the generated OpenAPI client package, DTO → entity mappers, repository error mapping to Failure. Load whenever writing or editing a network call, interceptor, or API client wrapper.
---

# dio + generated API client

## The pipeline

```
domain.Repository              # domain types only, returns Either<Failure, T>
      ↓
data.RepositoryImpl            # calls generated client, maps DTOs, handles errors
      ↓
packages/<api_client>          # OpenAPI-generated; exports Api classes + DTOs
      ↓
Dio (configured in core/network)
```

**Repositories never touch `Dio` directly** — they call the generated API client. `Dio` only shows up in `core/network/dio_factory.dart` and the error handling mixin.

## DioFactory

```dart
// core/network/dio_factory.dart
class DioFactory {
  const DioFactory({
    required this.config,
    required this.authTokenProvider,
    required this.logger,
  });
  final AppConfig config;
  final AuthTokenProvider authTokenProvider;
  final ILogger logger;

  Dio create() {
    final dio = Dio(BaseOptions(
      baseUrl: config.apiBaseUrl,
      connectTimeout: const Duration(seconds: 10),
      receiveTimeout: const Duration(seconds: 30),
      sendTimeout: const Duration(seconds: 30),
      headers: {'Accept': 'application/json'},
    ));

    dio.interceptors.addAll([
      _AuthInterceptor(authTokenProvider),
      _RefreshInterceptor(dio, authTokenProvider, logger),
      if (config.isDebug) LogInterceptor(requestBody: true, responseBody: true),
    ]);

    return dio;
  }
}
```

Rules:
- **One `Dio` per app.** Register as a singleton; pass it to the generated API client's constructor.
- Interceptors do one thing each. `_AuthInterceptor` attaches the Bearer token. `_RefreshInterceptor` handles 401s by refreshing and retrying once (then throws if refresh fails).
- `LogInterceptor` only in debug. Never in release.
- No business logic inside interceptors — only transport concerns.

## AuthTokenProvider

```dart
abstract interface class AuthTokenProvider {
  Future<String?> currentToken();
  Future<String?> refresh();
  Future<void> clear();
  Stream<AuthFailureReason> get failureStream;  // emits when refresh fails
}
```

- Stored in `core/auth/`.
- Backed by `flutter_secure_storage`.
- `failureStream` lets `AuthBloc` react to implicit sign-outs (refresh-token expired mid-call).

## Generated API client usage

The generated package (`bdi_interventions_api_client`-style) exposes one `Api` class per tag:

```dart
final api = AuthenticationApi(dio, serializers);
final response = await api.postApiAuthLogin(body: JsonObject({'email': email, 'password': password}));
final UserDto dto = response.data?.user;
```

Rules:
- **Repositories depend on the Api classes, not on `Dio`.** Inject the `AuthenticationApi` through GetIt.
- **Hide conflicting names at import time:**
  ```dart
  import 'package:bdi_interventions_api_client/bdi_interventions_api_client.dart' hide User;
  ```
  Your domain `User` now wins.
- **Always map to domain types before returning.** The generated DTO never crosses into `presentation/`.

## Repository with error handling

```dart
// data/repositories/activity_repository_impl.dart
final class ActivityRepositoryImpl
    with ApiCallErrorHandling
    implements ActivityRepository {
  ActivityRepositoryImpl({required ActivitiesApi api, required ActivityDao dao})
      : _api = api, _dao = dao;

  final ActivitiesApi _api;
  final ActivityDao _dao;

  @override
  Future<Either<Failure, Activity>> getActivity(String id) => handleApiCall(
        () => _api.getActivity(id: id),
        map: (dto) => dto.toDomain(),
      );

  @override
  Stream<Either<Failure, Activity>> watchActivity(String id) =>
      _dao.watchActivity(id).map((row) => row == null
          ? Left(const NotFoundFailure(message: 'activity not found'))
          : Right(row.toDomain()));
}
```

## ApiCallErrorHandling mixin

```dart
// core/network/api_call_error_handling.dart
mixin ApiCallErrorHandling {
  Future<Either<Failure, T>> handleApiCall<R, T>(
    Future<Response<R>> Function() call, {
    required T Function(R dto) map,
  }) async {
    try {
      final response = await call();
      final data = response.data;
      if (data == null) return Left(const UnknownFailure(message: 'empty response'));
      return Right(map(data));
    } on DioException catch (e, s) {
      return Left(_mapDioException(e, s));
    } catch (e, s) {
      return Left(UnknownFailure(message: e.toString(), rootCause: e, stackTrace: s));
    }
  }

  Failure _mapDioException(DioException e, StackTrace s) => switch (e.type) {
        DioExceptionType.cancel             => const CancelledFailure(),
        DioExceptionType.connectionTimeout ||
        DioExceptionType.receiveTimeout    ||
        DioExceptionType.sendTimeout       ||
        DioExceptionType.connectionError    => NetworkFailure(rootCause: e, stackTrace: s),
        DioExceptionType.badCertificate     => NetworkFailure(message: 'SSL error', rootCause: e, stackTrace: s),
        DioExceptionType.badResponse        => _mapStatus(e, s),
        DioExceptionType.unknown            => UnknownFailure(message: e.message ?? 'unknown', rootCause: e, stackTrace: s),
      };

  Failure _mapStatus(DioException e, StackTrace s) {
    final status = e.response?.statusCode ?? 0;
    final body = e.response?.data;
    return switch (status) {
      400 => ValidationFailure(message: _extractMessage(body), fields: _extractFields(body)),
      401 || 403 => AuthFailure(code: status.toString(), rootCause: e, stackTrace: s),
      404 => NotFoundFailure(message: _extractMessage(body), code: '404'),
      409 => ServerFailure(message: _extractMessage(body), code: '409', rootCause: e, stackTrace: s),
      429 => RateLimitFailure(retryAfter: _extractRetryAfter(e.response!.headers)),
      >= 500 => ServerFailure(message: _extractMessage(body), code: status.toString(), rootCause: e, stackTrace: s),
      _ => UnknownFailure(message: _extractMessage(body), rootCause: e, stackTrace: s),
    };
  }
}
```

## DTOs and mappers

- DTOs come from the generated client package. No hand-rolled DTOs in the app unless the API client is missing a shape (rare).
- Mappers are one-way (DTO → entity) and live under `data/mappers/`.
- For polymorphic DTOs (`oneOf`), switch on the discriminator in the mapper.

## Connectivity

- Use `connectivity_plus` in `core/network/` — check "am I online?" only to short-circuit optional background work. **Don't** gate user-triggered calls on connectivity checks; let the call fail and map to `NetworkFailure`.

## Caching

Caching is a repository concern, not an interceptor concern. Two good patterns:

1. **Drift-backed cache** — repo writes to drift on success, reads from drift when offline or stale. TTL on the row.
2. **`dio_cache_interceptor`** — for purely idempotent GETs where the response can be cached verbatim. Don't use it for auth-sensitive endpoints.

Avoid "in-memory Map in the repo" shortcuts — they leak, they're invisible to debuggers, and they confuse test setup.

## Don'ts

- `try { dio.get(...) } catch (e) { ... }` in any file that isn't the error-mapping mixin.
- Hard-coded base URLs. Always through `AppConfig`.
- `Interceptor`s doing business logic (counting requests, emitting analytics, deciding whether to re-auth beyond a simple token refresh).
- Multiple `Dio` instances. One per app.
- Exposing the generated DTO type on a domain repository signature.
