---
name: dart-collections-iterables
description: 使用 Dart 集合操作与可迭代工具链（List、Set、Map、Iterable），高效处理数据变换。
metadata:
  model: deepseek-v4-pro
  last_modified: 2026-05-10T08:23:49.040634Z
---
# Working with Dart Collections and Iterables

## Contents

- [Collections Overview](#collections-overview)
- [Collection Literals with Spread, If, and For](#collection-literals-with-spread-if-and-for)
- [Understanding Iterable and Lazy Evaluation](#understanding-iterable-and-lazy-evaluation)
- [Searching and Predicate Methods](#searching-and-predicate-methods)
- [Termination and Conversion: toList() vs toSet()](#termination-and-conversion-tolist-vs-toset)
- [Building a Data Processing Pipeline](#building-a-data-processing-pipeline)
- [Workflow: Implementing Collection Operations](#workflow-implementing-collection-operations)
- [Examples](#examples)

## Collections Overview

Dart's core collections serve distinct roles. Choose the type that matches your data constraints, not habit.

### Declaring Lists

Lists are ordered, indexable, and allow duplicates. Use square bracket literals.

```dart
var numbers = [1, 2, 3]; // List<int>
var constantList = const [1, 2, 3]; // Compile-time constant
```

Access elements with `[]` or `elementAt`. Lists implement `Iterable`.

### Declaring Sets

Sets are unordered, unique-element collections. Use curly braces with an explicit type argument or assign to a `Set` variable.

```dart
var halogens = <String>{'fluorine', 'chlorine', 'fluorine'}; // Set<String> with one 'fluorine'
Set<String> names = {}; // empty set
```

**Catch**: `{}` alone creates a `Map`, not a `Set`.

### Declaring Maps

Maps hold key-value pairs; keys are unique. Use map literals with `key: value`.

```dart
var gifts = {'first': 'partridge', 'second': 'turtledoves'};
```

Keys and values can be any type. Access via `[]`; missing keys return `null`.

## Collection Literals with Spread, If, and For

Dart allows control flow directly inside collection literals—no builder methods needed.

### Spread Operator (`...`)

Expands an iterable in-place. Use `...?` for null-aware expansion: if the expression is `null`, nothing is inserted.

```dart
var a = [1, 2, null];
var items = [0, ...a, 3]; // [0, 1, 2, null, 3]

List<int>? nullableList;
var safe = [0, ...?nullableList, 1]; // [0, 1]
```

### Collection If

Include elements conditionally. Works with boolean expressions and patterns (`if-case`). Supports `else`.

```dart
bool include = true;
var list = [1, if (include) 2, 3]; // [1, 2, 3]

// Pattern matching
var data = 123;
var typeInfo = [
  if (data case int i) 'Integer: $i',
  if (data case String s) 'String: $s',
];
```

### Collection For

Iterate and generate elements. Both `for-in` and traditional C-style loops are allowed.

```dart
var numbers = [1, 2, 3];
var squares = [for (var n in numbers) n * n]; // [1, 4, 9]

var descending = [for (var i = 5; i > 0; i--) i]; // [5, 4, 3, 2, 1]
```

Nest control flow elements freely inside literals.

```dart
var items = [
  for (var i in [1, 2, 3])
    if (i.isOdd) ...[i, i * 10]
]; // [1, 10, 3, 30]
```

## Understanding Iterable and Lazy Evaluation

`List` and `Set` both implement `Iterable`. Methods like `map`, `where`, `expand`, `take`, `skip`, `takeWhile`, `skipWhile` are **lazy** — they return an `Iterable` that defers all work until a terminal operation triggers iteration.

### Key Lazy Methods

- `map`: Transforms each element.
- `where`: Filters elements by predicate.
- `expand`: Maps each element to an iterable and flattens.
- `take` / `skip`: Limit or skip the first `n` elements.
- `takeWhile` / `skipWhile`: Control based on a condition.
- `fold` / `reduce`: **Eager** terminal operations that aggregate to a single value.
- `forEach`: Terminal iteration — use only for side effects, not to build new collections.

Lazy chains avoid intermediate allocations and early work.

```dart
final chain = numbers.where((n) => n > 2).map((n) => n * 10).take(3);
// No elements processed yet.
```

The chain executes only when you iterate (e.g., `toList()` or `fold`).

## Searching and Predicate Methods

These methods traverse the iterable but stop early when possible. Use them for efficient existence checks and lookups.

- `firstWhere`: Returns first element matching predicate. Throws if none, unless `orElse` is provided.
- `singleWhere`: Returns the only matching element; throws if zero or multiple matches.
- `any`: Returns `true` if at least one element satisfies the predicate (short-circuits).
- `every`: Returns `true` if all elements satisfy (short-circuits on first `false`).
- `first` / `last`: Direct access; throw on empty iterable.
- `contains`: Checks for equality-based presence.

```dart
var users = [User('Alice', 21), User('Bob', 17)];

// Safe lookup with default
var adult = users.firstWhere((u) => u.age >= 18, orElse: () => User('None', 0));

bool hasMinor = users.any((u) => u.age < 18); // true
bool allAdults = users.every((u) => u.age >= 18); // false
```

Prefer `any` over `where(...).isNotEmpty` — `any` stops after the first match, `where` would check all.

## Termination and Conversion: toList() vs toSet()

When you need a concrete collection, call a terminal method:

- `toList()`: Creates a new `List`. Preserves order and duplicates. O(n) time.
- `toSet()`: Creates a new `Set`. Removes duplicates (first occurrence kept, but `Set` is unordered). O(n) time.

**Crucial**: The lazy chain executes **only once** at this point. After consumption, the `Iterable` is “spent.” If you call `toList()` again on the same lazy iterable, it re‑evaluates from the source again, doubling work. Always store the result:

```dart
final processed = numbers.where((n) => n.isEven).map((n) => n * 2);
final list = processed.toList(); // eagerly evaluated
final set = list.toSet();        // reuses the already‑materialized list
```

If you need both derivatives, materialize once.

## Building a Data Processing Pipeline

Combine lazy operations and terminal methods into a fluent pipeline. This example filters even numbers, doubles them, skips the first, takes the next three, and sums them.

```dart
void main() {
  final numbers = [1, 2, 3, 4, 5, 6, 7, 8];
  final sum = numbers
      .where((n) => n.isEven)          // [2, 4, 6, 8] (lazy)
      .map((n) => n * 2)               // [4, 8, 12, 16]
      .skip(1)                         // [8, 12, 16]
      .take(3)                         // [8, 12, 16]
      .fold(0, (prev, n) => prev + n); // terminal: sum = 36
  print(sum); // 36
}
```

Real‑world example: Extract valid email addresses from raw strings.

```dart
class EmailAddress {
  final String address;
  EmailAddress(this.address);
}

bool isValidEmail(EmailAddress email) => email.address.contains('@');

Iterable<EmailAddress> validEmails(Iterable<String> addresses) =>
    addresses.map((a) => EmailAddress(a)).where(isValidEmail).toList();

void main() {
  final input = ['a@b.com', 'invalid', 'c@d.com'];
  final result = validEmails(input);
  print(result.map((e) => e.address).join(', ')); // a@b.com, c@d.com
}
```

## Workflow: Implementing Collection Operations

Follow this process when writing Dart collection manipulation code.

### Task Progress

- [ ] Identify the target collection type (List, Set, Map) based on order, uniqueness, and key access needs.
- [ ] Choose literal syntax or constructor; add `const` for compile‑time constants.
- [ ] Use spread (`...`/`...?`), `if`, and `for` elements to inline building logic.
- [ ] Design a lazy transformation chain with `where`, `map`, `expand`, `take`, `skip`.
- [ ] Insert search/predicate calls (`firstWhere`, `any`, `every`) to short‑circuit when needed.
- [ ] Apply a terminal operation (`toList`, `toSet`, `fold`, `reduce`) only at the end.
- [ ] Test with representative data; verify expected output.
- [ ] Refactor to avoid repeated materialization or redundant iterations.

### Conditional Branching

- **Duplicate removal needed?** Use `toSet()` or a `Set` literal. If order must be preserved, use `Set` iteration order (insertion‑order from Dart 2.0+) or manually track seen items.
- **Need indexed access?** Convert to `List` via `toList()`. Avoid repeated `elementAt(i)` on a lazy iterable—it re‑walks from the start each time.
- **Checking existence?** Use `any` instead of `where(...).isNotEmpty`.
- **Handling missing elements?** Always supply `orElse` to `firstWhere`/`singleWhere` if absence is expected; otherwise catch `StateError`.
- **Infinite iterables?** Never call `last`, `length`, or `toList()` on them; use `take` or `takeWhile` to limit.

### Feedback Loop

1. Write the pipeline as a single expression chaining lazy methods and one terminal call.
2. Run the file with `dart run` or in DartPad.
3. If the result is wrong, temporarily break the chain:
   - Insert `.toList()` after each step and print to inspect intermediate state.
   - Replace the step with a dummy `map((e) => print(e))` to see elements.
4. Adjust predicate or transformation logic.
5. Re‑run until correct.
6. Remove debug code; ensure final chain is clean and single‑terminal.

## Examples

### Example 1: Partitioning users by age

```dart
class User {
  final String name;
  final int age;
  User(this.name, this.age);
}

void main() {
  final users = [User('Alice', 21), User('Bob', 17), User('Charlie', 30)];
  
  final (minors, adults) = (
    users.where((u) => u.age < 18).toList(),
    users.where((u) => u.age >= 18).toList(),
  );
  
  print('Minors: ${minors.map((u) => u.name).join(', ')}'); // Bob
  print('Adults: ${adults.map((u) => u.name).join(', ')}'); // Alice, Charlie
}
```

### Example 2: Building a report from transaction logs

```dart
class Transaction {
  final double amount;
  final String category;
  Transaction(this.amount, this.category);
}

void main() {
  final transactions = [
    Transaction(12.0, 'food'),
    Transaction(50.0, 'transport'),
    Transaction(8.5, 'food'),
    Transaction(30.0, 'utilities'),
  ];
  
  final foodTotal = transactions
      .where((t) => t.category == 'food')
      .map((t) => t.amount)
      .fold(0.0, (sum, a) => sum + a);
  
  final summary = transactions
      .where((t) => t.amount > 10.0)
      .map((t) => '${t.category}: \$${t.amount.toStringAsFixed(2)}')
      .toList();
  
  print('Food total: \$${foodTotal.toStringAsFixed(2)}'); // $20.50
  print('Large transactions: $summary'); // [transport: $50.00, utilities: $30.00]
}
```

Use these patterns to write concise, performant Dart collection code. Always let laziness do the heavy lifting until the moment you truly need the result.
