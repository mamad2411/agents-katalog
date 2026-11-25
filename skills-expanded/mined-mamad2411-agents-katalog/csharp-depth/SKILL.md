---
name: csharp-depth
description: "Deep C# expertise from C# in Depth"
---

# Skeet: C# Mastery

Jon Skeet's core belief: **Understand the language deeply, then let that understanding guide simple code.** The goal isn't to use every feature—it's to know which feature fits each situation.

## The Foundational Principle

> "The more you understand about how C# works, the simpler your code can be."

Deep knowledge enables simplicity. You don't need clever tricks when you understand the fundamentals.

---

## Core Principles

### 1. Understand Value vs Reference Semantics

The most fundamental distinction in C#. Get this wrong, and everything else breaks.

**Value types (structs):**
- Copied on assignment
- Stored on stack (usually)
- No null by default (before nullable value types)

**Reference types (classes):**
- Reference copied, object shared
- Stored on heap
- Can be null

```csharp
// Value type: independent copies
int a = 5;
int b = a;
b = 10;
Console.WriteLine(a); // Still 5

// Reference type: shared object
var list1 = new List<int> { 1, 2, 3 };
var list2 = list1;
list2.Add(4);
Console.WriteLine(list1.Count); // 4 - same list!
```

**Struct guidelines:**
- Keep small (< 16 bytes)
- Make immutable
- Don't inherit (can't anyway)
- Use for naturally value-like concepts (Point, DateTime, Guid)

### 2. Nullable Reference Types Are Essential

Enable nullable reference types. They catch null bugs at compile time.

```csharp
#nullable enable

// Compiler tracks nullability
string name = "Alice";      // Non-null, guaranteed
string? nickname = null;    // Nullable, explicit

void Greet(string name)     // Caller must provide non-null
{
    Console.WriteLine(name.Length); // Safe - can't be null
}

void GreetOptional(string? name)
{
    // Must check before use
    if (name is not null)
    {
        Console.WriteLine(name.Length);
    }
}
```

**Nullable patterns:**
```csharp
// Null-coalescing
string display = nickname ?? "No nickname";

// Null-coalescing assignment
nickname ??= "Default";

// Null-conditional
int? length = nickname?.Length;

// Null-forgiving (when you know better than compiler)
string definitelyNotNull = GetValueThatMightBeNull()!;
// Use sparingly - you're telling compiler to trust you
```

### 3. Pattern Matching Is Your Friend

Modern C# pattern matching replaces verbose type checks and casts.

**Not this:**
```csharp
if (obj is string)
{
    string s = (string)obj;
    Console.WriteLine(s.Length);
}
```

**This:**
```csharp
if (obj is string s)
{
    Console.WriteLine(s.Length);
}
```

**Switch expressions (C# 8+):**
```csharp
string GetDescription(Shape shape) => shape switch
{
    Circle { Radius: 0 } => "Point",
    Circle { Radius: var r } => $"Circle with radius {r}",
    Rectangle { Width: var w, Height: var h } when w == h => $"Square {w}x{w}",
    Rectangle { Width: var w, Height: var h } => $"Rectangle {w}x{h}",
    _ => "Unknown shape"
};
```

**Property patterns:**
```csharp
// Nested property matching
if (person is { Address: { City: "London" } })
{
    // Person lives in London
}

// C# 10+ simplified
if (person is { Address.City: "London" })
{
    // Same thing, cleaner
}
```

### 4. Records for Data

Records are the right choice for immutable data types.

```csharp
// Immutable by default, value equality, with-expressions, deconstruction
public record Person(string Name, int Age);

var alice = new Person("Alice", 30);
var older = alice with { Age = 31 };  // Creates new instance

// Value equality
var alice2 = new Person("Alice", 30);
Console.WriteLine(alice == alice2);  // True

// Deconstruction
var (name, age) = alice;
```

**Record structs (C# 10+):**
```csharp
// Value type record - best of both worlds
public readonly record struct Point(double X, double Y);
```

**When to use records vs classes:**
- Record: Data transfer, immutable state, value equality needed
- Class: Identity matters, mutable state, complex behavior

### 5. Generics: Understand Variance

Covariance and contravariance are confusing until they click.

**Covariance (out):** Can use more derived type
```csharp
// IEnumerable<out T> is covariant
IEnumerable<Animal> animals = new List<Dog>(); // OK - Dog is Animal

// Works because you only GET values out
foreach (Animal animal in animals) { }
```

**Contravariance (in):** Can use less derived type
```csharp
// Action<in T> is contravariant
Action<Dog> dogAction = (Animal a) => Console.WriteLine(a.Name);

// Works because you only PUT values in
dogAction(new Dog());
```

**Memory aid:**
- `out` = output = covariant = can substitute derived
- `in` = input = contravariant = can substitute base

### 6. LINQ: Deferred vs Immediate Execution

Understanding when LINQ executes is critical.

**Deferred execution (most LINQ):**
```csharp
var query = numbers.Where(n => n > 5);  // Nothing happens yet
// The filter runs when you iterate:
foreach (var n in query) { }  // NOW it executes
```

**Immediate execution:**
```csharp
var list = numbers.Where(n => n > 5).ToList();   // Executes now
var count = numbers.Count(n => n > 5);           // Executes now
var first = numbers.First(n => n > 5);           // Executes now
```

**The multiple enumeration trap:**
```csharp
// BAD: Enumerates twice (or worse, source changed between)
IEnumerable<int> filtered = GetNumbers().Where(n => n > 5);
Console.WriteLine(filtered.Count());  // Enumerates
Console.WriteLine(filtered.Sum());    // Enumerates again

// GOOD: Materialize once
var filtered = GetNumbers().Where(n => n > 5).ToList();
Console.WriteLine(filtered.Count);    // No enumeration
Console.WriteLine(filtered.Sum());    // No enumeration
```

### 7. Collection Expressions (C# 12)

Modern syntax for creating collections.

```csharp
// Old way
int[] numbers = new int[] { 1, 2, 3 };
List<int> list = new List<int> { 1, 2, 3 };

// New way
int[] numbers = [1, 2, 3];
List<int> list = [1, 2, 3];

// Spread operator
int[] combined = [..first, ..second, 99];

// Works with any collection type
ImmutableArray<int> immutable = [1, 2, 3];
Span<int> span = [1, 2, 3];
```

---

## Common Pitfalls

### Closure Capture

```csharp
// WRONG: All lambdas capture the same variable
var actions = new List<Action>();
for (int i = 0; i < 5; i++)
{
    actions.Add(() => Console.WriteLine(i));
}
// All print 5!

// RIGHT: Capture loop variable by value
for (int i = 0; i < 5; i++)
{
    int captured = i;
    actions.Add(() => Console.WriteLine(captured));
}
// Prints 0, 1, 2, 3, 4

// Note: foreach fixed this in C# 5
foreach (var item in items)
{
    actions.Add(() => Console.WriteLine(item)); // Works correctly
}
```

### Struct Mutation

```csharp
// DANGEROUS: Mutable struct
public struct MutablePoint
{
    public int X;
    public int Y;
    public void Move(int dx, int dy) { X += dx; Y += dy; }
}

var point = new MutablePoint { X = 1, Y = 2 };
// This works as expected
point.Move(1, 1);

// But this doesn't!
var points = new List<MutablePoint> { point };
points[0].Move(1, 1);  // Compiles but modifies a COPY
// points[0] unchanged!

// SAFE: Immutable struct
public readonly struct Point
{
    public int X { get; init; }
    public int Y { get; init; }
    public Point Move(int dx, int dy) => new(X + dx, Y + dy);
}
```

### Boxing Overhead

```csharp
// BOXING: Value type → object allocation
int x = 42;
object boxed = x;  // Allocates on heap

// Avoid in hot paths:
// BAD
void Log(object value) => Console.WriteLine(value);
Log(42);  // Boxing!

// GOOD
void Log<T>(T value) => Console.WriteLine(value);
Log(42);  // No boxing
```

---

## The Skeet Test

Before committing C# code, ask:

1. **Value or reference?** Is the semantics correct for the type?
2. **Nullability clear?** Are nullable types marked `?`, non-nullable guaranteed?
3. **Pattern matching used?** Could if-else chains be switch expressions?
4. **LINQ materialized?** Are queries enumerated multiple times?
5. **Closures safe?** Are loop variables captured correctly?
6. **Structs immutable?** Are any mutable structs causing issues?

---

## When to Apply

| Scenario | Apply Skeet |
|----------|-------------|
| Language edge cases, "why does this work?" | Yes |
| Generics, variance, type inference | Yes |
| LINQ behavior and optimization | Yes |
| Nullable reference types | Yes |
| Async/await behavior | Partially - see async |
| Performance optimization | Partially - see performance-specific resources |

---

## Source Material

- "C# in Depth" (4th Edition, Manning, 2019)
- Stack Overflow contributions (top reputation, all time)
- NodaTime library (designed by Skeet)
- Blog posts and conference talks

---

*"The more you understand about how C# works, the simpler your code can be."* — Jon Skeet
