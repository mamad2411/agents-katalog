---
name: dotnet-efcore-query-perf
description: >
  Improve EF Core query performance: AsNoTracking, projections (Select), N+1 splits,
  Include/ThenInclude discipline, compiled queries, indexes alignment, and logging
  slow SQL. Use when EF Core slow queries, N+1, tracking overhead, cartesian explosion,
  AsSplitQuery, or owned .NET app data access tuning.
---

# .NET EF Core Query Perf

## Scope And Authorization

- **In scope:** .NET applications and databases you own; prefer staging with production-like data.
- **Out of scope:** Untested index drops on production primaries without approval.
- Capture SQL carefully—redact PII in logs.
- Pair with `code-quality-standards`, indexing/DBA skills, and API performance practices.

## When To Use

- High SQL counts or duration in APM for EF-powered endpoints.
- Tracking overhead on large read-only lists.
- `Include` causes cartesian explosion.
- Need compiled queries for hot paths.
- Reviewing LINQ that translates poorly.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| General .NET security | .NET security skills |
| IL decompile of third-party | `dotnet-il-decompile` |
| Migrations safety | `database-migration-safety` |
| Caching layer design | `caching-strategies` |
| Code quality baseline | `code-quality-standards` |

## High-impact techniques

| Technique | Use when |
| --- | --- |
| `AsNoTracking()` | Read-only queries |
| `Select` projection | Need few columns/DTOs |
| `AsSplitQuery()` | Multiple collection Includes |
| Filtered `Include` | Only subset of children |
| Compiled query | Hot path same shape |
| Raw SQL / views | EF translation poor (careful) |
| Proper indexes | Filters/sorts/joins |

## Workflow

### 1. Confirm scope and success criteria

1. Endpoints, EF version, provider (SQL Server/Postgres/etc.).
2. Success: fewer queries/ms; stable plans; tests for query counts where useful.
3. Baseline metrics from APM or `ToQueryString` + DB stats.

### 2. Measure

```csharp
// Log SQL (dev/staging)
optionsBuilder
    .LogTo(Console.WriteLine, LogLevel.Information)
    .EnableSensitiveDataLogging(); // never in prod logs
```

```csharp
var sql = query.ToQueryString();
```

1. Count round-trips; identify N+1 (lazy loads if enabled).
2. Prefer lazy loading **off** in web apps to avoid surprise N+1.

### 3. Fix N+1 and Includes

```csharp
// BAD: loop with lazy load
var blogs = await db.Blogs.ToListAsync();
foreach (var b in blogs) { _ = b.Posts.Count; }

// GOOD: explicit include or projection
var blogs = await db.Blogs
    .AsNoTracking()
    .Include(b => b.Posts)
    .AsSplitQuery()
    .ToListAsync();

// OFTEN BETTER: project
var dto = await db.Blogs
    .AsNoTracking()
    .Select(b => new BlogDto(
        b.Id,
        b.Title,
        b.Posts.Count))
    .ToListAsync();
```

1. Multiple collection Includes → consider `AsSplitQuery()` to avoid cartesian product.
2. Filtered include: `.Include(b => b.Posts.Where(p => p.Published))`.

### 4. Tracking and identity resolution

1. Read APIs: `AsNoTracking()` or `AsNoTrackingWithIdentityResolution()` when graphs needed without update.
2. Avoid tracking thousands of entities for a list view.
3. For updates: load minimal set; attach carefully.

### 5. Compiled queries and pagination

```csharp
private static readonly Func<AppDbContext, int, IAsyncEnumerable<BlogDto>> HotQuery =
    EF.CompileAsyncQuery((AppDbContext db, int take) =>
        db.Blogs.AsNoTracking()
            .OrderBy(b => b.Id)
            .Select(b => new BlogDto(b.Id, b.Title, 0))
            .Take(take));
```

1. Always paginate public lists (`Skip/Take` or keyset).
2. Ensure `ORDER BY` stable for pagination.

### 6. SQL translation pitfalls

| LINQ smell | Risk |
| --- | --- |
| Client eval methods | Unexpected in-memory filter |
| `ToList` mid-chain | Pulls too much |
| `string.Format` in expression | May not translate |
| Huge `Contains` lists | Parameter limits |

1. Review EF warnings for client evaluation.
2. Align indexes with `Where`/`OrderBy` columns.

### 7. Verify and hand off

```bash
dotnet test
# Compare APM SQL duration before/after
```

1. Regression tests with known fixture counts optional.
2. Document repository query patterns for the team.
3. Apply `code-quality-standards`.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Reads | NoTracking + project | Track full graph for JSON |
| Collections | SplitQuery or project | Triple Include cartesian |
| Lazy load | Disabled | On in web by default |
| Lists | Paginated | Unbounded ToList |
| Secrets | No sensitive SQL logs prod | EnableSensitiveDataLogging prod |
| Indexes | Match filters | Hope optimizer |

## Output Checklist

- [ ] Slow queries baselined
- [ ] N+1 eliminated or justified
- [ ] AsNoTracking on read paths
- [ ] Projections used where suitable
- [ ] SplitQuery considered for multi-include
- [ ] Pagination on lists
- [ ] Indexes reviewed
- [ ] Hot paths consider compiled queries
- [ ] APM shows improvement
- [ ] Guidelines shared with team

## Rules

- Measure SQL round-trips and duration—not only C# microbenchmarks.
- Prefer projections over fat entity graphs for APIs.
- Never leave sensitive data logging on in production.
- Owned apps only.
- Focus on EF Core query performance patterns.
