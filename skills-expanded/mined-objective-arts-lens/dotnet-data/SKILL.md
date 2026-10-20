---
name: dotnet-data
description: "EF Core and .NET data access patterns"
---

# Lerman: Data Access Done Right

Julie Lerman's core belief: **EF Core is powerful, but only if you understand what SQL it generates.** The ORM is a tool, not a magic wand. Know when it helps, know when it gets in the way, and always check the query plan.

## The Foundational Principle

> "Just because the ORM can do it doesn't mean it should."

EF Core gives you productivity. Dapper gives you control. The best .NET code knows when to use each.

---

## Core Principles

### 1. DbContext as Unit of Work

DbContext is short-lived. One per request, one per operation. Never share across threads.

**Not this:**
```csharp
// WRONG: Singleton DbContext shared across requests
public class OrderService
{
    private static readonly AppDbContext _db = new();  // Shared, not thread-safe

    public Order GetOrder(int id) => _db.Orders.Find(id);
}
```

**This:**
```csharp
// RIGHT: Scoped lifetime via DI
builder.Services.AddDbContext<AppDbContext>(options =>
    options.UseSqlServer(connectionString));

public class OrderService
{
    private readonly AppDbContext _db;

    public OrderService(AppDbContext db) => _db = db;

    public async Task<Order?> GetOrderAsync(int id)
        => await _db.Orders.FindAsync(id);
}
```

**Why scoped:** A long-lived context accumulates stale tracked entities, leaks memory, and corrupts concurrent operations. One request = one context = one unit of work.

### 2. AsNoTracking for Read-Only Queries

If you are not going to modify the entities, tell EF Core. The performance difference is massive on large result sets.

**Not this:**
```csharp
// WRONG: Tracking every entity just to display a list
var orders = await _db.Orders
    .Where(o => o.Status == "Active")
    .ToListAsync();  // Change tracker watches every entity
```

**This:**
```csharp
// RIGHT: No tracking overhead for read-only data
var orders = await _db.Orders
    .AsNoTracking()
    .Where(o => o.Status == "Active")
    .ToListAsync();

// Or set it at the context level for read-heavy services
public class ReportingDbContext : AppDbContext
{
    public ReportingDbContext(DbContextOptions<ReportingDbContext> options)
        : base(options)
    {
        ChangeTracker.QueryTrackingBehavior = QueryTrackingBehavior.NoTracking;
    }
}
```

**Impact:** AsNoTracking can cut query time 40-60% on large result sets. The change tracker creates identity map entries, snapshot copies, and relationship fixup for every tracked entity.

### 3. N+1 Problem

The silent performance killer. One query per navigation property, per row.

**Not this:**
```csharp
// N+1: 1 query for orders + N queries for customers
var orders = await _db.Orders.ToListAsync();
foreach (var order in orders)
{
    Console.WriteLine(order.Customer.Name);  // SELECT per order!
}
```

**This:**
```csharp
// Eager loading: 1 or 2 queries total
var orders = await _db.Orders
    .Include(o => o.Customer)
    .Include(o => o.OrderItems)
        .ThenInclude(oi => oi.Product)
    .Where(o => o.Status == "Active")
    .ToListAsync();

// Split queries when Include produces cartesian explosion
var orders = await _db.Orders
    .Include(o => o.OrderItems)
    .Include(o => o.Shipments)
    .AsSplitQuery()  // Separate SQL per Include instead of one giant JOIN
    .ToListAsync();
```

**Detecting N+1:** Enable sensitive logging in development to see every query:
```csharp
options.UseSqlServer(connectionString)
    .LogTo(Console.WriteLine, LogLevel.Information)
    .EnableSensitiveDataLogging();  // Dev only -- shows parameter values
```

### 4. Projections with Select

Loading entire entities to use three fields wastes memory, bandwidth, and CPU cycles.

**Not this:**
```csharp
// WRONG: Loads entire entity graph just for a dropdown
var customers = await _db.Customers
    .Include(c => c.Address)
    .ToListAsync();

return customers.Select(c => new { c.Id, c.Name, c.Address.City });
```

**This:**
```csharp
// RIGHT: Only the columns you need, translated to efficient SQL
var customers = await _db.Customers
    .Select(c => new CustomerDropdownDto
    {
        Id = c.Id,
        Name = c.Name,
        City = c.Address.City  // EF Core generates the JOIN for you
    })
    .ToListAsync();
// SQL: SELECT c.Id, c.Name, a.City FROM Customers c JOIN Addresses a ...
```

**Rule:** If the UI needs 3 fields, the query should return 3 columns. Projections also sidestep N+1.

### 5. Migrations

Code-first migrations keep your schema versioned alongside your code.

```csharp
// Create a migration after changing your model
// CLI: dotnet ef migrations add AddOrderShippingDate

public partial class AddOrderShippingDate : Migration
{
    protected override void Up(MigrationBuilder migrationBuilder)
    {
        migrationBuilder.AddColumn<DateTime>(
            name: "ShippedAt",
            table: "Orders",
            type: "datetime2",
            nullable: true);

        migrationBuilder.CreateIndex(
            name: "IX_Orders_ShippedAt",
            table: "Orders",
            column: "ShippedAt");
    }

    protected override void Down(MigrationBuilder migrationBuilder)
    {
        migrationBuilder.DropIndex("IX_Orders_ShippedAt", "Orders");
        migrationBuilder.DropColumn("ShippedAt", "Orders");
    }
}
```

**Production:** Generate idempotent SQL scripts, never run `Database.Migrate()` in production:
```bash
dotnet ef migrations script --idempotent -o migrate.sql
```

**Data seeding in OnModelCreating:**
```csharp
modelBuilder.Entity<OrderStatus>().HasData(
    new OrderStatus { Id = 1, Name = "Pending" },
    new OrderStatus { Id = 2, Name = "Shipped" },
    new OrderStatus { Id = 3, Name = "Delivered" }
);
```

### 6. Raw SQL Fallback

When the ORM generates bad SQL or you need database-specific features, drop to raw SQL.

**Not this:**
```csharp
// WRONG: String concatenation = SQL injection
var sql = $"SELECT * FROM Orders WHERE Status = '{status}'";
var orders = _db.Orders.FromSqlRaw(sql).ToList();
```

**This:**
```csharp
// RIGHT: FromSqlInterpolated parameterizes automatically
var orders = await _db.Orders
    .FromSqlInterpolated(
        $"SELECT * FROM Orders WHERE Status = {status} AND Total > {minTotal}")
    .Include(o => o.Customer)  // Can still chain LINQ on top
    .OrderBy(o => o.CreatedAt)
    .ToListAsync();

// DML operations
await _db.Database.ExecuteSqlInterpolatedAsync(
    $"UPDATE Orders SET Status = {newStatus} WHERE Id = {orderId}");
```

### 7. Repository Pattern Debate

DbContext already implements Repository + Unit of Work. Adding another layer often adds complexity without value.

**When the extra layer hurts:** Generic `IRepository<T>` with `GetById`/`GetAll`/`Add`/`Remove` just wraps DbContext with a narrower API. Complex queries leak IQueryable or require dozens of specialized methods.

**When it helps -- domain-specific query objects:**
```csharp
public class OrderRepository
{
    private readonly AppDbContext _db;
    public OrderRepository(AppDbContext db) => _db = db;

    public async Task<List<Order>> GetShippableOrdersAsync()
        => await _db.Orders
            .AsNoTracking()
            .Include(o => o.OrderItems)
            .Where(o => o.Status == "Paid" && o.OrderItems.Any())
            .OrderBy(o => o.CreatedAt)
            .ToListAsync();
}
```

**The rule:** If your repository is just CRUD wrappers, delete it. If it encapsulates reused domain queries, keep it.

### 8. Connection Management

Connection pooling, retry policies, and proper configuration prevent outages under load.

```csharp
builder.Services.AddDbContext<AppDbContext>(options =>
    options.UseSqlServer(connectionString, sqlOptions =>
    {
        // Retry transient failures (network blips, Azure SQL throttling)
        sqlOptions.EnableRetryOnFailure(
            maxRetryCount: 3,
            maxRetryDelay: TimeSpan.FromSeconds(5),
            errorNumbersToAdd: null);

        // Command timeout for long-running queries
        sqlOptions.CommandTimeout(30);
    }));
```

**Not this:**
```csharp
// WRONG: Opening manual connections alongside EF Core
using var conn = new SqlConnection(connectionString);
await conn.OpenAsync();  // Bypasses pooling configuration
```

**This:**
```csharp
// RIGHT: Reuse the DbContext connection for raw ADO.NET
var conn = _db.Database.GetDbConnection();
await conn.OpenAsync();
using var cmd = conn.CreateCommand();
cmd.CommandText = "SELECT @@VERSION";
var version = await cmd.ExecuteScalarAsync();
```

### 9. Dapper as Alternative

Dapper is a micro-ORM: raw SQL + object mapping. No change tracking, no overhead. Use it for read-heavy paths where EF Core's abstraction costs too much.

**Dapper for complex reads:**
```csharp
using var conn = new SqlConnection(connectionString);

var report = await conn.QueryAsync<SalesReport>("""
    SELECT r.Region, SUM(o.Total) AS Revenue, COUNT(*) AS OrderCount,
           RANK() OVER (ORDER BY SUM(o.Total) DESC) AS Rank
    FROM Orders o JOIN Regions r ON o.RegionId = r.Id
    WHERE o.CreatedAt >= @Since
    GROUP BY r.Region
    """, new { Since = startDate });
```

**EF Core for writes:**
```csharp
var order = await _db.Orders.Include(o => o.OrderItems)
    .FirstAsync(o => o.Id == orderId);

order.Status = "Shipped";
order.ShippedAt = DateTime.UtcNow;
await _db.SaveChangesAsync();  // Change tracking handles the UPDATE
```

**Side-by-side registration:**
```csharp
builder.Services.AddDbContext<AppDbContext>(o => o.UseSqlServer(cs));
builder.Services.AddScoped<IDbConnection>(_ => new SqlConnection(cs));
// Write path: EF Core. Read path: Dapper.
```

### 10. IQueryable vs IEnumerable

IQueryable builds expression trees that translate to SQL. IEnumerable runs in memory. Mixing them up pulls your entire table into the application.

**Not this:**
```csharp
// WRONG: AsEnumerable forces client-side evaluation -- loads ALL rows
public IEnumerable<Order> GetActiveOrders()
    => _db.Orders.AsEnumerable().Where(o => o.Status == "Active");

// WRONG: Custom methods break IQueryable translation
public IQueryable<Order> GetOrders()
    => _db.Orders.Where(o => MyCustomMethod(o.Status));  // Throws at runtime
```

**This:**
```csharp
// RIGHT: Filter stays as IQueryable, translated to SQL WHERE clause
public IQueryable<Order> GetActiveOrders()
    => _db.Orders.Where(o => o.Status == "Active");

// Caller composes further before materializing
var result = await orderRepo.GetActiveOrders()
    .Where(o => o.Total > 100)
    .OrderByDescending(o => o.CreatedAt)
    .Take(20)
    .ToListAsync();  // Single SQL: WHERE + ORDER BY + TOP
```

**Safety net:** EF Core 5+ throws by default when a LINQ expression cannot be translated to SQL. Never downgrade this to a warning.

---

## Anti-Patterns

| Anti-Pattern | Problem | Fix |
|---|---|---|
| Singleton DbContext | Thread-unsafe, stale data, memory leak | Scoped lifetime via DI |
| Tracking read-only data | Wasted CPU and memory on change tracker | AsNoTracking() |
| Lazy loading in loops | N+1 queries, one per row per navigation | Include/ThenInclude or projection |
| Loading entities for DTOs | Fetching 50 columns to use 3 | Select projection |
| `Database.Migrate()` in prod | Schema changes during app startup = outage | Idempotent SQL scripts |
| String concat in FromSqlRaw | SQL injection | FromSqlInterpolated or parameterized |
| Generic `IRepository<T>` | Leaky abstraction, forces narrow query API | Domain-specific repositories or direct DbContext |
| No retry policy | Transient failures crash the app | EnableRetryOnFailure |
| `.AsEnumerable()` before `.Where()` | Pulls entire table into memory | Keep as IQueryable |
| Ignoring generated SQL | ORM writes bad queries silently | LogTo + EXPLAIN in dev |

---

## Decision Framework

| Situation | Approach |
|---|---|
| CRUD with relationships | EF Core with change tracking |
| Read-only list or grid | EF Core + AsNoTracking + projection |
| Complex reporting query | Dapper with hand-written SQL |
| Bulk insert (10k+ rows) | EF Core Bulk Extensions or SqlBulkCopy |
| Need database-specific SQL | FromSqlInterpolated with LINQ composition |
| Performance-critical hot path | Dapper or compiled EF Core queries |
| Schema evolution | Code-first migrations, idempotent scripts |

---

## Code Review Checklist

Before merging .NET data access code, verify:

1. **DbContext lifetime?** Scoped, never singleton or static.
2. **AsNoTracking?** Applied to every query that does not modify data.
3. **N+1 checked?** Include used for needed navigations, or projection avoids them.
4. **Projection used?** Select returns only needed columns, not full entities for display.
5. **IQueryable preserved?** Filtering and sorting happen server-side, not after AsEnumerable.
6. **SQL injection safe?** FromSqlInterpolated or parameterized, never string concatenation.
7. **Retry policy configured?** EnableRetryOnFailure set for cloud databases.
8. **Migration is reversible?** Both Up and Down methods implemented.
9. **Generated SQL reviewed?** LogTo or SQL Profiler confirms efficient queries in dev.
10. **Right tool chosen?** EF Core for writes and simple reads, Dapper for complex reports.

---

## Source Material

- "Programming Entity Framework" / "EF Core in Action" (Julie Lerman, Jon P Smith)
- Entity Framework Core documentation (Microsoft)
- Dapper (Marc Gravell, Stack Overflow)

---

*"Profile your queries. The ORM writes the SQL, but you own the performance."* -- Julie Lerman
