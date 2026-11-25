---
name: dart-type-system
description: 深入理解 Dart 类型系统（基本类型、泛型、Record、别名），确保类型安全和代码健壮性。
metadata:
  model: deepseek-v4-pro
  last_modified: 2026-05-10T08:36:19.588646Z
---
# Applying Type Safety and Generics in Dart

## Contents

- [Built-in Types](#built-in-types)
  - [Numbers](#numbers)
  - [Strings](#strings)
  - [Booleans](#booleans)
- [Records](#records)
  - [Declaration and Fields](#declaration-and-fields)
  - [Destructuring](#destructuring)
  - [Equality and Use Cases](#equality-and-use-cases)
- [Generics](#generics)
  - [Generic Classes](#generic-classes)
  - [Generic Methods](#generic-methods)
  - [Type Constraints](#type-constraints)
  - [Covariance and Contravariance](#covariance-and-contravariance)
- [Type Aliases (Typedef)](#type-aliases-typedef)
  - [Inline Type Alias](#inline-type-alias)
  - [Function Type Alias](#function-type-alias)
- [Dart Type System](#dart-type-system)
  - [Static vs Runtime Types](#static-vs-runtime-types)
  - [Type Promotion](#type-promotion)
  - [Type Inference](#type-inference)
- [Workflow: Refactoring a Function to a Type-Safe Generic Version](#workflow-refactoring-a-function-to-a-type-safe-generic-version)
- [Examples](#examples)

## Built-in Types

Dart provides four primitive built-in types essential for most programs. Use them directly with literals and built-in methods.

### Numbers

`int` — platform-dependent 64‑bit integer (native) or 53‑bit integer (web).  
`double` — 64‑bit IEEE 754 floating‑point.  
Both are subtypes of `num`, which offers operators (`+`, `-`, `*`, `/`) and methods like `abs()`, `ceil()`, `floor()`.

**Literals:**
```dart
var i = 42;
var hex = 0xDEADBEEF;
var d = 3.14;
var exp = 1.42e5;
var both = 1;            // int
double d2 = 1;           // automatically converts to double (1.0)
num n = 1;
n += 2.5;                // n now double
```

**Common properties/methods:**
```dart
var i = 7;
i.isEven;                // false
i.isOdd;                 // true
i.abs();                 // 7
i.bitLength;             // 3 (bits for 7)
0.0.isNaN;               // false
double.parse('1.1');     // 1.1
3.14159.toStringAsFixed(2); // '3.14'
```

Use `int.parse()` and `double.parse()` to convert from `String`. Use `toString()` or `toStringAsFixed(digits)` for conversion to `String`.

### Strings

`String` holds a sequence of UTF‑16 code units. Use single or double quotes.

**Literals and interpolation:**
```dart
var s1 = 'Single quotes';
var s2 = "Double quotes";
var name = 'Dash';
var greeting = 'Hello, $name';               // interpolation
var upper = '${name.toUpperCase()}';          // expression
var multi = '''
  Multi‑line
  string
''';
var raw = r'Not interpreted \n';
```

**Common properties/methods:**
```dart
'Dart'.isEmpty;            // false
'Dart'.length;             // 4
'  Dart  '.trim();         // 'Dart'
'Dart'.toUpperCase();      // 'DART'
```

Use adjacent string literals or `+` for concatenation.

### Booleans

`bool` can only be `true` or `false`. Dart forbids implicit conversion to bool — always check explicitly.

```dart
var isEmpty = ''.isEmpty;           // true
var isZero = 0 == 0;                // true
var isNull = null == null;          // true
var isNaN = (0 / 0).isNaN;          // true
```

## Records

Records are anonymous, immutable, heterogeneous, fixed‑size aggregates. (Language version ≥ 3.0)

### Declaration and Fields

**Positional fields (accessed via `$1`, `$2`, …):**
```dart
var point = (1, 2);
print(point.$1); // 1
```

**Named fields (accessed by name):**
```dart
var pair = (x: 10, y: 20);
print(pair.x);   // 10
```

Mix positional and named fields; named fields can appear in any order among themselves:
```dart
var rec = ('first', a: true, 42);
print(rec.$1);   // 'first'
print(rec.a);    // true
print(rec.$2);   // 42  (skips named fields)
```

Record types are structural — shape (field names, order, types) determines the type. Positional field names in a type annotation are only documentation and don't affect the type:
```dart
(int x, int y) a = (1, 2);
(int a, int b) b = (3, 4);
a = b; // OK
```
Named field names **are** part of the type:
```dart
({int x, int y}) r1 = (x: 1, y: 2);
({int a, int b}) r2 = (a: 3, b: 4);
r1 = r2; // Compile‑time error – different types
```

### Destructuring

Use pattern matching to unpack records:

```dart
var json = {'name': 'Dash', 'age': 10};
(String name, int age) userInfo(Map<String, dynamic> j) =>
    (j['name'] as String, j['age'] as int);

final (name, age) = userInfo(json);  // positional destructure

({String name, int age}) info = (name: 'Dash', age: 10);
final (:name, :age) = info;          // named destructure
```

### Equality and Use Cases

Two records are equal if they have the same shape and corresponding fields compare equal. Named field order is ignored.

```dart
var a = (x: 1, y: 2);
var b = (y: 2, x: 1);
print(a == b); // true
```

Use records for multiple returns, ad‑hoc data bundles, or simple data structures without declaring a full class:

```dart
typedef ButtonItem = ({String label, Icon icon, void Function()? onPressed});
final List<ButtonItem> buttons = [
  (label: 'Save', icon: Icon(Icons.save), onPressed: () { ... }),
];
```

Later refactor to a class or extension type without changing consuming code.

## Generics

### Generic Classes

Parameterize types with angle brackets to reduce duplication and improve type safety.

```dart
abstract class Cache<T> {
  T getByKey(String key);
  void setByKey(String key, T value);
}
```

Use single‑letter names by convention: `E` (element), `T`, `S`, `K` (key), `V` (value).

### Generic Methods

Methods and top‑level functions can declare type parameters before the return type.

```dart
T first<T>(List<T> ts) {
  T tmp = ts[0];
  // ...
  return tmp;
}
```

### Type Constraints

Restrict the type parameter with `extends`. A typical bound is `Object` to forbid nullable types:

```dart
class Foo<T extends Object> { ... }
```

Use F‑bounds for self‑referential constraints:

```dart
T max<T extends Comparable<T>>(T a, T b) => a.compareTo(b) > 0 ? a : b;
```

### Covariance and Contravariance

Dart’s type system follows the **consumer**/**producer** model:

- **Consumer** (input): accept a supertype — contravariant.
- **Producer** (output): accept a subtype — covariant.

When overriding methods, return types are covariant (can be more specific), while parameter types are contravariant (can be more general). The `covariant` keyword explicitly allows overriding with a narrower parameter type, shifting the check to runtime.

```dart
class Animal {
  void chase(Animal a) {}
}
class Cat extends Animal {
  @override
  void chase(covariant Animal a) {} // a now runtime‑checked
}
```

## Type Aliases (Typedef)

A typedef gives a name to any type. Two forms exist:

### Inline Type Alias

(Dart ≥ 2.13) Alias any type, including non‑function types.

```dart
typedef IntList = List<int>;
IntList il = [1, 2, 3];

typedef ListMapper<X> = Map<X, List<X>>;
ListMapper<String> m = {}; // Map<String, List<String>>
```

### Function Type Alias

Useful when a function signature is complex or reused. Prefer inline function types in new code.

```dart
typedef Compare<T> = int Function(T a, T b);

int sort(int a, int b) => a - b;
void main() {
  assert(sort is Compare<int>); // true
}
```

## Dart Type System

### Static vs Runtime Types

Every expression has a **static type** known at compile time and a **runtime type** of the actual object. Dart enforces that the runtime type always conforms to the static type (soundness) through a combination of compile‑time checks and runtime checks.

```dart
num value = 42;       // static: num, runtime: int
value = 3.14;         // OK (compiler accepts), runtime double
(value as int).isEven; // runtime check: throws if value is double
```

### Type Promotion

After an `is` check or a null check, the static type of a local variable is automatically promoted to a more specific type within the guarded block.

```dart
void printLength(Object obj) {
  if (obj is String) {
    // obj promoted to String
    print(obj.length);
  }
}
```
Nullable variables are promoted to non‑nullable:

```dart
String? maybe;
if (maybe != null) {
  print(maybe.length); // maybe promoted to String
}
```

### Type Inference

Dart infers types for `var`/`final` declarations, collection literals, and generic type arguments, reducing annotation noise.

```dart
var x = 5;                  // int
final items = [3.0];        // List<double>
var map = {'a': 1, 'b': 2}; // Map<String, int>
```

Top‑level inference combines downward context (expected type) and upward information (expression type).

Generic argument inference uses both context and argument types. With **inference using bounds** (Dart ≥ 3.7), the algorithm leverages declared bounds to produce more precise types.

```dart
var ints = [3.0].map((d) => d.toInt()); // Iterable<int>
// d inferred as double (downward), return int used to infer map<int>
```

## Workflow: Refactoring a Function to a Type-Safe Generic Version

Use this workflow when you have multiple functions that perform identical logic on different concrete types.

### Task Progress

- [ ] Identify the duplicated logic across types.
- [ ] Determine a common supertype or interface the types share.
- [ ] Create a generic function signature with a type parameter `T`.
- [ ] Add a bound `T extends ...` to restrict usable types.
- [ ] Replace concrete types in the implementation with `T`.
- [ ] Update all call sites to use the generic version.
- [ ] Write/run unit tests with at least two different types.
- [ ] Run static analysis (`dart analyze`) and fix errors.
- [ ] Run tests → Review output → Fix → Re‑run until green.

### Conditional Branching

- **Creating NEW code**: Write the generic function directly; start with `T extends Object?` and tighten bound after tests.
- **Editing EXISTING code**: Search for all callers with `grep` or IDE find‑references. After refactoring, verify each call site compiles; adjust type annotations if needed.

### Feedback Loop

1. Write minimal tests for the existing concrete functions.
2. Refactor to generic.
3. Run tests — if they pass without changes, the generic signature preserves behaviour.
4. If compilation fails due to missing methods on `T`, add the appropriate bound (e.g., `Comparable<T>`).
5. Repeat: run `dart test`, inspect failures, adjust constraints, re‑run.

## Examples

**Before – duplicated code:**

```dart
int maxInt(int a, int b) {
  return a > b ? a : b;
}

double maxDouble(double a, double b) {
  return a > b ? a : b;
}

void main() {
  print(maxInt(3, 7));       // 7
  print(maxDouble(3.1, 2.4));// 3.1
}
```

**After – generic version with constraint:**

```dart
T max<T extends Comparable<T>>(T a, T b) {
  return a.compareTo(b) > 0 ? a : b;
}

void main() {
  print(max(3, 7));           // 7
  print(max(3.1, 2.4));       // 3.1 (num inferred)
  print(max('apple', 'zoo')); // 'zoo'
}
```

**Testing the refactored function:**

```dart
void runTests() {
  assert(max(5, 2) == 5);
  assert(max(3.14, 3.14) == 3.14);
  assert(max('abc', 'xyz') == 'xyz');

  // with custom comparable
  final people = [Person('A'), Person('C'), Person('B')];
  assert(max(people[0], people[1]).name == 'C');
}

class Person implements Comparable<Person> {
  final String name;
  Person(this.name);
  @override
  int compareTo(Person other) => name.compareTo(other.name);
}
```

Run `dart analyze` and `dart run` (or `dart test`) to validate. If a type argument fails to satisfy `Comparable`, the compiler reports the error immediately, keeping your code type-safe.
