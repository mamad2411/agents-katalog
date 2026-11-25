---
name: dart-patterns
description: "When to activate: Dart language patterns, null safety, extensions, mixins, generics, sealed classes, records, pattern matching"
origin: zakr
metadata:
  namespace: zakr/devtools-pack
  version: 1.0.0
  category: engineering
  language: dart
  platforms: [claude-code, codex, gemini-cli, cursor, aider, windsurf]
---
# Dart Language Patterns

## Null Safety

```dart
// Nullable vs non-nullable
String name = 'Alice';     // never null
String? nickname;          // can be null

// Null-aware operators
String display = nickname ?? 'Anonymous';    // fallback
nickname?.toUpperCase();                     // safe call
nickname!.toUpperCase();                     // assert non-null (use sparingly)
nickname ??= 'Default';                      // assign if null

// Late variables (initialized before first use)
late final String config;
config = loadConfig();
```

## Records (Dart 3+)

```dart
// Positional record
(int, String) pair = (1, 'one');
print(pair.$1); // 1

// Named record
({String name, int age}) user = (name: 'Alice', age: 30);
print(user.name);

// Function returning multiple values
({double lat, double lon}) getLocation() => (lat: 51.5, lon: -0.1);
final loc = getLocation();
```

## Sealed Classes and Pattern Matching

```dart
sealed class Result<T> {}
class Success<T> extends Result<T> { final T value; Success(this.value); }
class Failure<T> extends Result<T> { final String error; Failure(this.error); }

void handle(Result<String> result) {
  switch (result) {
    case Success(:final value): print('Got: $value');
    case Failure(:final error): print('Error: $error');
  }
}

// Exhaustive switch expression
String label(Result<String> r) => switch (r) {
  Success(:final value) => value,
  Failure(:final error) => 'Error: $error',
};
```

## Extensions

```dart
extension StringX on String {
  String get capitalized => isEmpty ? this : '${this[0].toUpperCase()}${substring(1)}';
  bool get isEmail => contains('@') && contains('.');
}

extension IterableX<T> on Iterable<T> {
  T? get firstOrNull => isEmpty ? null : first;
  Map<K, T> indexBy<K>(K Function(T) key) => {for (final e in this) key(e): e};
}

// Usage
'hello'.capitalized; // 'Hello'
users.indexBy((u) => u.id);
```

## Mixins

```dart
mixin Loggable {
  void log(String message) => print('[${runtimeType}] $message');
}

mixin Serializable {
  Map<String, dynamic> toJson();
  // Classes must implement toJson
}

class UserService with Loggable, Serializable {
  @override
  Map<String, dynamic> toJson() => {};

  void fetchUser(int id) {
    log('Fetching user $id');
  }
}
```

## Generics

```dart
// Bounded generics
class Repository<T extends Entity> {
  Future<T?> findById(String id) async { ... }
  Future<List<T>> findAll() async { ... }
}

// Generic extensions
extension FutureX<T> on Future<T> {
  Future<Result<T>> toResult() async {
    try { return Success(await this); }
    catch (e) { return Failure(e.toString()); }
  }
}

// Type inference
final map = <String, List<int>>{};
map['a'] = [1, 2, 3]; // type inferred
```

## Async Patterns

```dart
// Stream transformations
Stream<int> counter() async* {
  for (int i = 0; i < 10; i++) {
    await Future.delayed(const Duration(milliseconds: 100));
    yield i;
  }
}

// async* with error handling
Stream<String> fetchPages(List<String> urls) async* {
  for (final url in urls) {
    try {
      yield await fetchUrl(url);
    } catch (e) {
      yield 'Error: $e';
    }
  }
}

// Completer for bridging callback -> Future
Future<String> callbackToFuture() {
  final completer = Completer<String>();
  someCallbackApi(
    onSuccess: completer.complete,
    onError: completer.completeError,
  );
  return completer.future;
}
```

## Functional Patterns

```dart
// where, map, fold, reduce
final total = orders
    .where((o) => o.status == 'paid')
    .map((o) => o.amount)
    .fold(0.0, (sum, a) => sum + a);

// Cascade notation
final paint = Paint()
  ..color = Colors.blue
  ..strokeWidth = 2.0
  ..style = PaintingStyle.stroke;

// Spread and collection-if
final merged = [...list1, ...list2, if (includeExtra) extraItem];
```

## Freezed-Style Immutable Models

```dart
// Manual immutable class pattern (without freezed package)
class User {
  const User({required this.id, required this.name, this.email});
  final String id;
  final String name;
  final String? email;

  User copyWith({String? id, String? name, String? email}) => User(
    id: id ?? this.id,
    name: name ?? this.name,
    email: email ?? this.email,
  );

  @override
  bool operator ==(Object other) =>
    other is User && id == other.id && name == other.name;

  @override
  int get hashCode => Object.hash(id, name);
}
```
