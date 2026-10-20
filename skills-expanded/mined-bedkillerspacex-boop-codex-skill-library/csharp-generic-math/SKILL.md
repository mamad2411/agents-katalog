---
name: csharp-generic-math
description: >
  Use .NET generic math (INumber<T>, IAdditionOperators, IBinaryInteger, etc.)
  for reusable numeric algorithms in owned C# codebases on modern TFMs. Use when
  writing type-parameterized math utilities, SIMD-friendly abstractions, or
  replacing duplicated int/double overloads with INumber-constrained generics.
---

# C# Generic Math

## Scope And Authorization

- **In scope:** C# projects targeting frameworks that support generic math (typically .NET 7+).
- **Out of scope:** Changing cryptographic primitives “via generic math”; financial ledger rules without domain review.
- Prefer clear numerical stability notes for algorithms (overflow, NaN, division by zero).
- Pair with `csharp-style-conventions` and `code-quality-standards`.

## When To Use

- Libraries that must run on `int`, `long`, `double`, `decimal`, or custom numeric types.
- Replacing copy-pasted `Sum(int[])` / `Sum(double[])` helpers.
- Constraining generics with `INumber<T>`, `IFloatingPoint<T>`, `IBinaryInteger<T>`.
- Parsing/formatting via `ISpanParsable<T>` / `IFormattable` patterns in generic code.
- Evaluating whether generic math is worth complexity vs concrete types.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Channels/pipelines | `csharp-channels-pipelines` |
| Minimal API security | `csharp-minimal-apis-security` |
| Style only | `csharp-style-conventions` |
| Crypto correctness | dedicated crypto skills |
| Implementation quality baseline | `code-quality-standards` |

## Key interfaces (selection)

| Interface | Role |
| --- | --- |
| `INumber<TSelf>` | Core arithmetic + comparisons |
| `INumberBase<TSelf>` | Base constants, parsing helpers |
| `IAdditionOperators<TSelf,TOther,TResult>` | `+` |
| `IBinaryInteger<TSelf>` | Integer bit ops, shifts |
| `IFloatingPoint<TSelf>` | IEEE-like float ops |
| `IMinMaxValue<TSelf>` | `MinValue` / `MaxValue` |
| `IParsable<TSelf>` / `ISpanParsable<TSelf>` | Parse |

## Workflow

### 1. Confirm scope and success criteria

1. TFM (`net8.0`…), numeric types required, performance budget.
2. Success: one algorithm implementation; tests across types; overflow policy explicit.

### 2. Check TFM and language version

```xml
<TargetFramework>net8.0</TargetFramework>
<LangVersion>latest</LangVersion>
```

```bash
dotnet --version
dotnet build
```

### 3. Write constrained APIs

```csharp
using System.Numerics;

public static class Stats
{
    public static T Sum<T>(ReadOnlySpan<T> values)
        where T : INumber<T>
    {
        T sum = T.Zero;
        foreach (var v in values)
            sum += v;
        return sum;
    }

    public static T Clamp<T>(T value, T min, T max)
        where T : INumber<T>
    {
        if (value < min) return min;
        if (value > max) return max;
        return value;
    }

    public static T AverageInteger<T>(ReadOnlySpan<T> values)
        where T : IBinaryInteger<T>
    {
        if (values.Length == 0)
            throw new ArgumentException("empty", nameof(values));
        return Sum(values) / T.CreateChecked(values.Length);
    }
}
```

### 4. Creation, overflow, and floating rules

| API | Use |
| --- | --- |
| `T.CreateChecked(x)` | Throws on overflow/unrepresentable |
| `T.CreateSaturating(x)` | Clamps |
| `T.CreateTruncating(x)` | Truncates bits |
| `T.Zero` / `T.One` | Constants |

1. Integers: define checked vs unchecked context intentionally.
2. Floats: handle `NaN` / infinity in comparisons (`IFloatingPoint` helpers).
3. `decimal` for currency-like values when generic over `INumber` includes it — still know domain rules.

### 5. When not to abstract

1. Hot inner loops may specialize for `float`/`Vector<T>` after profiling.
2. Algorithms that only make sense for IEEE floats should constrain `IFloatingPointIeee754<T>`.
3. Public API surface: sometimes dual concrete + generic overloads ease usability.

### 6. Tests

```csharp
[Theory]
[InlineData(1, 2, 3)]
public void Sum_Int(int a, int b, int expected)
    => Assert.Equal(expected, Stats.Sum<int>(new[] { a, b }.AsSpan()) /* adjust */);

[Fact]
public void Sum_Double()
    => Assert.Equal(3.5, Stats.Sum<double>(new[] { 1.0, 2.5 }), precision: 5);
```

Cover empty sequences, negatives, and overflow paths for integers.

### 7. Verify

```bash
dotnet test
# Optional: BenchmarkDotNet comparing generic vs concrete
```

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Constraints | Tightest interface that fits | Unconstrained `T` with dynamic |
| Overflow | `CreateChecked` where safety matters | Silent wrap in finance |
| API | Generic helpers + tests | Generic everything including UI glue |
| Perf | Measure before micro-optimizing | Assume generic always slower/faster |
| Currency | Explicit decimal policy | Blind `INumber` money math |

## Output Checklist

- [ ] TFM supports generic math
- [ ] Interfaces chosen per method
- [ ] Zero/One/Create* usage reviewed
- [ ] Overflow/NaN policy documented
- [ ] Tests for multiple `T`
- [ ] Perf note if on hot path
- [ ] Public API usability considered
- [ ] Style + code quality applied
- [ ] Residual numeric risks noted
- [ ] No crypto misuse

## Rules

- Generic math is for reusable algorithms — not a substitute for domain validation.
- Be explicit about overflow and floating error.
- Focus on **.NET generic math interfaces** in C#.
