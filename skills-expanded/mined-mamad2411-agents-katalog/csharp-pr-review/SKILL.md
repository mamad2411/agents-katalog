---
name: csharp-pr-review
description: 'Perform a structured PR review for C# and Blazor codebases. Produces categorized findings (Critical / Warning / Suggestion) covering naming, null safety, async correctness, DI lifetimes, EF Core patterns, Blazor-specific issues, and test coverage.'
---

# C# / Blazor PR Review

Your goal is to perform a thorough, structured code review of C# and Blazor pull request changes.

## Inputs

| Input | Required | Description |
|-------|----------|-------------|
| Changed files | Yes | The diff or file contents of the PR |
| PR description | No | Context about what the PR intends to change |
| Target framework | No | Defaults to assuming .NET 8+ |

## Output Format

Produce findings grouped by severity. For each finding, include:
1. **File + line reference**
2. **Code snippet** (the problematic code, quoted)
3. **Explanation** of the issue
4. **Corrected example** where applicable

```
## 🔴 Critical
### [filename.cs:line] Issue title
> code snippet
Explanation...
✅ Fix: corrected code

## 🟡 Warning
...

## 🔵 Suggestion
...

---
## Summary
- 🔴 Critical: N
- 🟡 Warning: N
- 🔵 Suggestion: N

**Merge recommendation**: [BLOCK / APPROVE WITH WARNINGS / APPROVE]
```

## Review Checklist

### Naming Conventions

- Public types, methods, properties: `PascalCase`
- Private fields: `_camelCase`
- Local variables and parameters: `camelCase`
- Interfaces: `I`-prefix (`IMyService`)
- Async methods: `-Async` suffix
- Constants: `PascalCase` (not `ALL_CAPS`)

### Null Safety

- Nullable reference types (`<Nullable>enable</Nullable>`) must be respected
- Null-forgiving operator (`!`) flagged as Warning unless clearly justified
- Null checks before dereferencing non-nullable expressions
- `ArgumentNullException.ThrowIfNull(param)` preferred over manual null checks in .NET 6+

### Async / Await

- 🔴 **Critical**: `async void` outside event handlers
- 🔴 **Critical**: `.Wait()`, `.Result`, `.GetAwaiter().GetResult()` in async paths (deadlock risk)
- 🟡 **Warning**: Missing `CancellationToken` parameter on public async methods
- 🟡 **Warning**: `Task.Run(() => SyncWork())` without clear justification
- 🔵 **Suggestion**: Library code should use `ConfigureAwait(false)`
- 🔵 **Suggestion**: Use `Task.WhenAll()` for concurrent independent awaits

### Blazor Render Modes

- 🔴 **Critical**: `@onclick` or other interactive event handlers on components without an interactive render mode
- 🟡 **Warning**: `@rendermode InteractiveServer` on a page that doesn't need interactivity (prefer Static SSR)
- 🟡 **Warning**: Missing `@rendermode` causing unexpected SSR behavior on a component expected to be interactive

### Blazor Component Correctness

- 🔴 **Critical**: Component subscribes to events / `NavigationManager.LocationChanged` without `IDisposable`/`IAsyncDisposable`
- 🟡 **Warning**: `[Parameter]` property mutated directly inside the component
- 🟡 **Warning**: `StateHasChanged()` called in a loop or on every keystroke
- 🟡 **Warning**: `Action<T>` used instead of `EventCallback<T>` for component events
- 🔵 **Suggestion**: Missing `@key` on `@foreach` rendered components
- 🔵 **Suggestion**: Large inline `@code` blocks — suggest extracting to code-behind

### Dependency Injection

- 🔴 **Critical**: Scoped service captured in a Singleton service (state corruption)
- 🔴 **Critical**: `IServiceProvider.GetService<T>()` used inside a component or business service (service locator anti-pattern)
- 🟡 **Warning**: `HttpClient` injected directly instead of via `IHttpClientFactory`
- 🔵 **Suggestion**: Constructor injection preferred over `[Inject]` property injection for testability in non-Blazor classes

### EF Core

- 🔴 **Critical**: String interpolation in `FromSqlRaw` / `ExecuteSqlRaw` (SQL injection)
- 🟡 **Warning**: Navigation properties accessed inside `foreach` without `Include()` (N+1 query)
- 🟡 **Warning**: Missing `AsNoTracking()` on read-only queries in high-traffic paths
- 🟡 **Warning**: `DbContext` injected as Singleton (must be Scoped)
- 🔵 **Suggestion**: Consider `AsSplitQuery()` for queries with multiple `Include()` chains

### Exception Handling

- 🔴 **Critical**: `catch (Exception)` that swallows the exception without logging
- 🟡 **Warning**: `try/catch` in a loop catching a predictable failure on every iteration
- 🔵 **Suggestion**: Use specific exception types instead of catching `Exception`

### Test Coverage

- 🟡 **Warning**: New public business logic method has no corresponding unit test
- 🟡 **Warning**: Test names don't follow `MethodName_StateUnderTest_ExpectedBehavior` convention
- 🔵 **Suggestion**: Magic literal values in tests — extract to named constants

## Workflow

1. Read all changed files completely before writing any finding
2. Apply the checklist systematically to each changed file
3. Don't flag issues in unchanged context lines
4. Group all findings by severity tier
5. Write the summary and merge recommendation last
