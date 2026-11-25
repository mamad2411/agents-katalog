---
name: openapi-generation
description: Generate a typed Dart Dio client from an OpenAPI 3.x spec — `openapi-generator-cli` setup, generated DTO discipline, repository wrapping, regen workflow, CI enforcement. Load whenever touching generated API client code or adding a new endpoint.
---

# OpenAPI -> Dio client

## Why generate

A hand-written `Dio` service layer drifts from the server. Types for headers, query params, request/response bodies go stale silently. A generated client:
- Re-derives DTOs + endpoint methods from the spec on every build.
- Is immediately out of date (in a good way) when the server ships a breaking change — compile error, not runtime 500.
- Centralizes serialization on the spec rather than per-endpoint.

## Tooling

Use **openapi-generator-cli** (the community one) via a local `build.yaml` runner, or the `openapi_generator` Dart package that wraps it.

Install the CLI (npm one-shot):

```bash
npm install -g @openapitools/openapi-generator-cli
```

Or run it as a `dart run` script via the `openapi_generator` package.

## Generation config

`openapi-generator.yaml`:

```yaml
generatorName: dart-dio
outputDir: lib/generated/api
inputSpec: api/openapi.yaml
additionalProperties:
  pubName: api_client
  pubLibrary: api_client
  useEnumExtension: true
  serializationLibrary: json_serializable
  dateLibrary: core
  nullableFields: true
```

Generate:

```bash
openapi-generator-cli generate -c openapi-generator.yaml
cd lib/generated/api && dart pub get && dart run build_runner build --delete-conflicting-outputs && cd -
```

Automate via `make api` or a `tool/` script.

## Layout

```
api/
  openapi.yaml              # the spec, committed
lib/
  data/
    datasources/
      orders_remote_source.dart
    repositories/
      orders_repository_impl.dart
  generated/
    api/                    # the entire generated pub package — committed
```

Commit the generated code. PR diffs on server changes become reviewable, CI doesn't need the generator, and IDE analysis is instant.

## Wire the client

One `Dio` instance per flavor, in the composition root. Pass it to the generated `ApiClient`:

```dart
final dio = Dio(BaseOptions(baseUrl: env.apiBaseUrl))
  ..interceptors.add(LogInterceptor(responseBody: !kReleaseMode))
  ..interceptors.add(AuthInterceptor(tokenStore: sl()))
  ..interceptors.add(RetryInterceptor());

final api = OpenApi(dio: dio);
```

`OpenApi` exposes typed API groups (`api.getOrderApi()`, etc.).

## Remote data source wrapper

The generated types stay behind `data/`. `OrdersRemoteSource` hides the generator:

```dart
class OrdersRemoteSource {
  OrdersRemoteSource(this._api);
  final OrderApi _api;

  Future<OrderDTO> fetchOne(String id) async {
    final response = await _api.getOrderById(id: id);
    return response.data!; // generated non-null wrapper
  }

  Future<List<OrderDTO>> list({int page = 0, int size = 20}) async {
    final response = await _api.listOrders(page: page, size: size);
    return response.data?.toList() ?? const [];
  }
}
```

Generated DTOs (`OrderDTO`, etc.) map to domain entities at the repository:

```dart
class OrdersRepositoryImpl implements OrdersRepository {
  OrdersRepositoryImpl(this._source);
  final OrdersRemoteSource _source;

  @override
  Future<Either<Failure, Order>> getOne(String id) async {
    try {
      final dto = await _source.fetchOne(id);
      return Right(dto.toDomain());
    } on DioException catch (e) {
      return Left(e.toFailure());
    }
  }
}
```

## Regen workflow

- Spec lives in `api/openapi.yaml`. Version-controlled, reviewable.
- A Makefile target `make api` runs `openapi-generator-cli generate && cd lib/generated/api && dart pub get && dart run build_runner build --delete-conflicting-outputs`.
- CI step verifies no drift: `make api && git diff --exit-code lib/generated/api`.

When the spec changes, you:
1. Pull the updated `openapi.yaml`.
2. `make api`.
3. Fix the breaks in `data/` wrappers. The repository contracts stay the same.
4. Update domain mappers if a field name/type changed.

## Error mapping

Dio throws `DioException` on non-2xx. Map at the repository boundary:

```dart
extension _DioFailure on DioException {
  Failure toFailure() {
    if (type == DioExceptionType.cancel) return const CancelledFailure();
    if (type == DioExceptionType.connectionTimeout || type == DioExceptionType.receiveTimeout) return const TimeoutFailure();
    if (response?.statusCode == 401) return const UnauthorizedFailure();
    if (response?.statusCode == 404) return const NotFoundFailure();
    if ((response?.statusCode ?? 0) >= 500) return ServerFailure(statusCode: response!.statusCode!);
    return NetworkFailure(message: message ?? 'Unknown');
  }
}
```

Domain speaks `Failure`. Never surfaces `DioException`.

## Testing

Mock at the `OrdersRemoteSource` boundary, not at `Dio`:

```dart
class FakeOrdersRemoteSource implements OrdersRemoteSource {
  @override Future<OrderDTO> fetchOne(String id) async => OrderDTO(id: id, /* ... */);
  @override Future<List<OrderDTO>> list({int page = 0, int size = 20}) async => const [];
}
```

Generated `OrderDTO` is constructable, so test fixtures are trivial.

For lower-level coverage of your interceptors, use `DioAdapter` from the `http_mock_adapter` package.

## Enum extensions

`useEnumExtension: true` generates a `X.values.firstWhereOrNull((e) => e.name == raw)` extension so unknown server values parse to `null` instead of throwing. Handle `null` at the mapper.

## Hard nos

- No hand-written API methods alongside generated ones for the same endpoint — pick one surface.
- No leaking generated DTOs (`OrderDTO`) into the domain layer. Map at the repository.
- No `dynamic` return types from `data/` to domain.
- No committing a `lib/generated/` that doesn't match the committed `openapi.yaml` (CI catches).
- No `catch (_)` at the data-source layer. Typed catch, mapped to `Failure`.
