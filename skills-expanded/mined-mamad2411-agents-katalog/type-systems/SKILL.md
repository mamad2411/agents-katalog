---
name: type-systems
description: "Language design philosophy"
---

# Hejlsberg: Language Design Wisdom

Anders Hejlsberg's core belief: **Languages should be powerful yet approachable.** Complexity should be opt-in. The simple case should be simple; advanced features available when needed.

## The Foundational Principle

> "Make the easy things easy, and the hard things possible."

Every language feature should earn its place. If it makes common tasks harder or confuses developers, it shouldn't exist.

---

## Design Philosophy

### 1. Type Systems Should Help, Not Hinder

Types exist to catch errors and enable tooling—not to satisfy the compiler.

**Progressive disclosure of complexity:**
```csharp
// Simple case: inference handles it
var name = "Alice";
var numbers = new[] { 1, 2, 3 };

// More control when needed
List<string> names = new();

// Full generic power when required
Dictionary<string, Func<Task<IEnumerable<int>>>> lookup = new();
```

**The evolution:**
- C# 1.0: Explicit types everywhere
- C# 3.0: var for local inference
- C# 9.0: Target-typed new
- C# 12.0: Collection expressions

Each step made the common case simpler while keeping full power available.

### 2. Null Safety Through Evolution

Hejlsberg admits null was a billion-dollar mistake—but fixing it in an existing language requires care.

**The retrofit approach:**
```csharp
// Opt-in at project or file level
#nullable enable

// Existing code still works
string oldCode = null;  // Warning, not error

// New code is safe
string newCode = "safe";
string? nullable = null;

// Gradual migration possible
```

**Why not breaking change:**
- Millions of lines of existing code
- Pragmatism over purity
- Warnings first, then errors

### 3. Composition Over Magic

Prefer explicit, composable features over hidden behavior.

**LINQ: Composition done right**
```csharp
// Each method is independent, composable
var result = items
    .Where(x => x.IsActive)
    .OrderBy(x => x.Name)
    .Select(x => x.Id)
    .Take(10);

// You understand each step
// You can rearrange, remove, add
// No hidden coupling
```

**Compare to "magic" ORMs:**
```csharp
// Hidden behavior, hard to understand
var items = context.Items
    .Include(x => x.Related)   // What SQL does this generate?
    .ThenInclude(x => x.Other) // N+1 query issue hidden?
    .ToList();                 // When does query execute?
```

### 4. Immutability as Default Path

Modern C# increasingly favors immutability.

**Records (C# 9):**
```csharp
// Immutable by default
public record Person(string Name, int Age);

// Mutation through copying
var older = person with { Age = person.Age + 1 };
```

**Init-only properties (C# 9):**
```csharp
public class Config
{
    public string Endpoint { get; init; }  // Set once, then readonly
    public int Timeout { get; init; }
}
```

**Required members (C# 11):**
```csharp
public class Order
{
    public required string CustomerId { get; init; }
    public required decimal Total { get; init; }
}
// Compiler enforces all required members are set
```

### 5. Pattern Matching: Declarative over Imperative

Express what you want, not how to get it.

**Evolution:**
```csharp
// C# 1: Imperative, error-prone
if (obj is string)
{
    string s = (string)obj;
    if (s.Length > 0) { ... }
}

// C# 7: Basic patterns
if (obj is string s && s.Length > 0) { ... }

// C# 8: Switch expressions
var description = obj switch
{
    string s when s.Length == 0 => "empty string",
    string s => $"string: {s}",
    int n when n < 0 => "negative",
    int n => $"number: {n}",
    null => "null",
    _ => "unknown"
};

// C# 11: List patterns
var result = list switch
{
    [] => "empty",
    [var single] => $"one: {single}",
    [var first, .., var last] => $"first: {first}, last: {last}"
};
```

### 6. Async as First-Class Citizen

Async/await transformed how we write concurrent code.

**Before (callback hell):**
```csharp
client.GetAsync(url, response =>
{
    response.ReadAsync(data =>
    {
        Process(data, result =>
        {
            callback(result);
        });
    });
});
```

**After (async/await):**
```csharp
var response = await client.GetAsync(url);
var data = await response.ReadAsync();
var result = await Process(data);
return result;
```

**Design principle:** Async code should read like sync code. The complexity of continuations is handled by the compiler.

### 7. Expression-Bodied Members

When a method is just a return, show it.

**Evolution:**
```csharp
// C# 1: Verbose
public int Double(int x)
{
    return x * 2;
}

// C# 6: Expression-bodied methods
public int Double(int x) => x * 2;

// Extended to properties, constructors, etc.
public string Name { get; }
public Person(string name) => Name = name;
public override string ToString() => $"Person: {Name}";
```

---

## Language Evolution Principles

### Backward Compatibility

Every new C# version can compile old code. Breaking changes are extremely rare.

**Why this matters:**
- Enterprises can upgrade gradually
- Libraries don't force version churn
- Investment in code is preserved

### Opt-In Complexity

Advanced features don't complicate simple code.

```csharp
// You can write C# ignoring:
// - Spans and Memory<T>
// - ref structs
// - Unsafe code
// - Source generators
// - Advanced generic constraints

// Until you need them
```

### Compiler as Partner

The compiler should help you write correct code.

```csharp
// Definite assignment analysis
int x;
if (condition)
    x = 1;
Console.WriteLine(x);  // Error: x might not be assigned

// Exhaustiveness checking
int result = shape switch
{
    Circle c => c.Area,
    Rectangle r => r.Area,
    // Warning: pattern not exhaustive
};

// Nullability analysis
string? name = GetName();
Console.WriteLine(name.Length);  // Warning: possible null
```

---

## The Hejlsberg Test

When designing APIs or writing code, ask:

1. **Is the simple case simple?** Can a beginner understand the basic usage?
2. **Is complexity opt-in?** Do advanced features hide until needed?
3. **Is it composable?** Can features be combined predictably?
4. **Is it explicit?** Can you understand what code does without hidden magic?
5. **Is it safe by default?** Does the compiler catch common mistakes?
6. **Will it age well?** Can this code migrate to future C# versions?

---

## Design Decisions to Learn From

### Why Properties, Not Public Fields

```csharp
// Fields can't evolve
public string Name;  // Can't add validation later without breaking

// Properties can
public string Name { get; set; }  // Add logic later, no break
public string Name
{
    get => _name;
    set => _name = value ?? throw new ArgumentNullException();
}
```

### Why Extension Methods

```csharp
// Can't modify string class
// But can extend it
public static class StringExtensions
{
    public static bool IsNullOrEmpty(this string? s) => string.IsNullOrEmpty(s);
}

// Enables LINQ without modifying IEnumerable
// Enables method syntax on any type
```

### Why Anonymous Types with Limited Scope

```csharp
var point = new { X = 1, Y = 2 };  // Anonymous type

// Can't be returned from methods
// Can't be passed as parameters (without generics)
// WHY: Forces named types for public contracts
```

---

## When to Apply

| Scenario | Apply Hejlsberg |
|----------|-----------------|
| API design decisions | Yes - simplicity and evolution |
| Choosing between language features | Yes - what's idiomatic? |
| Understanding "why C# works this way" | Yes |
| Performance optimization | Partially - correctness first |
| Interop with other languages | Partially - C# idioms may not apply |

---

## Source Material

- Channel 9/YouTube interviews with Anders Hejlsberg
- C# Language Design Notes (github.com/dotnet/csharplang)
- .NET Design Guidelines
- "Masterminds of Programming" (interview chapter)
- TypeScript design philosophy (also Hejlsberg)

---

*"Make the easy things easy, and the hard things possible."* — Anders Hejlsberg
