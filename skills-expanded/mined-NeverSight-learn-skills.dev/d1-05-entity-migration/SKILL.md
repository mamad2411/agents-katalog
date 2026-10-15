---
name: d1-05-entity-migration
description: "Creates an EF Core entity + runs the migration that creates its table in Postgres. CRUD drill Day 1 step 5. Trigger: 'day1 step5', 'create entity/table for up-api'. Use the entity name and columns exactly as user specifies — do not suggest or add columns."
compatibility: ".NET 10 SDK, dotnet-ef; up-api DbContext + db connection must already work."
---

# Day 1 · Step 5 — Entity + migration (no redeploy)

**Before starting:** Ask for:
1. **Entity name** (PascalCase, e.g., `Product`, `Order`, `User`) — REQUIRED
2. **Columns** (format: `ColumnName:Type`, comma-separated, e.g., `Name:string, Price:decimal, Stock:int`) — REQUIRED
3. **Nullable columns** (optional, default: all non-string/Id are non-nullable) — OPTIONAL

Use exactly as specified. Do not suggest, add, or modify columns.

`up-api/Entities/<Entity>.cs`:
```csharp
public class <Entity>
{
    public int Id { get; set; }
    // one property per given column, e.g.:
    // public string Name { get; set; } = string.Empty;
    // public decimal Price { get; set; }
}
```

Add to `AppDbContext`:
```csharp
public DbSet<<Entity>> <Entity>s => Set<<Entity>>();
```

```Run bash
cd up-api
dotnet ef migrations add Init<Entity>
dotnet ef database update
```

This runs against the already-running Postgres container via the `localhost:5432` connection string from
the db-config step — no redeploy needed. Verify the table exists (`\dt` in `psql`, or a quick
`docker exec` into the db container).
