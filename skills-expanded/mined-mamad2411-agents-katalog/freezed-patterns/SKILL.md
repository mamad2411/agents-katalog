---
name: freezed-patterns
description: `freezed` patterns for this Flutter project — sealed unions for view states / events / domain types, copyWith discipline, JSON serialization, equality semantics, guidance on when NOT to use freezed. Load whenever modeling a new state/event/domain entity or touching `.freezed.dart` generation.
---

# freezed patterns

## What we use freezed for

- **View states** — `sealed class HomeState` with variants.
- **Bloc events** — ditto.
- **Domain unions** — `Either`-like types where a `fpdart` `Either<Failure, T>` doesn't fit naturally.
- **Immutable data classes with value equality** — when we want structural equality without writing 30 lines of `==` / `hashCode`.

## What we don't use freezed for

- Simple DTOs that are just JSON-in/JSON-out and never compared — plain class with `json_serializable` is enough.
- Things with identity (entities in the DDD sense, like `User` with a stable `id`). Equality by id, not by value.

## Install

Don't hand-write versions into `pubspec.yaml` — let `dart pub add` resolve the current stable:

```bash
dart pub add freezed_annotation json_annotation
dart pub add --dev freezed build_runner json_serializable
```

**Floor constraints that matter for the patterns in this skill:**

| Package | Floor | Reason |
|---|---|---|
| `freezed` | `>= 3.0.0` | Dart 3 `@freezed sealed class ...` unions with exhaustive pattern matching (the syntax every example below uses). v2 still uses `@freezed class X with _$X` for unions and is incompatible. |
| `freezed_annotation` | `>= 3.0.0` | Must track `freezed`. |
| `json_serializable` | `>= 6.0.0` | Works with Dart 3 sealed classes. |
| `build_runner` | `>= 2.4.0` | Matches the `dart run build_runner ...` invocation used by /init-flutter-app and the codegen commands. |

If `dart pub add` resolves anything below a floor, stop and report — something is constraining resolution (an older SDK constraint, a transitive pin).

Run `dart run build_runner build --delete-conflicting-outputs` after any change.

## Sealed state (view state)

```dart
import 'package:freezed_annotation/freezed_annotation.dart';

part 'home_state.freezed.dart';

@freezed
sealed class HomeState with _$HomeState {
  const factory HomeState.idle() = HomeIdle;
  const factory HomeState.loading() = HomeLoading;
  const factory HomeState.ready({required List<Order> orders, bool refreshing = false}) = HomeReady;
  const factory HomeState.error({required String message}) = HomeError;
}
```

### In the view

```dart
final state = context.watch<HomeCubit>().state;
switch (state) {
  case HomeIdle():    return const SizedBox.shrink();
  case HomeLoading(): return const CenterSpinner();
  case HomeReady(:final orders, :final refreshing): return OrderList(orders: orders, refreshing: refreshing);
  case HomeError(:final message): return ErrorPanel(message: message);
}
```

The switch is **exhaustive** — adding a new variant becomes a compile error until you handle it. This is why we prefer this over `maybeWhen` / `when`.

### Tiny note on `when`

`when` / `maybeWhen` still work, but pattern-matching switches cover the same use cases without rebuilding bodies for every variant call. Prefer switches in new code.

## Domain union (either-like)

```dart
@freezed
sealed class FetchOutcome<T> with _$FetchOutcome<T> {
  const factory FetchOutcome.success(T value) = FetchSuccess<T>;
  const factory FetchOutcome.empty() = FetchEmpty<T>;
  const factory FetchOutcome.offline() = FetchOffline<T>;
  const factory FetchOutcome.failure(Object error) = FetchFailure<T>;
}
```

Reserve this for variants that carry different shapes. If you just have `success / failure`, use `Either<Failure, T>` from fpdart or `Result<T, E>` instead — a whole freezed file for two variants is noise.

## JSON-backed value class

```dart
@freezed
class OrderDTO with _$OrderDTO {
  const factory OrderDTO({
    required String id,
    @JsonKey(name: 'customer_id') required String customerId,
    @JsonKey(name: 'total_cents') required int totalCents,
    required String status,
    @JsonKey(name: 'created_at') required DateTime createdAt,
  }) = _OrderDTO;

  factory OrderDTO.fromJson(Map<String, Object?> json) => _$OrderDTOFromJson(json);
}
```

- `@JsonKey(name: ...)` for `snake_case` -> `camelCase`.
- `@JsonKey(defaultValue: <value>)` for fields that may be absent.
- `@JsonKey(fromJson: _parseX, toJson: _encodeX)` for bespoke parsing.

## copyWith discipline

Freezed generates `copyWith` with nullable parameters that default to `_Undefined`. Consumers read naturally:

```dart
final loaded = state.copyWith(refreshing: true);
final cleared = loaded.copyWith(orders: []);
```

To explicitly clear a nullable field, most setups require `copyWith(value: null)` with a sentinel; freezed handles this out of the box.

## Equality

Freezed generates value equality + `hashCode` based on all fields. This is exactly what you want for states. For entities with a stable id, override `==`/`hashCode` yourself or use a plain class.

## `@Default` vs required

```dart
const factory HomeState.ready({
  required List<Order> orders,
  @Default(false) bool refreshing,
}) = HomeReady;
```

Use `@Default` only when the default is semantically the "empty" or "off" case and it makes call sites cleaner. Don't default a required business parameter.

## Nested freezed + immutability

Freezed is immutable by default. Nested collections (`List<T>`) are also frozen via `UnmodifiableListView` when you return them from getters. Prefer `IList<T>` from `fast_immutable_collections` when you want equality-by-content for nested lists.

## Cost

- A freezed file adds generation time. A big file with 30 unions noticeably slows `build_runner`.
- `const` constructors work; keep them where you can.
- Avoid `@With([Mixin])` unless you truly need mixin composition — debugging generated code is not fun.

## Hard nos

- No hand-written `==` / `hashCode` / `copyWith` on a freezed class. The generator is the source.
- No `.when(...)` for switches that already have exhaustive pattern matches.
- No freezed for a single-variant class. Use a plain `final class` with `Equatable` or hand-written equality.
- No deeply nested mutable fields inside a freezed class (e.g., `final Map<String, List<Foo>>` — equality will surprise you). Use immutable collections.
- No generating code by hand ("just for one field"). Always run `build_runner`.
