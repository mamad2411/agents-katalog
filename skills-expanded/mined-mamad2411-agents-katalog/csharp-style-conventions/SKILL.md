---
name: csharp-style-conventions
description: >
  Apply C# and .NET naming conventions, file layout, XML documentation, nullable
  reference types, and EditorConfig/analyzer alignment when writing or reviewing
  C# code. Use for style consistency on owned .NET projects — does not replace
  code-quality-standards for reliability and security.
---

# C# Style Conventions

## Scope And Authorization

- **In scope:** C# / .NET repositories you maintain.
- **Out of scope:** Rewriting third-party code style without ownership; using style debates to block security fixes.
- Prefer repo-local `.editorconfig` and Directory.Build.props as source of truth when present.
- Pair always with `code-quality-standards` for non-style concerns.

## When To Use

- New C# code, refactors, or PR review comments on naming/layout.
- Enabling nullable reference types and cleaning warnings.
- Aligning with Microsoft .NET naming guidelines and team EditorConfig.
- Adding XML docs on public APIs.
- Choosing `async` suffix, interface `I` prefix, and file-scoped namespaces.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Security of Minimal APIs | `csharp-minimal-apis-security` |
| Reliability / testing depth | `code-quality-standards` |
| Language feature how-to (channels, required) | feature-specific csharp skills |
| Commit messages | `commit-message-conventions` |
| API user docs broadly | `api-documentation-writing` |

## Convention tables

### Naming

| Symbol | Convention | Example |
| --- | --- | --- |
| Types, methods, props | PascalCase | `OrderService`, `GetTotal` |
| Interfaces | `I` + PascalCase | `IOrderRepository` |
| Locals, parameters | camelCase | `orderId` |
| Private fields | `_camelCase` or team rule | `_clock` |
| Constants | PascalCase | `DefaultTimeout` |
| Async methods | `Async` suffix when returning awaitable | `LoadAsync` |

### Layout

| Topic | Prefer |
| --- | --- |
| Namespaces | File-scoped `namespace X;` when TFM allows and repo agrees |
| Usings | Outside namespace; remove unused; IDE organize |
| One type per file | Generally; exceptions for small nested helpers |
| Braces | Allman or K&R per EditorConfig — **do not mix** |
| var | When type obvious; explicit when it aids reading |

### Nullable

| Practice | Notes |
| --- | --- |
| `<Nullable>enable</Nullable>` | Project-wide |
| Annotate public APIs | `string?` vs `string` |
| Avoid `!` bang | Except localized proven cases |
| Guard arguments | `ArgumentNullException.ThrowIfNull` |

## Workflow

### 1. Read repo truth

```bash
# Prefer existing config
ls .editorconfig Directory.Build.props *.sln 2>$null
dotnet format style --verify-no-changes || true
```

If EditorConfig exists, **do not** invent conflicting rules.

### 2. Apply naming and structure on touch points

1. Rename only with IDE renames (not text replace) for public APIs.
2. Keep public API renames intentional and versioned.
3. Match neighboring files in the same folder.

### 3. XML documentation (public surface)

```csharp
/// <summary>
/// Loads an order by id for the current tenant.
/// </summary>
/// <param name="orderId">Stable order identifier.</param>
/// <returns>The order, or null if not found.</returns>
public Task<Order?> GetAsync(string orderId, CancellationToken ct = default)
```

Use `<remarks>`, `<exception>`, and `cref` where they help public consumers. Avoid noise docs on trivial private methods.

### 4. Nullable cleanup workflow

```bash
dotnet build -warnaserror:nullable 2>$null || dotnet build
```

1. Fix real null flows first.
2. Use `is null` patterns / pattern matching.
3. Record residual `#nullable disable` with reason (prefer none).

### 5. Analyzers

```xml
<!-- Directory.Build.props sketch -->
<PropertyGroup>
  <Nullable>enable</Nullable>
  <ImplicitUsings>enable</ImplicitUsings>
  <TreatWarningsAsErrors>true</TreatWarningsAsErrors>
  <!-- enforce gradually if legacy -->
</PropertyGroup>
```

Enable StyleCop.Analyzers / meziantou / Roslynator only as team agrees; fix or suppress with justification.

### 6. PR review style comments

Use `code-review-comments-style`: prefer actionable, repo-rule-linked nits; do not bike-shed within allowed EditorConfig variance.

### 7. Verify

```bash
dotnet format
dotnet build
dotnet test
```

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Naming | `TryParse` / `Async` consistent | `get_order_data_async` in C# APIs |
| Nullable | Enabled + fixed warnings | Ignore CS8602 floods |
| Docs | Public contracts documented | Essay on private setters |
| Format | `dotnet format` CI | Personal Visual Studio only settings |
| Scope | Style on touched code | 5k-file reformat mixed with feature |

## Output Checklist

- [ ] Repo EditorConfig / analyzers read
- [ ] Naming matches guidelines and neighbors
- [ ] File-scoped namespaces policy followed
- [ ] Nullable enable status known; warnings addressed on changes
- [ ] Public API XML docs when required by team
- [ ] `dotnet format` / build clean for change set
- [ ] No drive-by mass reformat without agreement
- [ ] Security/reliability not neglected (hand off to code-quality)
- [ ] Suppressions justified
- [ ] Residual debt listed if legacy

## Rules

- Style serves readability; repo config wins over personal taste.
- This skill does **not** replace `code-quality-standards`.
- Focus on **C# / .NET style conventions**.
