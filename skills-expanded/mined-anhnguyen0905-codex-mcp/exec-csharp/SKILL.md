---
name: exec-csharp
description: C#/.NET execution idioms to embed into Codex prompts when the target project is C# — nullable reference types, async correctness, and .NET conventions.
---

# C# / .NET Idioms (embed when project is C#)

```
C#/.NET standards:
- Nullable reference types: honor the project's <Nullable> setting; no ! null-forgiving to silence
  warnings — narrow or guard instead. Validate args with ArgumentNullException.ThrowIfNull at boundaries.
- Async: async all the way — no .Result/.Wait()/.GetAwaiter().GetResult() (deadlock risk); pass and
  honor CancellationToken through call chains; ConfigureAwait(false) in library code; return Task,
  never async void except event handlers.
- Errors: throw specific exceptions with context; catch the narrowest type you can handle; never
  swallow; use try/finally or using/await using for IDisposable/IAsyncDisposable resources.
- Immutability: prefer records and init-only setters for DTOs; expose IReadOnlyList/IReadOnlyDictionary,
  not mutable collections; readonly fields where possible.
- Idioms: LINQ over manual loops when clearer; pattern matching and switch expressions; string
  interpolation over concatenation; var when the type is obvious. Dispose enumerators/streams.
- DI & config: constructor injection via the built-in container; bind config with IOptions<T>; no
  service-locator or static state for dependencies. Follow the project's layering.
- Follow .editorconfig / analyzers already configured; match namespace and folder structure.
- Tests: the repo's framework (xUnit/NUnit/MSTest) + assertion lib (FluentAssertions if present);
  Arrange-Act-Assert; descriptive Method_Scenario_Expected names consistent with existing tests.
```
