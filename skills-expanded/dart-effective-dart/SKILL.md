---
name: dart-effective-dart
description: 遵循 Effective Dart 最佳实践（代码风格、文档、用法、API 设计），编写一致、可维护、高效的 Dart 代码。
metadata:
  model: deepseek-v4-pro
  last_modified: 2026-05-10T08:27:48.392637Z
---
# Writing Effective Dart Code

## Contents

- [Style](#style-guidelines): naming, ordering, formatting
- [Documentation](#documentation-guidelines): doc comments structure and wording
- [Usage](#usage-guidelines): leveraging language features correctly
- [Design](#design-guidelines): API architecture and type safety
- [Workflow](#workflow-applying-effective-dart-to-your-code): step-by-step application with feedback loop
- [Examples](#examples-violation-vs-compliant-code): violation vs. compliant code

---

## Style Guidelines

### Naming

- Use `UpperCamelCase` for types (classes, enums, typedefs), extensions, and type parameters.  
  `class SliderMenu {}`, `typedef Predicate<T> = bool Function(T);`
- Use `lowercase_with_underscores` for packages, directories, source files, and import prefixes.  
  `my_package/lib/file_system.dart`, `import 'dart:math' as math;`
- Use `lowerCamelCase` for variables, methods, parameters, and constants (including enum values).  
  `var itemCount = 3;`, `const defaultTimeout = 1000;`
- Capitalize acronyms/abbreviations longer than two letters as regular words: `Http`, `Uri`.  
  Two‑letter acronyms keep their English capitalization: `IO`, `UI`. When they start a `lowerCamelCase` identifier, make them all lowercase: `var httpConnection = ...;`.  
- Don’t use a leading underscore for non‑private identifiers.  
- Don’t use Hungarian notation or prefix letters.  
- Don’t explicitly name libraries (legacy `library my_library;` is discouraged).  
- Prefer wildcard `_` for unused callback parameters (Dart ≥3.7).

### Ordering

- Place `dart:` imports first, then `package:` imports, then relative imports.  
- Put `export` directives in a separate section after all imports.  
- Sort each section alphabetically.

### Formatting

- Run `dart format` on every file before committing.  
- Keep lines to 80 characters or fewer; break long expressions manually if needed.  
- Always use curly braces for flow control structures (one‑line `if` without `else` is the only exception).

---

## Documentation Guidelines

- Use `///` (C# style) for documentation comments, **not** `/** */`.
- Write doc comments for all public APIs. Consider library‑level doc comments and private member documentation.
- Start every doc comment with a single‑sentence summary, separated from the rest by a blank line.  
- **For side‑effect‑centric functions/methods**: begin with a third‑person verb.  
  `/// Deletes the file at [path] from the file system.`
- **For non‑boolean properties/variables**: use a noun phrase.  
  `/// The number of checked buttons on the page.`
- **For boolean properties/variables**: start with *“Whether”* followed by a noun or gerund phrase.  
  `/// Whether the modal is currently displayed to the user.`
- **For methods that return a value** (conceptually like a property): use a noun phrase or non‑imperative verb phrase.  
  `/// The [index]th element of this iterable.`
- **For library/class comments**: start with a noun phrase describing the instance or entity.  
- Don’t document both getter and setter; document the property once on the getter.  
- Include inline code samples using fenced code blocks with ` ```dart `.
- Use square brackets `[identifier]` to link to in‑scope identifiers (classes, methods, fields).  
- Explain parameters, return values, and exceptions in prose, not with formal `@param` tags. Put doc comments before metadata annotations.
- Prefer brevity; avoid abbreviations unless they are obvious; use *“this”* instead of *“the”* to refer to the instance.

---

## Usage Guidelines

### Null safety

- Don’t explicitly initialize variables to `null`.  
- Don’t use explicit default `null` for optional parameters.  
- Don’t write `if (bool == true)`; use `if (bool)`. For nullable booleans, use `if (nullableBool ?? false)` or `if (b != null && b)`.  
- Avoid `late` variables if you need to check initialization; use a nullable field and test `null` instead.  
- Use type promotion or null‑check patterns to safely unwrap nullable types. Prefer private `final` fields for promotion.

### Strings

- Concatenate adjacent string literals without `+`.  
- Prefer interpolation: `'Hello, $name!'` over `'Hello, ' + name + '!'`.  
- Omit curly braces in interpolation when the expression is a simple identifier.

### Collections

- Use collection literals (`<int>[]`, `{}`, `{}`) instead of constructors like `List()`, `Map()`.  
- Use `.isEmpty` / `.isNotEmpty` instead of `.length == 0`.  
- Avoid `Iterable.forEach()` with a function literal; use a `for`‑in loop unless the function already exists (e.g., `forEach(print)`).  
- Use `toList()` to copy an iterable; reserve `List.from()` for changing the element type.  
- Use `whereType<T>()` to filter by type; avoid `where((e) => e is T).cast<T>()`.  
- Avoid `cast()`; prefer creating a properly typed collection, casting elements on access, or using `List<T>.from()`.

### Functions

- Bind a name with a function declaration (`void localFunc() { ... }`) instead of assigning a lambda to a variable.  
- Use tear‑offs instead of wrapping a method in an unnecessary lambda:  
  `charCodes.forEach(print);` not `(code) { print(code); }`.

### Variables

- Choose a consistent rule for `var` vs `final` on local variables and stick to it throughout the project.  
- Prefer computing values on demand (via getters) instead of caching them in extra fields, unless profiling proves a performance problem.

### Members

- Don’t wrap a public field in a trivial getter/setter; expose the field directly.  
- Use `final` fields to make read‑only properties.  
- Use `=>` for single‑expression members; avoid deep nesting.  
- Don’t write `this.` except to avoid shadowing (parameter and field have the same name) or to redirect a named constructor.  
- Initialize fields at their declaration whenever the value does not depend on constructor arguments.

### Constructors

- Use initializing formals (`Point(this.x, this.y);`).  
- Prefer constructor initializer lists over `late` fields.  
- Use `;` instead of `{}` for empty constructor bodies.  
- Don’t use `new` (it’s optional and unnecessary).  
- Don’t redundantly add `const` in a constant context (collection literal, const constructor call, switch case expression, etc.).

### Error handling

- Catch errors only with `on` clauses that specify the expected type.  
- Never silently swallow exceptions; always log, handle, or rethrow.  
- Throw objects that implement `Error` only for programmatic bugs; throw `Exception` for runtime failures.  
- Don’t explicitly catch `Error`; let them propagate.  
- Use `rethrow` to preserve the original stack trace.

### Asynchrony

- Prefer `async`/`await` over raw `Future.then()` chains.  
- Don’t add `async` when the function body just returns a future and never uses `await`.  
- Use higher‑order methods on streams (`map`, `where`, etc.) instead of manual listeners.  
- Avoid `Completer`; use `async`/`await` or `Future.then()` instead.  
- When testing a `FutureOr<T>` where `T` could be `Object`, test for `Future<T>` to disambiguate.

---

## Design Guidelines

### Names

- Use terms consistently across the API.  
- Place the most descriptive noun last (`pageCount`, `ConversionSink`).  
- Name non‑boolean properties/variables with noun phrases (`list.length`).  
- Name boolean properties/variables with non‑imperative verb phrases (`isEmpty`, `hasElements`).  
- For named boolean *parameters*, consider omitting the verb (`paused: false`).  
- Prefer the positive form for booleans (`isConnected` over `isDisconnected`).  
- Name side‑effecting methods with imperative verb phrases (`list.add()`, `window.refresh()`).  
- Avoid starting a method name with `get`; use getters or choose a more descriptive verb.  
- Name conversion methods `to___()` (creates a new object) or `as___()` (different representation backed by original).  
- Follow mnemonic conventions for type parameters: `E` for element, `K`/`V` for key/value, `T`/`S`/`U` otherwise.  
- Don’t embed parameter descriptions in method names.

### Libraries

- Make declarations private (prepend `_`) unless they are intended as public API.  
- It’s fine to define multiple related classes in the same library (class‑level privacy is library‑scoped).

### Classes and mixins

- Don’t define a single‑member abstract class when a plain function (`typedef`) suffices.  
- Don’t define a class that contains *only* static members; use top‑level functions/variables instead.  
- Don’t extend or implement a class that isn’t explicitly designed for it; respect `final`, `base`, `interface`, `sealed` modifiers.  
- Use class modifiers to communicate intent (e.g., `final class`, `base class`).  
- Prefer pure `mixin` or pure `class` over `mixin class` in new code.

### Constructors

- Make the constructor `const` if all fields are `final` and the constructor does no work beyond initialization.

### Members

- Prefer `final` for fields and top‑level variables unless the value must change.  
- Use getters for operations that conceptually access a property (no arguments, no visible side effects, consistent result).  
- Use setters for operations that conceptually change a property (one argument, idempotent).  
- Don’t define a setter without a corresponding getter.  
- Avoid faking overloading with runtime type tests; define separate methods for different types if callers usually know which operation they want.  
- Avoid public `late final` fields without initializers; they unintentionally expose a setter.  
- Never return a nullable `Future`, `Stream`, or collection type. Return an empty container or a future of a nullable type.  
- Don’t return `this` from methods just to enable a fluent interface; use cascades (`..`).

### Types

- Type annotate variables without initializers.  
- Annotate fields and top‑level variables if the type isn’t obvious from the initializer.  
- Don’t redundantly annotate initialized local variables; let inference work.  
- Annotate return types and parameter types on function declarations.  
- Don’t annotate function expression parameters when they are inferred.  
- Don’t type annotate initializing formals (`this.x`).  
- Write type arguments on generic invocations only when not inferred from context.  
- Avoid incomplete generic types (`List` without `<>`); write the full type `List<num>`.  
- Use `dynamic` explicitly when inference would fail and you actually want `dynamic`.  
- In function type annotations, prefer full signatures: `bool Function(String)` over just `Function`.  
- Don’t specify a return type for a setter.  
- Use the modern `typedef` syntax (`typedef Comparison<T> = int Function(T, T);`).  
- Prefer inline function types over a `typedef` unless the type is lengthy or reused often.  
- Use `Future<void>` for async methods that return no value.  
- Avoid `FutureOr<T>` as a return type; use `Future<T>` and keep the function consistently async. (In contravariant positions, like a callback parameter, it is acceptable.)

### Parameters

- Avoid positional boolean parameters; use named parameters or named constructors.  
- Avoid optional positional parameters when callers may want to skip earlier ones; use named parameters instead.  
- Don’t force callers to pass a special “no value” like `null`; make the parameter optional.  
- Use inclusive‑start, exclusive‑end parameters for ranges (consistent with `substring`, `sublist`).

### Equality

- Override `hashCode` whenever you override `==`.  
- Ensure `==` is reflexive, symmetric, and transitive.  
- Avoid custom equality for mutable classes.  
- The parameter of `==` must be non‑nullable (`Object`), not `Object?`.

---

## Workflow: Applying Effective Dart to Your Code

### Task Progress

- [ ] 1. Format codebase
- [ ] 2. Audit naming conventions
- [ ] 3. Add/improve documentation
- [ ] 4. Refactor usage patterns
- [ ] 5. Review API design
- [ ] 6. Run static analysis and tests
- [ ] 7. Final review and merge

### Step 1: Format the codebase

Run `dart format lib/ test/` on the project directory.  
**If** the output shows changes, **then** review them to ensure logic is unaffected.

### Step 2: Audit naming conventions

Check each identifier:

- **If** a type/extension/typedef name is not `UpperCamelCase`, **then** rename it.
- **If** a file/directory/package/import prefix uses underscores incorrectly, **then** rename to `lowercase_with_underscores`.
- **If** a variable, method, or constant uses `SCREAMING_CAPS` in new code, **then** convert to `lowerCamelCase`.
- **If** an acronym longer than two letters is all‑caps, **then** follow the capitalization rule.
- **If** there are unused callback parameters named anything other than `_` (in local anonymous functions), **then** replace with `_`.

### Step 3: Add/improve documentation

For every public declaration (class, mixin, extension, top‑level function/variable, enum, method, getter, setter):

- **If** no doc comment exists, **then** add `///` with a one‑sentence summary.
- **If** the member is a side‑effecting function, **then** start with a third‑person verb (`/// Deletes ...`).
- **If** the member is a non‑boolean property/getter, **then** start with a noun phrase.
- **If** the member is boolean, **then** start with “Whether”.
- **If** the documentation is redundant with the name or repeats obvious context, **then** remove or rewrite to explain *what* the reader doesn’t know.
- **If** a code example would clarify usage, **then** include a fenced ````dart` block.
- **If** any referenced identifier exists in scope, **then** surround it with `[ ]` brackets.
- **If** there are `@param` or `@returns` tags, **then** rewrite them as prose.

### Step 4: Refactor usage patterns

Search the codebase for anti‑patterns and replace:

- `new Type()` → `Type()` (remove `new`)
- `const const ...` → single `const` or remove entirely where context is constant.
- `if (b == true)` → `if (b)`; `if (b == false)` → `if (!b)`.
- `var list = List.empty()` → `var list = <Type>[]`.
- `collection.length == 0` → `collection.isEmpty`.
- `collection.where((e) => e is T).cast<T>()` → `collection.whereType<T>()`.
- `var foo = () { ... };` → `void foo() { ... }` for named local functions.
- `predicate.forEach((e) => f(e))` → `predicate.forEach(f)` (tear‑off).
- `list = list.cast<int>()` → `List<int>.from(list)` if the whole list is needed.
- Unnecessary `this.` (except for shadowing and constructor redirection) → remove it.
- `StringBuffer(); buffer.write(...)` with cascade → `StringBuffer()..write(...)`.
- `return Future.value(...)` in an `async` function that does nothing else → remove `async` and return the future directly, or keep `async` only if necessary.
- Direct `Completer` usage → rewrite with `async`/`await`.

### Step 5: Review API design

Examine class and function signatures:

- **If** a class has only static members, **then** convert to top‑level functions/variables (unless grouping constants like `Color`).
- **If** an abstract class has a single abstract method, **then** replace it with a `typedef`.
- **If** a public field is mutable but should logically be read‑only, **then** make it `final`.
- **If** a getter does work that is heavy or has side effects, **then** consider converting to a method with a verb name.
- **If** a method returns `null` for a collection/future/stream, **then** change to return an empty collection or a future of a nullable value; document accordingly.
- **If** boolean parameters are positional, **then** convert to named parameters.
- **If** optional positional parameters force callers to pass a placeholder to reach a later argument, **then** switch to named optional parameters.
- **If** `==` is overridden without `hashCode`, **then** add a `hashCode` override that obeys the contract.

### Step 6: Run static analysis and tests

Execute `dart analyze` and `dart test`.  
**If** the analyzer reports warnings/errors, **then** fix them, focusing first on potential violations of the rules above.  
**If** tests fail after refactoring, **then** revert the smallest possible change and re‑evaluate.

### Step 7: Final review and merge

Check the diff for any remaining inconsistencies. Run `dart format` one last time.  
**If** all steps are green, **then** the code follows Effective Dart.

---

## Examples: Violation vs. Compliant Code

### Style

```dart
// ❌ Violation
class myClass {
  final String Title;
  int page_count;
}

// ✅ Compliant
class MyClass {
  final String title;
  int pageCount;
}
```

### Documentation

```dart
// ❌ Violation
// Returns the count of items.
int count() { ... }

// ✅ Compliant
/// The number of items currently stored.
int get count => _items.length;
```

```dart
// ❌ Violation
/// @param name The user's name.
/// @returns The greeting.
String greet(String name) => 'Hello, $name!';

// ✅ Compliant
/// Returns a greeting for the given [name].
String greet(String name) => 'Hello, $name!';
```

### Usage

```dart
// ❌ Violation
var list = new List<dynamic>();
list.add(1);
if (list.length == 0) return null;

// ✅ Compliant
var list = <int>[];
list.add(1);
if (list.isEmpty) return null;
```

```dart
// ❌ Violation
people.forEach((person) {
  print(person.name);
});

// ✅ Compliant
for (final person in people) {
  print(person.name);
}
```

### Design

```dart
// ❌ Violation
class MathUtils {
  static int max(int a, int b) => a > b ? a : b;
}

// ✅ Compliant
int max(int a, int b) => a > b ? a : b; // top-level function
```

```dart
// ❌ Violation
class Circle {
  double radius;
  double get area => computeArea();
}

// ✅ Compliant
class Circle {
  final double radius;
  double get area => pi * radius * radius; // no caching, always correct
}
```

```dart
// ❌ Violation
Future<List<String>?> fetchNames() async {
  if (noData) return null;
  return ['Alice', 'Bob'];
}

// ✅ Compliant
Future<List<String>> fetchNames() async {
  if (noData) return <String>[];
  return ['Alice', 'Bob'];
}
```

These rules and examples constitute a minimal, enforceable subset of Effective Dart. For a comprehensive list, refer to the official Effective Dart guides, but apply these principles as the baseline for all Dart code.
