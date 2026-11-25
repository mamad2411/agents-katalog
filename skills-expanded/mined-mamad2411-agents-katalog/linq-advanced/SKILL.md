---
name: linq-advanced
description: "Advanced LINQ patterns, pitfalls, and EF Core integration"
---

# Skeet/Meijer: LINQ Mastery

Jon Skeet's LINQ guidance: **Understand what LINQ compiles to, and deferred execution stops being mysterious.** Erik Meijer's design insight: **LINQ is monadic composition for C# developers who don't need to know that.**

## The Foundational Principle

> "The query doesn't run until you ask for results. Every time you ask, it runs again."

Deferred execution is LINQ's greatest strength and its most common trap.

---

## Core Principles

### 1. IQueryable<T> vs IEnumerable<T>

`IEnumerable<T>` uses delegates. `IQueryable<T>` uses expression trees. This determines where code runs.

**Not this:**
```csharp
IEnumerable<Order> orders = context.Orders;  // Cast away IQueryable
var big = orders.Where(o => o.Total > 1000); // Filters client-side on every row
```

**This:**
```csharp
IQueryable<Order> orders = context.Orders;
var big = orders.Where(o => o.Total > 1000); // SQL: WHERE Total > 1000
```

**The EF Core trap:**
```csharp
// EF Core 3+ throws on untranslatable expressions
context.Orders.Where(o => MyCustomMethod(o.Total)); // Throws

// Fix: materialize first, then apply client logic
var orders = await context.Orders.Where(o => o.Total > 1000).ToListAsync();
var filtered = orders.Where(o => MyCustomMethod(o.Total)); // Client-side, fine
```

**Rule:** Keep `IQueryable<T>` until you need client logic, then materialize and switch to `IEnumerable<T>`.

### 2. Deferred vs Immediate Execution

**Deferred:** Where, Select, SelectMany, OrderBy, Skip, Take, GroupBy, Join, Distinct
**Immediate:** ToList, ToArray, ToDictionary, Count, First, Any, Sum, Aggregate

```csharp
// BAD: Multiple enumeration -- source read twice
var source = GetExpensiveStream();
Console.WriteLine(source.Count());  // Enumerates
Console.WriteLine(source.First());  // Enumerates again

// GOOD: Materialize once
var list = source.ToList();
Console.WriteLine(list.Count);      // Property
Console.WriteLine(list[0]);         // Index
```

**Stale-query surprise:**
```csharp
var list = new List<int> { 1, 2, 3 };
var query = list.Where(x => x > 1); // Deferred
list.Add(4);
// query now yields 2, 3, 4 -- it sees the mutation
```

### 3. SelectMany -- Flattening Nested Collections

**Not this:**
```csharp
var allTags = new List<string>();
foreach (var post in posts)
    foreach (var tag in post.Tags)
        allTags.Add(tag);
```

**This:**
```csharp
var allTags = posts.SelectMany(p => p.Tags);

// With parent context
var tagged = posts.SelectMany(
    p => p.Tags,
    (post, tag) => new { post.Title, Tag = tag });

// Query syntax: multiple from clauses
var tagged = from post in posts
             from tag in post.Tags
             select new { post.Title, Tag = tag };
```

### 4. GroupBy and Projection

Always project groups to aggregates -- raw `IGrouping` is rarely what you want.

**Not this:**
```csharp
foreach (var g in orders.GroupBy(o => o.CustomerId))
{
    var total = 0m;
    foreach (var o in g) total += o.Total;
}
```

**This:**
```csharp
var summary = orders
    .GroupBy(o => o.CustomerId)
    .Select(g => new {
        CustomerId = g.Key, Count = g.Count(),
        Total = g.Sum(o => o.Total), Last = g.Max(o => o.Date)
    });
```

**EF Core -- keep GroupBy translatable:**
```csharp
// Translates to SQL GROUP BY
await context.Orders.GroupBy(o => o.CustomerId)
    .Select(g => new { g.Key, Total = g.Sum(o => o.Total) })
    .ToListAsync();

// Won't translate -- g.ToList() is not SQL
.Select(g => new { g.Key, Orders = g.ToList() }) // Throws
```

### 5. Custom Iterators with yield

`yield return` builds a lazy state machine. Values produced one at a time, on demand.

```csharp
IEnumerable<string> ReadLines(string path)
{
    using var reader = new StreamReader(path);
    string? line;
    while ((line = reader.ReadLine()) is not null)
        yield return line;
}
// Compose: only reads until 10 matches found
var longLines = ReadLines("huge.log").Where(l => l.Length > 200).Take(10);
```

**Caveat -- argument validation is deferred too:**
```csharp
// BAD: null check deferred until iteration
IEnumerable<T> Filter<T>(IEnumerable<T> src, Func<T, bool> pred)
{
    if (src is null) throw new ArgumentNullException(nameof(src));
    foreach (var item in src) if (pred(item)) yield return item;
}

// GOOD: Validate eagerly, iterate lazily
IEnumerable<T> Filter<T>(IEnumerable<T> src, Func<T, bool> pred)
{
    ArgumentNullException.ThrowIfNull(src);
    ArgumentNullException.ThrowIfNull(pred);
    return Inner(src, pred);
    static IEnumerable<T> Inner(IEnumerable<T> s, Func<T, bool> p)
    {
        foreach (var item in s) if (p(item)) yield return item;
    }
}
```

### 6. Query Syntax vs Method Syntax

**Query syntax wins for joins and let:**
```csharp
var result = from o in orders
             join c in customers on o.CustomerId equals c.Id
             let name = c.First + " " + c.Last
             where o.Total > 100
             orderby o.Date descending
             select new { name, o.Total, o.Date };
```

**Method syntax wins for simple chains:**
```csharp
var top = products.Where(p => p.InStock)
    .OrderByDescending(p => p.Sales).Take(10).Select(p => p.Name);
// Operators only in method syntax: Any, First, Distinct, Chunk
```

### 7. Aggregate and Reduce Patterns

```csharp
// Custom accumulation -- running balance
var balances = transactions.Aggregate(
    new List<decimal>(),
    (acc, tx) => { acc.Add((acc.Count > 0 ? acc[^1] : 0m) + tx.Amount); return acc; });

// Zip for parallel iteration
var results = names.Zip(scores, (n, s) => new { n, s });
// C# 12: names.Zip(scores) returns tuples
```

### 8. LINQ to Entities Gotchas

**Translatable:** comparisons, arithmetic, string.Contains/StartsWith, null checks, aggregates.

**Not translatable:**
```csharp
.Where(o => MyHelper.IsValid(o))           // Custom methods
.Select(o => new Order(o.Id, o.Total))     // Parameterized constructors
```

**Raw SQL escape hatch:**
```csharp
var orders = await context.Orders
    .FromSqlInterpolated($"SELECT * FROM Orders WHERE Total > {min}")
    .Where(o => o.Date > cutoff)  // Can chain LINQ after raw SQL
    .ToListAsync();
```

### 9. Performance

**Avoid LINQ in hot paths:**
```csharp
// BAD: closure + iterator allocation per iteration, O(n) scan
for (int i = 0; i < 1_000_000; i++)
    if (items.Any(x => x.Id == targetId)) Process(i);

// GOOD: pre-compute
var idSet = items.Select(x => x.Id).ToHashSet();
for (int i = 0; i < 1_000_000; i++)
    if (idSet.Contains(targetId)) Process(i);
```

**ToHashSet for repeated lookups:**
```csharp
// BAD: O(n*m) -- List.Contains is O(n)
var ids = GetValidIds().ToList();
var filtered = orders.Where(o => ids.Contains(o.Id));

// GOOD: O(n) -- HashSet.Contains is O(1)
var ids = GetValidIds().ToHashSet();
var filtered = orders.Where(o => ids.Contains(o.Id));
```

**Pre-computed joins:**
```csharp
// BAD: O(n) First() per order
orders.Select(o => new { o, C = customers.First(c => c.Id == o.CustomerId) });

// GOOD: O(1) dictionary lookup
var map = customers.ToDictionary(c => c.Id);
orders.Select(o => new { o, C = map[o.CustomerId] });
```

---

## Anti-Patterns

| Anti-Pattern | Problem | Fix |
|---|---|---|
| Multiple enumeration | Re-executes query, data may change | Materialize with ToList/ToArray |
| IQueryable cast to IEnumerable | Forces client-side evaluation | Keep as IQueryable until final step |
| LINQ in tight loops | Closure + iterator allocs per iteration | Pre-compute lookups, manual loops |
| GroupBy().First() for dedup | Loads all groups for one element | DistinctBy or dictionary |
| OrderBy before Where | Sorts then discards rows | Filter first, sort after |
| Nested Contains on List | O(n*m) quadratic scan | ToHashSet for inner collection |

---

## Decision Framework

| Situation | Choice |
|---|---|
| Querying a database | IQueryable -- server does the work |
| In-memory data | IEnumerable -- delegates are simpler |
| Result used more than once | Materialize with ToList/ToArray |
| Flatten nested collections | SelectMany |
| Join two sequences by key | Join (query syntax) or ToDictionary |
| Custom accumulation | Aggregate |
| Repeated key lookups | ToDictionary or ToHashSet first |
| Hot path (>10k iter/sec) | Manual loop -- skip LINQ overhead |

---

## Code Review Checklist

1. **IQueryable stays IQueryable?** No accidental cast to IEnumerable before database query executes.
2. **Single enumeration?** Deferred queries not iterated multiple times.
3. **Materialization intentional?** Every ToList/ToArray is deliberate, not defensive.
4. **EF Core translatable?** No custom methods inside IQueryable pipelines.
5. **No LINQ in hot loops?** Pre-computed lookups where iteration count is high.
6. **GroupBy projected?** Groups reduced to aggregates, not iterated raw.
7. **SelectMany over nested foreach?** Flattening done declaratively.
8. **Correct syntax?** Query syntax for joins/let, method syntax for simple chains.
9. **Closures acceptable?** No unexpected allocations in performance-critical code.

---

## Source Material

- "C# in Depth" (4th Edition, Manning, 2019) -- Jon Skeet
- "Functional Programming in C#" (Manning, 2017) -- Enrico Buonanno
- Erik Meijer's LINQ design papers and Channel 9 lectures
- EF Core documentation on client vs server evaluation

---

*"LINQ is not magic. It's a pipeline of functions composed through extension methods. Once you see that, you control it."* -- Jon Skeet
