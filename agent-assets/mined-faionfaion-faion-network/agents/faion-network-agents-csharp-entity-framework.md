# Entity Framework Patterns

## Summary

**One-sentence:** EF Core 8 patterns — fluent `IEntityTypeConfiguration`, `AsNoTracking` reads, `AsSplitQuery` on multi-collection includes, repository paged results, and ordered migrations.

**One-paragraph:** EF Core misuse — data annotations on entities, lazy-loading proxies, `IQueryable` returned from repositories, Cartesian explosions from multi-Include — produces the classic "EF Core is slow" complaint. This methodology pins five rules: entities are POCOs with private setters initialized in constructors; mapping lives in `IEntityTypeConfiguration<T>` via fluent API; read paths use `.AsNoTracking()` + DTO projection; multi-collection queries use `.AsSplitQuery()`; migrations are append-only and named with verbs. Output: entity + configuration + repository + migration scaffold per `02-output-contract.xml`.

**Ефективно для:**

- Production EF Core 8 apps with non-trivial domain.
- Read paths under throughput pressure (AsNoTracking + projection).
- Multi-collection queries causing Cartesian explosion.
- Repositories that must hide `IQueryable` from upper layers.
- Teams co-versioning migrations with entity changes.

## Applies If (ALL must hold)

- EF Core 6+ (Code-First) inside an ASP.NET Core or worker project.
- Migrations are the schema-of-record (not a hand-maintained SQL script).
- The team agrees DTOs separate from entities for transport.
- Read/write paths can be distinguished at the repository boundary.

## Skip If (ANY kills it)

- Database-First / `EDMX` legacy project — start with a migration plan first.
- Dapper / micro-ORM is already in place and adequate.
- Trivial CRUD with single-table reads — overhead exceeds benefit.
- Stored-procedure-heavy enterprise app — EF Core sits on top of SP-only contract.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Entity sketch | C# class or ERD | team |
| DbContext + connection | existing csproj | repo |
| Migration history | `Migrations/` folder | repo |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[csharp-dotnet]] | ASP.NET Core layout that wires EF in. |
| [[ddd-repositories]] | Repository pattern abstracting EF behind a domain interface. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: fluent-config-only, asnotracking-reads, no-iqueryable-return, splitquery-multi-include, append-only-migrations | ~1200 |
| `content/02-output-contract.xml` | essential | JSON Schema for entity+config+repo+migration spec | ~900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: cartesian-explosion, tracking-on-reads, lazy-loading-proxies, edited-migration | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure | ~700 |
| `content/06-decision-tree.xml` | essential | Routing tree on workload + Include shape → rule | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `design-entity-and-config` | sonnet | Layered judgment on relationships + indexes. |
| `write-repository-paged` | sonnet | Paged read scaffolding. |
| `audit-existing-queries` | sonnet | Look for AsNoTracking + Include violations. |

## Templates

| File | Purpose |
|------|---------|
| `templates/Entity.cs` | POCO entity with private setters |
| `templates/EntityConfiguration.cs` | Fluent mapping skeleton |
| `templates/Repository.cs` | Repository with PagedResult + AsNoTracking |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-csharp-entity-framework.py` | Validate entity+config+repo spec against schema | Pre-commit on spec artefact |

## Related

- [[csharp-dotnet]]
- [[ddd-repositories]]
- [[csharp-dotnet-patterns]]
- parent skill: `pro/dev/software-developer/`

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (workload — read-heavy vs write-heavy, Include shape) to a rule from `01-core-rules.xml`, either approving the EF Core pattern or routing to Dapper / raw SQL. Use it whenever adding a new entity, a new query, or refactoring a slow page.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/Entity.cs`

```csharp
using System.Collections.Generic;

namespace Faion.Domain.Orders;

public sealed class Order
{
    private readonly List<OrderItem> _items = new();

    public int Id { get; private set; }
    public string CustomerName { get; private set; } = "";
    public decimal Total { get; private set; }
    public IReadOnlyCollection<OrderItem> Items => _items.AsReadOnly();

    private Order() { }

    public Order(string customerName)
    {
        if (string.IsNullOrWhiteSpace(customerName))
            throw new ArgumentException("customer name required", nameof(customerName));
        CustomerName = customerName;
    }

    public void AddItem(OrderItem item)
    {
        _items.Add(item);
        Total += item.Price * item.Quantity;
    }
}

public sealed class OrderItem
{
    public int Id { get; private set; }
    public string Sku { get; private set; } = "";
    public decimal Price { get; private set; }
    public int Quantity { get; private set; }
    private OrderItem() { }
    public OrderItem(string sku, decimal price, int quantity)
    {
        Sku = sku; Price = price; Quantity = quantity;
    }
}
```

### `templates/EntityConfiguration.cs`

```csharp
using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;

namespace Faion.Infrastructure.Orders;

public sealed class OrderConfiguration : IEntityTypeConfiguration<Order>
{
    public void Configure(EntityTypeBuilder<Order> builder)
    {
        builder.ToTable("orders");
        builder.HasKey(o => o.Id);
        builder.Property(o => o.CustomerName).IsRequired().HasMaxLength(200);
        builder.Property(o => o.Total).HasPrecision(18, 2).HasDefaultValueSql("0");
        builder.HasIndex(o => o.CustomerName);
        builder.HasMany(o => o.Items)
            .WithOne()
            .HasForeignKey("OrderId")
            .OnDelete(DeleteBehavior.Cascade);
    }
}

public sealed class OrderItemConfiguration : IEntityTypeConfiguration<OrderItem>
{
    public void Configure(EntityTypeBuilder<OrderItem> builder)
    {
        builder.ToTable("order_items");
        builder.HasKey(i => i.Id);
        builder.Property(i => i.Sku).IsRequired().HasMaxLength(64);
        builder.Property(i => i.Price).HasPrecision(18, 2);
        builder.HasIndex(i => i.Sku);
    }
}
```

### `templates/Repository.cs`

```csharp
using Microsoft.EntityFrameworkCore;

namespace Faion.Infrastructure.Orders;

public sealed record OrderDto(int Id, string CustomerName, decimal Total);
public sealed record PagedResult<T>(IReadOnlyList<T> Items, int TotalCount, int Page, int PageSize);

public interface IOrderRepository
{
    Task<PagedResult<OrderDto>> ListAsync(int page, int pageSize, CancellationToken ct);
    Task<Order?> GetAsync(int id, CancellationToken ct);
    Task AddAsync(Order order, CancellationToken ct);
    Task SaveChangesAsync(CancellationToken ct);
}

public sealed class OrderRepository : IOrderRepository
{
    private readonly AppDbContext _db;

    public OrderRepository(AppDbContext db) => _db = db;

    public async Task<PagedResult<OrderDto>> ListAsync(int page, int pageSize, CancellationToken ct)
    {
        var query = _db.Orders
            .AsNoTracking()
            .Include(o => o.Items)
            .AsSplitQuery();

        var total = await query.CountAsync(ct);
        var items = await query
            .OrderBy(o => o.Id)
            .Skip((page - 1) * pageSize)
            .Take(pageSize)
            .Select(o => new OrderDto(o.Id, o.CustomerName, o.Total))
            .ToListAsync(ct);

        return new PagedResult<OrderDto>(items, total, page, pageSize);
    }

    public Task<Order?> GetAsync(int id, CancellationToken ct) =>
        _db.Orders.Include(o => o.Items).FirstOrDefaultAsync(o => o.Id == id, ct);

    public async Task AddAsync(Order order, CancellationToken ct)
    {
        await _db.Orders.AddAsync(order, ct);
    }

    public Task SaveChangesAsync(CancellationToken ct) => _db.SaveChangesAsync(ct).ContinueWith(_ => { }, ct);
}

public sealed class AppDbContext : DbContext
{
    public DbSet<Order> Orders => Set<Order>();
    public DbSet<OrderItem> OrderItems => Set<OrderItem>();
    public AppDbContext(DbContextOptions<AppDbContext> opt) : base(opt) { }
    protected override void OnModelCreating(ModelBuilder modelBuilder) =>
        modelBuilder.ApplyConfigurationsFromAssembly(typeof(AppDbContext).Assembly);
}
```
