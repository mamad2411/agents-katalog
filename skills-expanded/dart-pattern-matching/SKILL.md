---
name: dart-pattern-matching
description: 使用 Dart 3 的模式匹配特性（Pattern Matching）简化数据解构和分支逻辑。
metadata:
  model: deepseek-v4-pro
  last_modified: 2026-05-10T08:18:12.989121Z
---
# Mastering Pattern Matching in Dart

## Contents

- [Core Concepts](#core-concepts)
- [Pattern Types](#pattern-types)
  - [Constant Pattern](#constant-pattern)
  - [Variable Pattern](#variable-pattern)
  - [Wildcard Pattern](#wildcard-pattern)
  - [List Pattern](#list-pattern)
  - [Map Pattern](#map-pattern)
  - [Record Pattern](#record-pattern)
  - [Object Pattern](#object-pattern)
- [Logical Operators in Patterns](#logical-operators-in-patterns)
- [Relational Patterns and Guard Clauses](#relational-patterns-and-guard-clauses)
- [Switch Expressions and Exhaustiveness](#switch-expressions-and-exhaustiveness)
- [Refactoring if-else Chains](#refactoring-if-else-chains)
- [Workflow: Applying Pattern Matching](#workflow-applying-pattern-matching)
- [Examples](#examples)

## Core Concepts

A pattern describes the **shape** of a value. Use patterns to simultaneously **test** a value’s structure, **destructure** it into parts, and **bind** those parts to new variables. Patterns replace chains of `if`‑`is` checks, casts, and manual field extraction.

// Without patterns:
if (json is Map && json['user'] is List) {
  var user = json['user'] as List;
  var name = user[0] as String;
}

// With patterns:
if (json case {'user': [String name, ...]}) { ... }

A pattern can **match**, **destructure**, or **do both** depending on where it appears (declaration, assignment, switch case, loop).

## Pattern Types

### Constant Pattern

Matches when the value equals a compile‑time constant. Use for literals, `const` objects, enum values.

```dart
switch (number) {
  case 0: print('zero');
  case double.infinity: print('infinity');
  case const (1 + 2): print('three');
}
```

### Variable Pattern

Declares a new variable and binds the matched value. Use `var` or a type annotation. In a destructuring context it captures a sub‑value.

```dart
var (a, b) = (1, 2);           // a = 1, b = 2
switch ((1, 2)) {
  case (var x, var y): print('$x $y');
}
```

A typed variable pattern fails if the runtime type doesn’t match.

### Wildcard Pattern

`_` matches any value and discards it. Use to ignore positional elements or test a type without binding.

```dart
var [_, y, _] = list;          // only y bound
switch (record) {
  case (int _, String _): print('first int, second String');
}
```

### List Pattern

Destructures `List` objects by position. Must contain the exact number of elements unless a **rest element** `...` is used.

```dart
var [a, b] = [1, 2];           // exact length
var [first, ..., last] = [1, 2, 3, 4, 5]; // first=1, last=5
```

Capture unmatched elements with a rest‑element variable:

```dart
var [head, ...tail] = [1, 2, 3]; // head=1, tail=[2,3]
```

### Map Pattern

Destructures `Map` values by key. Ignores extra keys; a missing key causes the match to fail (in a switch) or throws `StateError` (in a declaration).

```dart
var {'name': name, 'age': age} = {'name': 'Lily', 'age': 13};
switch (json) {
  case {'user': var name}: print(name);
}
```

### Record Pattern

Destructures `Record` fields by position or by name. Must match the record’s shape exactly.

```dart
// positional
var (x, y) = (1, 2);
// named
var (myString: s, myNumber: n) = (myString: 'a', myNumber: 1);
```

### Object Pattern

Destructures class instances via getters. The pattern checks the runtime type; then binds the result of calling each getter.

```dart
switch (shape) {
  case Rect(width: var w, height: var h): print('area = ${w * h}');
  case Circle(radius: var r): print('area = ${pi * r * r}');
}
```

Omit the getter name when it matches the variable name: `case Rect(:width, :height)`.

## Logical Operators in Patterns

Combine subpatterns with `||` (logical‑or) and `&&` (logical‑and).

### Logical‑or `||`

Matches if **any** branch matches. Branches are evaluated left‑to‑right; the first match stops evaluation. Useful for sharing a case body.

```dart
switch (color) {
  case Color.red || Color.blue || Color.green: print('primary');
}
```

All branches must bind the **same set of variables** because only one branch executes.

### Logical‑and `&&`

Matches only if **both** subpatterns match. Use to chain relational patterns or combine type and value checks.

```dart
case int value && >= 0 && <= 100: print('0..100');
```

Variables bound in the two subpatterns must not overlap.

### Parentheses

Group subpatterns to control precedence, just like logical expressions.

```dart
// Equivalent: (x || y) && z  vs  x || (y && z)
case (Pattern.a || Pattern.b) && Pattern.c: ...
```

## Relational Patterns and Guard Clauses

**Relational patterns** use `==`, `!=`, `<`, `>`, `<=`, `>=` to compare the matched value against a constant. They match when the operator returns `true`.

```dart
String grade(int score) => switch (score) {
  >= 90 => 'A',
  >= 80 => 'B',
  >= 70 => 'C',
  _ => 'F',
};
```

**Guard clauses** appear after a case pattern with the keyword `when`. The guard is an arbitrary boolean expression that runs **after** the pattern matches. If the guard evaluates to `false`, the switch continues to the next case (it does **not** exit the switch).

```dart
switch (pair) {
  case (int a, int b) when a > b: print('$a > $b');
  case (int a, int b) when a < b: print('$a < $b');
  case (int a, int b): print('equal');
}
```

Use guards for conditions that cannot be expressed purely with patterns (e.g., comparing two extracted values).

## Switch Expressions and Exhaustiveness

**Switch expressions** return a value and must be **exhaustive**: every possible input must match at least one case. Use sealed classes to let the compiler verify exhaustiveness; otherwise add a wildcard `_` as the final case.

```dart
// Exhaustive because Shape is sealed
double area(Shape s) => switch (s) {
  Square(:var length) => length * length,
  Circle(:var radius) => pi * radius * radius,
};
```

**Switch statements** do not enforce exhaustiveness unless the matched value is a sealed class or an enum. Always include a `default` (or `_`) case for non‑exhaustive switches.

Multiple cases can share a body without `||` in statements (by falling through), but `||` is **required** to share a guard.

```dart
switch (shape) {
  case Square(size: var s) || Circle(size: var s) when s > 0:
    print('Non‑empty symmetric shape');
}
```

## Refactoring if-else Chains

Replace traditional `if`‑`else` logic with a single switch for increased readability and safety.

### Task Progress

- [ ] Identify the variable that drives branching.
- [ ] List all distinct shapes or value ranges the variable can take.
- [ ] For each branch, write a pattern that captures the required shape and binds variables.
- [ ] Move complex boolean conditions into `when` guards.
- [ ] Ensure exhaustiveness with a final `_` case or a `default` block.
- [ ] Run the Dart analyzer and verify no non‑exhaustive or dead‑code warnings.
- [ ] Execute tests to confirm identical behavior.

### Example: Before and After

**Original if-else:**

```dart
void describe(dynamic obj) {
  if (obj is int) {
    if (obj > 0) {
      print('positive int');
    } else if (obj < 0) {
      print('negative int');
    } else {
      print('zero');
    }
  } else if (obj is String) {
    if (obj.length >= 5) {
      print('long string');
    } else {
      print('short string');
    }
  } else {
    print('unknown');
  }
}
```

**Refactored with switch pattern matching:**

```dart
void describe(dynamic obj) => switch (obj) {
  int obj when obj > 0 => print('positive int'),
  int obj when obj < 0 => print('negative int'),
  int _ => print('zero'),
  String s when s.length >= 5 => print('long string'),
  String _ => print('short string'),
  _ => print('unknown'),
};
```

## Workflow: Applying Pattern Matching

Use this repeatable process whenever you introduce pattern matching.

### Task Progress Checklist

- [ ] **Analyze** the data structure: Is it a record, list, map, or custom object?
- [ ] **Choose the context**: Declaration, assignment, switch expression/statement, or if‑case.
- [ ] **Pattern design**: Select the right pattern type (constant, variable, list, map, record, object) and nest as needed.
- [ ] **Combine** with `&&`/`||` if multiple checks must occur at the same level.
- [ ] **Add guards** for logic that relies on the bound variables.
- [ ] **Check exhaustiveness**: For switch expressions over non‑sealed types, end with `_ =>`. For statements, add `default:` or confirm all subtype cases are covered.
- [ ] **Run `dart analyze`** to catch pattern errors (type mismatches, missing exhaustiveness).
- [ ] **Write unit tests** that exercise every case, including defaults.
- [ ] **Review output**: Are variables bound with the correct types and values?
- [ ] **Iterate**: Fix issues, re‑analyze, re‑run tests until passing.

**Conditional guidance:**

- **Creating NEW code:** Start with a switch expression. Write the happy‑path patterns first, then fill in edge cases and the `_` fallback.
- **Editing EXISTING code:** Identify old `if`‑`is` chains and convert branch by branch. Keep the old code commented until the new switch passes the same tests.

**Feedback loop:** Write pattern code → `dart analyze` → fix errors → run tests → review coverage → repeat.

## Examples

### Destructuring Multiple Returns

```dart
(String, int) userInfo(Map json) => (json['name'], json['age']);

// One‑line destructure
var (name, age) = userInfo({'name': 'Ada', 'age': 25});
print('$name, $age');
```

### Validating Incoming JSON

```dart
final json = {'user': ['Alice', 30]};
if (json case {'user': [String name, int age]}) {
  print('Valid user: $name, $age');
}
```

### Algebraic Data Type (Sealed Class + Switch)

```dart
sealed class Result {}
class Data extends Result {
  final String value;
  Data(this.value);
}
class Error extends Result {
  final Object exception;
  Error(this.exception);
}

String handle(Result r) => switch (r) {
  Data(value: var v) => 'Success: $v',
  Error(exception: var e) => 'Error: $e',
};
```

### Relational Patterns with Guard

```dart
String describeAge(int age) => switch (age) {
  < 0 => 'invalid',
  >= 0 && <= 12 => 'child',
  >= 13 && <= 19 => 'teen',
  >= 20 => 'adult',
};
```

### Logical‑or with Multiple Cases

```dart
switch (day) {
  case DateTime.monday || DateTime.tuesday || DateTime.wednesday:
    print('early week');
  case DateTime.thursday || DateTime.friday:
    print('late week');
  case DateTime.saturday || DateTime.sunday:
    print('weekend');
}
```
