---
name: dart-style
description: Dart 3 idioms and conventions for this project — null safety, sealed classes and pattern matching, records, async cleanup, equality via freezed, and when to use each keyword. Load whenever writing or reviewing Dart.
---

# Dart style

Opinionated defaults for this codebase. These complement the analyzer rules, not replace them.

## Naming

- Files: `snake_case.dart`. One public type per file is the default.
- Types: `UpperCamelCase`. Variables & functions: `lowerCamelCase`. Constants: `lowerCamelCase` (Dart doesn't use SCREAMING_CASE).
- Private identifiers start with `_` (Dart's only access modifier).
- `Dto` suffix on wire types; entities use the plain noun (`User`, not `UserEntity`).

## Immutability

- `final` everywhere you can. `const` on constructors whenever values allow.
- State classes, entities, and events are **immutable**. Use `freezed` — it generates `==`, `hashCode`, `copyWith`, `toString`, and pattern-match-friendly unions.
- Collection fields default to `const []` / `const {}` — avoid `null` for "empty".

## Equality

- **Don't write `==` by hand.** Either use `freezed`, or — for pure value types that don't need unions — a `record`.
- `Equatable` is legacy here. If you see it, it predates freezed adoption.

## Null safety

- Prefer a non-nullable field with a sensible default over a nullable one.
- `required` on all non-defaulted named parameters.
- The bang operator `!` is a smell. Use `switch` with a null pattern, or `if (x case final value?)`, or `x ?? fallback`. One `!` per small function is okay; two is a code review comment.
- `late` is only for lazy init where non-null is guaranteed by construction (e.g., `late final controller = TextEditingController();`).

## Sealed classes & pattern matching

```dart
sealed class LoadResult<T> {}
final class LoadInitial<T> extends LoadResult<T> { const LoadInitial(); }
final class LoadSuccess<T> extends LoadResult<T> { const LoadSuccess(this.value); final T value; }
final class LoadError<T>   extends LoadResult<T> { const LoadError(this.failure); final Failure failure; }

String describe(LoadResult<User> r) => switch (r) {
      LoadInitial()         => 'idle',
      LoadSuccess(:final value) => 'got ${value.name}',
      LoadError(:final failure) => 'error: ${failure.message}',
    };
```

- `switch` on sealed types is exhaustive — no `default:` needed. Add one only when you want a catch-all.
- Use destructuring patterns (`:final value`) to avoid intermediate variables.
- Records for ephemeral tuples: `({String id, int count})`. Don't let them leak across layers — prefer a named type.

## Functions and constructors

- Prefer **named parameters** once you have more than two.
- Factories for validation-heavy construction: `factory OrderId.parse(String raw)`.
- Extension methods for per-type helpers (mappers, formatters). Put them in a file next to the type.

## Async

- `Future<T>` or `Stream<T>`. No `Completer` unless bridging from a callback API.
- `unawaited(foo())` when you deliberately fire-and-forget. Analysis flags bare `foo();`.
- Guard `BuildContext` across `await`:
  ```dart
  await repo.submit(...);
  if (!context.mounted) return;
  context.go(const NextRoute().location);
  ```
- Cancel subscriptions in `close()` / `dispose()`. Close sinks. Analysis enforces it.

## Error handling

- Never `catch` without typing, at least `on DioException` / `on SomeException`.
- Inside a repository: catch, map to `Failure`, return `Left`.
- Outside a repository: don't catch — let the `Either` flow.
- `rethrow` cancellation: `if (e is DioException && e.type == DioExceptionType.cancel) return Left(const CancelledFailure());`.

## Scope functions — what replaces them

Dart doesn't have Kotlin's scope functions. The usual replacements:

| Kotlin | Dart |
|---|---|
| `let { ... }` on nullable | `if (x case final v?) { ... }` |
| `apply { ... }` | cascade `..` |
| `also { ... }` | just use the variable |
| `run { ... }` | IIFE `(() { ... })()` (rare) |
| `with(x) { ... }` | extension methods |

Cascades are idiomatic:

```dart
final query = SelectQuery(table)
  ..where((t) => t.userId.equals(id))
  ..orderBy([(t) => OrderingTerm.asc(t.createdAt)])
  ..limit(20);
```

## Collections

- `List.of`, `Map.of` for shallow copies. `.unmodifiable` when you hand out references.
- `Iterable.whereType<T>()` over `.where((x) => x is T).cast<T>()`.
- Avoid `first` / `last` without a fallback — use `firstOrNull`.

## Records — when to reach for them

- Method returns multiple values that don't need a name: `(String, int)` for a parse result.
- Inline pattern bindings: `final (name, age) = parseLine(input);`.
- **Don't** use them across layer boundaries. Name your types there.

## Enums

- Dart enums can carry data and methods. Use them for closed, small sets with associated constants:
  ```dart
  enum Flavor {
    dev(apiBaseUrl: 'https://dev.example.com'),
    prod(apiBaseUrl: 'https://api.example.com');
    const Flavor({required this.apiBaseUrl});
    final String apiBaseUrl;
  }
  ```
- For richer unions (payload per variant), use a `sealed class` + `freezed`.

## Don'ts

- No `print`. Use the injected `ILogger`.
- No `new` keyword (redundant).
- No `var` in production code. `final` for locals, explicit types on fields and public APIs.
- No `dynamic` unless you're reaching into JSON you haven't typed yet. Type it and move on.
- No exceptions as control flow.
- No static state mutated at runtime.
