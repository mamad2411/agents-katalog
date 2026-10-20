---
name: dotnet-perf
description: ".NET performance patterns — allocation-free code, pooling, Span<T>, and benchmarking"
---

# Sitnik / Adams: .NET Performance

Adam Sitnik and Ben Adams' core belief: **Allocations are the enemy.** Every heap allocation is future GC work. The fastest code is the code that never allocates.

## The Foundational Principle

> "Don't measure, don't guess. Benchmark, allocate less, and let the stack do the work."

---

## Core Principles

### 1. Span<T> and Memory<T> — Zero-Copy Slicing

Span<T> is a stack-only view over contiguous memory. No allocations, no copies.

**Not this:**
```csharp
string input = "2026-03-01T14:30:00";
string datePart = input.Substring(0, 10);   // new string allocated
string timePart = input.Substring(11);       // another allocation
```

**This:**
```csharp
ReadOnlySpan<char> input = "2026-03-01T14:30:00";
ReadOnlySpan<char> datePart = input[..10];   // slice, no allocation
ReadOnlySpan<char> timePart = input[11..];   // slice, no allocation
int year = int.Parse(input[..4]);            // parse directly from span
```

**Key rules:**
- `Span<T>` is stack-only (ref struct) — cannot live on the heap, no async
- `Memory<T>` is the heap-safe sibling — use across async boundaries
- `ReadOnlySpan<T>` for safe reads — prevents accidental mutation

```csharp
// Memory<T> for async scenarios
async Task ProcessAsync(Memory<byte> buffer)
{
    int bytesRead = await stream.ReadAsync(buffer);
    Process(buffer.Span[..bytesRead]);
}
```

### 2. ArrayPool<T> and MemoryPool<T> — Rent, Don't Allocate

**Not this:**
```csharp
byte[] buffer = new byte[4096];  // GC pressure in loops
int read = stream.Read(buffer);
```

**This:**
```csharp
byte[] buffer = ArrayPool<byte>.Shared.Rent(4096);
try
{
    int read = stream.Read(buffer.AsSpan(0, 4096));
    ProcessData(buffer.AsSpan(0, read));
}
finally
{
    ArrayPool<byte>.Shared.Return(buffer);  // ALWAYS return
}
```

**Critical rules:**
- Rented arrays may be larger than requested — always track actual length
- Always return in a finally block — leaked rentals defeat the purpose
- `clearArray: true` on Return if buffer held sensitive data

```csharp
// MemoryPool<T> for IMemoryOwner with automatic disposal
using IMemoryOwner<byte> owner = MemoryPool<byte>.Shared.Rent(4096);
await stream.ReadAsync(owner.Memory[..4096]);
```

### 3. ObjectPool<T> — Pool Expensive Objects

**Not this:**
```csharp
string FormatReport(IEnumerable<Item> items)
{
    var sb = new StringBuilder();  // new allocation every call
    foreach (var item in items)
        sb.AppendLine($"{item.Name}: {item.Value}");
    return sb.ToString();
}
```

**This:**
```csharp
private static readonly ObjectPool<StringBuilder> _sbPool =
    new DefaultObjectPoolProvider().CreateStringBuilderPool();

string FormatReport(IEnumerable<Item> items)
{
    var sb = _sbPool.Get();
    try
    {
        foreach (var item in items)
            sb.AppendLine($"{item.Name}: {item.Value}");
        return sb.ToString();
    }
    finally
    {
        _sbPool.Return(sb);  // cleared and returned to pool
    }
}
```

ASP.NET DI: register `DefaultObjectPoolProvider` as singleton, then `provider.Create(new StringBuilderPooledObjectPolicy())`.

### 4. ref structs and stackalloc — Stay on the Stack

**Not this:**
```csharp
byte[] temp = new byte[128];  // heap allocation for tiny buffer
Encoding.UTF8.GetBytes(input, temp);
```

**This:**
```csharp
Span<byte> temp = stackalloc byte[128];
int written = Encoding.UTF8.GetBytes(input, temp);
ReadOnlySpan<byte> result = temp[..written];
```

**Safety pattern — fall back to pool for large inputs:**
```csharp
int maxBytes = Encoding.UTF8.GetMaxByteCount(input.Length);
byte[]? rented = null;
Span<byte> buffer = maxBytes <= 256
    ? stackalloc byte[256]
    : (rented = ArrayPool<byte>.Shared.Rent(maxBytes));
try
{
    int written = Encoding.UTF8.GetBytes(input, buffer);
    Process(buffer[..written]);
}
finally
{
    if (rented is not null)
        ArrayPool<byte>.Shared.Return(rented);
}
```

**ref struct constraints:** Cannot be boxed, captured in closures, used in async, or stored as fields in classes.

### 5. String Performance — Death by a Thousand Allocations

**Not this:**
```csharp
string result = "";
foreach (var item in items)
    result += item.Name + ", ";  // O(n^2) allocations
```

**This:**
```csharp
string result = string.Join(", ", items.Select(i => i.Name));

// string.Create for pre-sized zero-intermediate-allocation formatting
string header = string.Create(37, guid, (span, g) =>
{
    "REQUEST-".AsSpan().CopyTo(span);
    g.TryFormat(span[8..], out _, "N");
});
```

**Comparison traps:**
```csharp
// NOT THIS — culture-sensitive, slow, allocates
if (input.ToLower() == "admin") { }

// THIS — ordinal is 5-10x faster
if (input.Equals("admin", StringComparison.OrdinalIgnoreCase)) { }
```

**Frozen collections for read-only lookups (.NET 8):**
```csharp
private static readonly FrozenDictionary<string, Handler> Handlers =
    new Dictionary<string, Handler>(StringComparer.OrdinalIgnoreCase)
    {
        ["GET"] = handleGet, ["POST"] = handlePost, ["PUT"] = handlePut,
    }.ToFrozenDictionary(StringComparer.OrdinalIgnoreCase);
```

### 6. Allocation Awareness — Know Where Bytes Come From

**Boxing traps:**
```csharp
// NOT THIS — boxing int to object
void Log(object value) => Console.WriteLine(value);
Log(42);  // boxes int to heap

// THIS — generic avoids boxing
void Log<T>(T value) => Console.WriteLine(value);
Log(42);  // no boxing
```

**Closure allocations:** Lambdas that capture local variables allocate a closure object. In hot paths, use static lambdas with explicit state parameters to avoid the allocation.

**params ReadOnlySpan<T> (C# 13):**
```csharp
// NOT THIS — params allocates an array every call
void Log(params string[] messages) { }

// THIS — zero heap allocation
void Log(params ReadOnlySpan<string> messages) { }
```

**Struct vs class quick rule:**
- Struct when: small (<= 16 bytes), immutable, frequently allocated, no boxing
- Class when: large, mutable, needs inheritance, shared references

### 7. BenchmarkDotNet — Trust Numbers, Not Instincts

```csharp
[MemoryDiagnoser]  // Track allocations — the most important diagnoser
[SimpleJob(RuntimeMoniker.Net80)]
public class ParsingBenchmarks
{
    private string _input = "12345";

    [Benchmark(Baseline = true)]
    public int IntParse() => int.Parse(_input);

    [Benchmark]
    public int SpanParse() => int.Parse(_input.AsSpan());

    [Params(10, 100, 1000)]
    public int ItemCount { get; set; }

    [Benchmark]
    public string Concat()
    {
        string r = "";
        for (int i = 0; i < ItemCount; i++) r += i.ToString();
        return r;
    }

    [Benchmark]
    public string Builder()
    {
        var sb = new StringBuilder();
        for (int i = 0; i < ItemCount; i++) sb.Append(i);
        return sb.ToString();
    }
}
```

**Reading results:** Mean (avg time), Allocated (bytes/op, target 0 B), Gen0/Gen1/Gen2 (GC collections, Gen2 = bad). Always Release mode. Always `[MemoryDiagnoser]`. Run: `dotnet run -c Release -- --filter '*Benchmarks*'`

### 8. IMemoryCache — Cache Smart, Not Hard

**Not this:**
```csharp
// Cache stampede — 100 concurrent misses all fetch
if (!_cache.TryGetValue(key, out Data data))
{
    data = await _db.FetchAsync(key);
    _cache.Set(key, data, TimeSpan.FromMinutes(5));
}
```

**This:**
```csharp
private static readonly SemaphoreSlim _lock = new(1, 1);

public async Task<Data> GetDataAsync(string key)
{
    if (_cache.TryGetValue(key, out Data data))
        return data;

    await _lock.WaitAsync();
    try
    {
        if (_cache.TryGetValue(key, out data))  // double-check after lock
            return data;

        data = await _db.FetchAsync(key);
        _cache.Set(key, data, new MemoryCacheEntryOptions
        {
            AbsoluteExpirationRelativeToNow = TimeSpan.FromMinutes(5),
            SlidingExpiration = TimeSpan.FromMinutes(1),
            Size = 1
        });
        return data;
    }
    finally { _lock.Release(); }
}
```

### 9. Value Types Done Right

**Structs help when:**
```csharp
public readonly record struct Color(byte R, byte G, byte B, byte A);  // 4 bytes
public readonly record struct Vector2(float X, float Y);              // 8 bytes

// Arrays: contiguous memory, no object headers, cache-friendly
Vector2[] positions = new Vector2[10_000];  // 80 KB contiguous
// Class equivalent: 240 KB scattered across heap
```

**Structs hurt when:**
```csharp
// TOO LARGE — 40 bytes copied on every pass-by-value
public struct LargeStruct { decimal Price; decimal Quantity; DateTime Ts; }

// MUTABLE — modifies a copy, original unchanged
public struct MutablePoint { public int X, Y; }
var list = new List<MutablePoint> { new() { X = 1 } };
list[0].X = 5;  // ERROR: modifies a copy

// BOXED — defeats the purpose
IComparable c = new MyStruct();  // heap allocation
```

**The struct checklist:** <= 16 bytes? Immutable? No boxing? Frequently allocated? If any "no," use a class.

---

## Anti-Patterns

| Anti-Pattern | Why It Hurts | Fix |
|---|---|---|
| `new byte[N]` in loops | GC pressure per iteration | `ArrayPool<byte>.Shared.Rent(N)` |
| `str.ToLower() == "x"` | Allocates, culture bugs | `StringComparison.OrdinalIgnoreCase` |
| `params T[]` on hot paths | Array allocation per call | `params ReadOnlySpan<T>` (C# 13) |
| Capturing locals in lambdas | Closure object allocated | Static lambdas with state parameter |
| Large mutable structs | Expensive copies, confusing | Class or readonly record struct |
| Missing `[MemoryDiagnoser]` | Benchmarks ignore allocations | Always add to benchmark classes |
| `Dictionary` for static lookups | Mutable overhead | `FrozenDictionary` (.NET 8) |

---

## Decision Framework

```
Need temporary buffer?
├── Small + sync → stackalloc + Span<T>
├── Variable size → ArrayPool<T>.Rent/Return
└── Async boundary → MemoryPool<T> + Memory<T>

Need string work?
├── Parsing/slicing → ReadOnlySpan<char>
├── Building output → StringBuilder (pooled) or string.Create
└── Comparing → StringComparison.Ordinal[IgnoreCase]

Need object reuse?
├── Arrays → ArrayPool<T>
├── StringBuilder → ObjectPool<StringBuilder>
└── Custom expensive objects → ObjectPool<T>

Struct or class?
├── <= 16 bytes + immutable + no boxing → readonly record struct
├── Large or mutable or inherited → class
└── Unsure → class (safer default)
```

---

## Code Review Checklist

- [ ] No unnecessary allocations in hot paths? (new, concat, closures)
- [ ] ArrayPool for temporary buffers with try/finally Return?
- [ ] Span<T> for slicing instead of Substring/Array.Copy?
- [ ] stackalloc for small fixed buffers with pool fallback?
- [ ] String comparisons use Ordinal, not ToLower?
- [ ] Structs are readonly and <= 16 bytes?
- [ ] BenchmarkDotNet with [MemoryDiagnoser] validates claims?
- [ ] Cache has stampede protection (double-check + lock)?
- [ ] FrozenDictionary/FrozenSet for static lookups?
- [ ] No boxing in hot paths (generics over object)?

---

## Source Material

- Sitnik, BenchmarkDotNet creator, "High-Performance .NET" talks
- Adams, ASP.NET Core / Kestrel performance contributions
- Watson, "Writing High-Performance .NET Code" (2nd Edition)
- .NET performance documentation (docs.microsoft.com)

---

*"If you haven't measured it, you haven't optimized it — you've just guessed."* — Adam Sitnik
