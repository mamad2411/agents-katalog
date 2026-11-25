---
name: "converting-ts-to-dart"
description: "Converts TypeScript to idiomatic Dart 3 code, covering syntax mapping, type system translation, async patterns, and module migration. Activates when translating TypeScript interfaces, classes, enums, generics, union types, async/await patterns, or modules to Dart; migrating frontend or Node.js logic to Flutter/Dart; converting RxJS Observables to Dart Streams; adapting TypeScript utility types to Dart equivalents; or producing idiomatic Dart 3 output (sealed classes, records, pattern matching) from TypeScript source."
metadata:
  last_modified: "2026-11-10 (GMT+8)"
---

# TypeScript to Dart 3 Conversion Guide

## Goal
Provide clear, idiomatic mappings from TypeScript syntax and patterns to modern Dart 3 equivalents. Every conversion should produce code that feels native to Dart — not a line-by-line transliteration.

## Instructions

### 1. Type System Mapping

#### 1.1 Primitive Types
TypeScript and Dart share similar primitives but with different names.

```typescript
// TypeScript
let name: string = "Zack";
let age: number = 25;
let active: boolean = true;
let items: string[] = ["a", "b"];
let pair: [string, number] = ["age", 25];
```
```dart
// Dart 3
final name = 'Zack';
final age = 25;
final active = true;
final items = ['a', 'b'];
final pair = ('age', 25); // Record instead of Tuple
```

Key mappings:
| TypeScript | Dart |
|---|---|
| `string` | `String` |
| `number` | `int` / `double` / `num` |
| `boolean` | `bool` |
| `any` | `dynamic` (avoid when possible) |
| `unknown` | `Object?` |
| `void` | `void` |
| `null` / `undefined` | `null` (Dart has no `undefined`) |
| `never` | `Never` |
| `T[]` / `Array<T>` | `List<T>` |
| `[A, B]` (Tuple) | `(A, B)` (Record) |
| `Record<K, V>` / `{ [key: string]: V }` | `Map<K, V>` |
| `Set<T>` | `Set<T>` |
| `Promise<T>` | `Future<T>` |
| `Observable<T>` | `Stream<T>` |

#### 1.2 Union Types
Dart has no direct union type. Convert using `sealed` classes for complex cases, or `Object` + pattern matching for simple ones.

```typescript
// TypeScript
type Result = Success | Failure;
type StringOrNum = string | number;
```
```dart
// Dart 3 — sealed class for ADTs
sealed class Result {}
class Success extends Result { final String data; Success(this.data); }
class Failure extends Result { final String error; Failure(this.error); }

// Simple union — use pattern matching
void process(Object value) {
  switch (value) {
    case String s: print('String: $s');
    case int n:    print('Int: $n');
  }
}
```

#### 1.3 Literal Types and Enums
```typescript
// TypeScript
type Direction = "up" | "down" | "left" | "right";
enum Status { Active = "ACTIVE", Inactive = "INACTIVE" }
```
```dart
// Dart 3 — enhanced enum
enum Direction { up, down, left, right }
enum Status {
  active('ACTIVE'),
  inactive('INACTIVE');
  final String value;
  const Status(this.value);
}
```

### 2. Interface and Type Conversion

#### 2.1 Interface → Class
Dart has no `interface` keyword. Every class implicitly defines an interface.

```typescript
// TypeScript
interface User {
  readonly id: string;
  name: string;
  email?: string;
  greet(): string;
}
```
```dart
// Dart 3 — abstract interface class
abstract interface class User {
  String get id;
  String get name;
  set name(String value);
  String? get email;
  String greet();
}
```

Or as a concrete data class (more common):
```dart
class User {
  final String id;
  String name;
  final String? email;

  User({required this.id, required this.name, this.email});

  String greet() => 'Hello, $name';
}
```

#### 2.2 Type Alias → typedef / Record
```typescript
// TypeScript
type Point = { x: number; y: number };
type Callback = (data: string) => void;
```
```dart
// Dart 3
typedef Point = ({double x, double y});
typedef Callback = void Function(String data);
```

#### 2.3 Generic Constraints
```typescript
// TypeScript
function merge<T extends object>(a: T, b: Partial<T>): T { ... }
```
```dart
// Dart has no Partial<T>. Use a copyWith method with nullable named parameters.
class Config {
  final String host;
  final int port;
  const Config({required this.host, required this.port});

  Config copyWith({String? host, int? port}) =>
      Config(host: host ?? this.host, port: port ?? this.port);
}
// Usage: base.copyWith(port: 8080) takes the place of passing a Partial<Config>.
```

### 3. Class Features

#### 3.1 Constructor Shorthand
Dart constructors are more concise than TypeScript's.

```typescript
// TypeScript
class User {
  readonly id: string;
  name: string;
  constructor(id: string, name: string) {
    this.id = id;
    this.name = name;
  }
}
```
```dart
// Dart 3 — initializing formals
class User {
  final String id;
  String name;
  User(this.id, this.name);
}
```

#### 3.2 Access Modifiers
TypeScript uses `private`/`protected`/`public`. Dart uses `_` prefix for library-private.

| TypeScript | Dart |
|---|---|
| `public` | (default, no prefix) |
| `private` | `_` prefix |
| `protected` | `_` prefix (no true protected) |
| `readonly` | `final` |
| `static` | `static` |
| `abstract` | `abstract` |

#### 3.3 Inheritance Patterns
```typescript
// TypeScript
abstract class Shape {
  abstract area(): number;
}
class Circle extends Shape {
  constructor(private radius: number) { super(); }
  area(): number { return Math.PI * this.radius ** 2; }
}
```
```dart
import 'dart:math';

// Dart 3
abstract class Shape {
  double area();
}
class Circle extends Shape {
  final double radius;
  Circle(this.radius);
  @override
  double area() => pi * radius * radius;
}
```

### 4. Functions and Async

#### 4.1 Function Syntax
```typescript
// TypeScript
const greet = (name: string, age?: number): string => {
  return age != null ? `${name} is ${age}` : name;
};
```
```dart
// Dart 3
String greet(String name, [int? age]) =>
    age != null ? '$name is $age' : name;
```

#### 4.2 Named vs Positional Parameters
TypeScript object destructuring → Dart named parameters.

```typescript
// TypeScript
function createUser({ name, age = 18 }: { name: string; age?: number }) { ... }
createUser({ name: "Zack" });
```
```dart
// Dart 3
void createUser({required String name, int age = 18}) {}

void main() => createUser(name: 'Zack');
```

#### 4.3 Async / Await
Nearly identical, but `Promise` → `Future`, `Promise.all` → `Future.wait`.

```typescript
// TypeScript
async function fetchUsers(): Promise<User[]> {
  const res = await fetch("/api/users");
  return res.json();
}
```
```dart
// Dart 3 (assumes User.fromJson(Map<String, dynamic>) as in section 2)
import 'dart:convert';

import 'package:http/http.dart' as http;

Future<List<User>> fetchUsers() async {
  final res = await http.get(Uri.parse('https://example.com/api/users'));
  final list = jsonDecode(res.body) as List<dynamic>;
  return list.cast<Map<String, dynamic>>().map(User.fromJson).toList();
}
```

#### 4.4 Stream (Observable equivalent)
```typescript
// TypeScript (RxJS)
observable$.pipe(map(x => x * 2), filter(x => x > 5)).subscribe(console.log);
```
```dart
// Dart 3
void listen(Stream<int> stream) {
  stream.map((x) => x * 2).where((x) => x > 5).listen(print);
}
```

### 5. Null Safety

Both languages support strict null checking, with similar operators.

| TypeScript | Dart | Purpose |
|---|---|---|
| `x?.prop` | `x?.prop` | Optional chaining |
| `x ?? y` | `x ?? y` | Null coalescing |
| `x!` | `x!` | Non-null assertion |
| `x?.prop ?? default` | `x?.prop ?? default` | Chaining + fallback |
| `x ??= y` | `x ??= y` | Null-aware assignment |

Key difference: Dart's null safety is **sound** — the compiler guarantees a non-nullable variable is never null at runtime. Prefer type promotion (`if (x != null)`) over the bang operator `!`.

### 6. Collections and Iteration

#### 6.1 Array → List
```typescript
// TypeScript
const nums = [1, 2, 3];
const doubled = nums.map(n => n * 2);
const evens = nums.filter(n => n % 2 === 0);
const sum = nums.reduce((a, b) => a + b, 0);
const hasNeg = nums.some(n => n < 0);
```
```dart
// Dart 3
final nums = [1, 2, 3];
final doubled = nums.map((n) => n * 2).toList();
final evens = nums.where((n) => n % 2 == 0).toList();
final sum = nums.fold(0, (a, b) => a + b);
final hasNeg = nums.any((n) => n < 0);
```

Method mapping:
| TypeScript | Dart |
|---|---|
| `.map()` | `.map().toList()` |
| `.filter()` | `.where().toList()` |
| `.reduce()` | `.fold()` (with initial value) / `.reduce()` |
| `.some()` | `.any()` |
| `.every()` | `.every()` |
| `.find()` | `.firstWhere(test, orElse: () => null)` (without `orElse` it throws `StateError`) |
| `.findIndex()` | `.indexWhere()` |
| `.includes()` | `.contains()` |
| `.flat()` | `.expand((e) => e).toList()` |
| `.push()` | `.add()` |
| `.splice()` | `.removeRange()` / `.insertAll()` |
| `[...a, ...b]` | `[...a, ...b]` |

#### 6.2 Object → Map
```typescript
// TypeScript
const config: Record<string, number> = { timeout: 30, retries: 3 };
Object.entries(config).forEach(([k, v]) => console.log(k, v));
```
```dart
// Dart 3
void logConfig() {
  final config = <String, int>{'timeout': 30, 'retries': 3};
  config.forEach((k, v) => print('$k $v'));
}
```

### 7. Pattern Matching (Dart 3 Exclusive Power)
Dart 3 pattern matching is more powerful than TypeScript's type narrowing. Lean into it during conversion.

```typescript
// TypeScript — type narrowing
function describe(shape: Shape) {
  if (shape instanceof Circle) {
    return `Circle r=${shape.radius}`;
  } else if (shape instanceof Rect) {
    return `Rect ${shape.w}x${shape.h}`;
  }
  return "Unknown";
}
```
```dart
// Dart 3 — exhaustive switch expression; Shape must be sealed and its subtypes live in the same library
sealed class Shape {}

final class Circle extends Shape {
  final double radius;
  Circle(this.radius);
}

final class Rect extends Shape {
  final double w, h;
  Rect(this.w, this.h);
}

String describe(Shape shape) => switch (shape) {
  Circle(:final radius)  => 'Circle r=$radius',
  Rect(:final w, :final h) => 'Rect ${w}x$h',
};
```

### 8. Module System

| TypeScript | Dart |
|---|---|
| `import { X } from './x'` | `import 'x.dart'` (imports all public) |
| `import * as lib from './x'` | `import 'x.dart' as lib` |
| `import { X as Y } from './x'` | No per-symbol rename. Use `import 'x.dart' as x;` and refer to `x.X`, or `import 'x.dart' show X;` to limit names |
| `export { X }` | Declarations are public by default (names starting with `_` are private). To re-export another library, use `export 'x.dart';` |
| `export default X` | No equivalent; just `import` the library |
| `import type { X }` | Not needed; Dart imports are already type-aware |

### 9. Error Handling
```typescript
// TypeScript
try {
  await riskyOp();
} catch (e: unknown) {
  if (e instanceof HttpError) { ... }
  throw e;
}
```
```dart
// Dart 3
Future<void> run() async {
  try {
    await riskyOp();
  } on HttpError {
    // handle
  } catch (_) {
    rethrow;
  }
}
```

### 10. Common Patterns Quick Reference

| TypeScript Pattern | Dart 3 Equivalent |
|---|---|
| `JSON.stringify(obj)` | `jsonEncode(obj)` |
| `JSON.parse(str)` | `jsonDecode(str)` |
| `console.log(x)` | `print(x)` (`debugPrint` is in `package:flutter/foundation.dart`) |
| `typeof x === 'string'` | `x is String` |
| `x instanceof Foo` | `x is Foo` |
| `setTimeout(fn, ms)` | `Future.delayed(Duration(milliseconds: ms), fn)` |
| `setInterval(fn, ms)` | `Timer.periodic(Duration(milliseconds: ms), (_) => fn())` |
| `Date.now()` | `DateTime.now().millisecondsSinceEpoch` (a number, like JS) |
| `Math.max(a, b)` | `max(a, b)` (from `dart:math`) |
| `Object.keys(obj)` | `map.keys.toList()` |
| `Array.from({length: n}, (_, i) => i)` | `List.generate(n, (i) => i)` |
| `str.startsWith('x')` | `str.startsWith('x')` |
| `str.split(',')` | `str.split(',')` |
| `` `Hello ${name}` `` | `'Hello $name'` |

## Constraints
* Always produce idiomatic Dart 3 — never write Java-style or TypeScript-style Dart.
* Prefer `final` over `var` when the variable is not reassigned.
* Use Records for lightweight multi-value returns; avoid creating throwaway classes.
* Use `sealed` classes for union type / ADT conversions — never fall back to raw `Object` + casting when the domain is bounded.
* Use `switch` expressions with destructuring over `if-else` chains for type narrowing.
* Preserve the original code's intent and naming conventions, adapting to Dart's `lowerCamelCase` / `UpperCamelCase` rules.
* Omit explicit type annotations where Dart's type inference handles it.
