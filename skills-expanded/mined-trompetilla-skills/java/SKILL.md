---
name: Java
description: Write robust Java avoiding null traps, equality bugs, and concurrency pitfalls.
metadata: {"clawdbot":{"emoji":"☕","requires":{"bins":["java","javac"]},"os":["linux","darwin","win32"]}}
---

## String Gotchas
- `==` compares references, not content — always use `.equals()` for strings
- String pool: literals interned, `new String()` not — `"a" == "a"` true, `new String("a") == "a"` false
- Strings are immutable — concatenation in loop creates garbage, use `StringBuilder`
- `null.equals(x)` throws NPE — use `"literal".equals(variable)` or `Objects.equals()`

## Null Handling
- NPE is most common exception — check nulls or use `Optional<T>`
- `Optional.get()` throws if empty — use `orElse()`, `orElseGet()`, or `ifPresent()`
- Don't use Optional for fields or parameters — intended for return types
- `@Nullable` and `@NonNull` annotations help static analysis — not enforced at runtime
- Primitive types can't be null — but wrappers (`Integer`) can, autoboxing hides this

## Equality Contract
- Override `equals()` must also override `hashCode()` — HashMap/HashSet break otherwise
- `equals()` must be symmetric, transitive, consistent — `a.equals(b)` implies `b.equals(a)`
- Use `getClass()` check, not `instanceof` — unless explicitly designed for inheritance
- `hashCode()` must return same value for equal objects — unequal objects can share hash
- Arrays: `Arrays.equals()` for content — `array.equals(other)` uses reference comparison

## Generics Traps
- Type erasure: generic type info gone at runtime — can't do `new T()` or `instanceof List<String>`
- Raw types bypass safety — `List list` allows any type, loses compile-time checks
- `List<Dog>` is not subtype of `List<Animal>` — use wildcards: `List<? extends Animal>`
- `<?>` is not same as `<Object>` — wildcard allows any type, Object only allows Object
- Generic arrays forbidden — `new T[10]` fails, use `ArrayList<T>` instead

## Collections Pitfalls
- Modifying while iterating throws `ConcurrentModificationException` — use Iterator.remove() or copy
- `Arrays.asList()` returns fixed-size list — can't add/remove, backed by array
- `List.of()`, `Set.of()` return immutable — throw on modification attempts
- `HashMap` allows null key and values — `Hashtable` and `ConcurrentHashMap` don't
- Sort requires `Comparable` or `Comparator` — ClassCastException if missing

## Autoboxing Dangers
- `Integer == Integer` uses reference for values outside -128 to 127 — use `.equals()`
- Unboxing null throws NPE — `Integer i = null; int x = i;` crashes
- Performance: boxing in tight loops creates garbage — use primitives
- `Integer.valueOf()` caches small values — `new Integer()` never caches (deprecated)

## Concurrency
- `volatile` ensures visibility, not atomicity — `count++` still needs synchronization
- `synchronized` on method locks `this` — static synchronized locks class object
- Double-checked locking broken without volatile — use holder pattern or enum for singletons
- `ConcurrentHashMap` safe but not atomic for compound ops — use `computeIfAbsent()`
- Thread pool: don't create threads manually — use `ExecutorService`

## Exception Handling
- Checked exceptions must be caught or declared — unchecked (RuntimeException) don't
- Try-with-resources auto-closes — implement `AutoCloseable`, Java 7+
- Catch specific exceptions first — more general catch later or unreachable code error
- Don't catch `Throwable` — includes `Error` which shouldn't be caught
- `finally` always runs — even on return, but return in finally overrides try's return

## Inheritance Quirks
- `private` methods not overridden — new method with same name in child
- `static` methods hide, don't override — called based on reference type, not object
- `super()` must be first statement in constructor — no logic before
- `final` methods can't be overridden — `final` class can't be extended
- Fields don't participate in polymorphism — accessed by reference type

## Memory Management
- Leaked listeners/callbacks prevent GC — remove references when done
- `WeakReference` for caches — allows GC when memory needed
- `static` collections grow forever — clear or use weak/soft references
- Inner classes hold reference to outer — use static nested class if not needed
- `finalize()` deprecated — use Cleaner or try-with-resources

## Modern Java
- Records (16+): immutable data carriers — auto-generates equals, hashCode, toString
- Sealed classes (17+): restrict inheritance — `permits` clause lists allowed subclasses
- Pattern matching in switch (21+): type patterns and guards — cleaner than instanceof chains
- Virtual threads (21+): lightweight concurrency — don't pool, create freely
- `var` for local variables (10+) — inferred type, still strongly typed
