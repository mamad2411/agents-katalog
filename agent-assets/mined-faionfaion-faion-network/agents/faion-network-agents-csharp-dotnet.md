# C# ASP.NET Core + Entity Framework

## Summary

**One-sentence:** Production ASP.NET Core + EF Core layout with [ApiController] + service interfaces + scoped DI + nullable refs + record DTOs + AsNoTracking reads.

**One-paragraph:** Greenfield .NET 8 backend conventions: `[ApiController]` controllers with typed route binding, `[Service]` interfaces with constructor DI, `DbContext` registered scoped, EF Core entities with `IEntityTypeConfiguration<T>`, repository interfaces only where DDD requires them, `AsNoTracking()` on read paths, `record` DTOs for transport, nullable reference types project-wide. Output: a feature folder (Controller + Service + DTO + EntityConfig + xUnit slice test) conforming to `02-output-contract.xml`.

**Ефективно для:**

- Enterprise backends on Microsoft stack (Azure, AD, SQL Server).
- High-throughput APIs needing async + minimal allocation.
- Domain-rich apps where strong static typing prevents bugs.
- Long-running services (`BackgroundService`) and gRPC microservices.
- Teams with Roslyn analyzers + nullable-refs already enforced.

## Applies If (ALL must hold)

- Greenfield or refactored ASP.NET Core 6+ project.
- EF Core (any provider) is the persistence layer.
- xUnit (not MSTest / NUnit) is the test framework.
- DI lifetimes (singleton/scoped/transient) are understood across the team.

## Skip If (ANY kills it)

- Tiny scripts or one-off cron — Python/Node ship in fewer lines.
- Frontend BFFs in TypeScript-first orgs — tRPC/Hono wins type-sharing.
- Edge runtimes with sub-50ms cold start — AOT not yet mature enough.
- Greenfield startups where senior C# hiring is a real constraint.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Feature spec | Markdown | ticket / SDD task |
| Existing solution layout | .sln + csproj | repo |
| DB schema or entity sketch | C# class or ERD | team |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[csharp-entity-framework]] | EF Core patterns this feature consumes. |
| [[csharp-xunit-testing]] | Test conventions for the slice test. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: apicontroller-required, scoped-dbcontext, nullable-refs-on, record-dtos, asnotracking-reads | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for feature folder + valid/invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: anaemic-controller, tracking-leaks, dto-as-entity, missing-cancellationtoken | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure: classify → entity+config → service → controller → test | ~700 |
| `content/06-decision-tree.xml` | essential | Routing tree on stack/runtime → rule | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `design-feature-folder` | sonnet | Layered judgment on naming + boundaries. |
| `write-controller-service` | sonnet | C# scaffolding within the 5 rules. |
| `write-xunit-slice-test` | haiku | Mechanical AAA test against the controller. |

## Templates

| File | Purpose |
|------|---------|
| `templates/FeatureController.cs` | `[ApiController]` skeleton with typed routes |
| `templates/FeatureService.cs` | Service + DI skeleton |
| `templates/EntityConfiguration.cs` | `IEntityTypeConfiguration<T>` skeleton |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-csharp-dotnet.py` | Validate feature-folder spec against schema | Pre-commit on spec artefact |

## Related

- [[csharp-entity-framework]]
- [[csharp-background-services]]
- [[csharp-xunit-testing]]
- parent skill: `pro/dev/software-developer/`

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (runtime constraints, stack, async needs) to a rule from `01-core-rules.xml`, either approving the ASP.NET Core feature layout or redirecting to a smaller stack (script, edge function, BFF). Use it whenever starting a new .NET feature folder or porting from Web Forms / .NET Framework.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/FeatureController.cs`

```csharp
using Microsoft.AspNetCore.Mvc;

namespace Faion.Features.Orders;

[ApiController]
[Route("api/[controller]")]
public sealed class OrdersController : ControllerBase
{
    private readonly IOrdersService _service;

    public OrdersController(IOrdersService service) => _service = service;

    [HttpGet("{id:int}")]
    [ProducesResponseType(typeof(OrderResponse), StatusCodes.Status200OK)]
    [ProducesResponseType(StatusCodes.Status404NotFound)]
    public async Task<ActionResult<OrderResponse>> Get(int id, CancellationToken ct)
    {
        var order = await _service.GetAsync(id, ct);
        return order is null ? NotFound() : Ok(order);
    }

    [HttpPost]
    [ProducesResponseType(typeof(OrderResponse), StatusCodes.Status201Created)]
    public async Task<ActionResult<OrderResponse>> Create(CreateOrderRequest req, CancellationToken ct)
    {
        var created = await _service.CreateAsync(req, ct);
        return CreatedAtAction(nameof(Get), new { id = created.Id }, created);
    }
}

public sealed record CreateOrderRequest(string CustomerName, decimal Total);
public sealed record OrderResponse(int Id, string CustomerName, decimal Total);
```

### `templates/FeatureService.cs`

```csharp
using Microsoft.EntityFrameworkCore;

namespace Faion.Features.Orders;

public interface IOrdersService
{
    Task<OrderResponse?> GetAsync(int id, CancellationToken ct);
    Task<OrderResponse> CreateAsync(CreateOrderRequest req, CancellationToken ct);
}

public sealed class OrdersService : IOrdersService
{
    private readonly AppDbContext _db;

    public OrdersService(AppDbContext db) => _db = db;

    public Task<OrderResponse?> GetAsync(int id, CancellationToken ct) =>
        _db.Orders
            .AsNoTracking()
            .Where(o => o.Id == id)
            .Select(o => new OrderResponse(o.Id, o.CustomerName, o.Total))
            .FirstOrDefaultAsync(ct);

    public async Task<OrderResponse> CreateAsync(CreateOrderRequest req, CancellationToken ct)
    {
        var order = new Order(req.CustomerName, req.Total);
        _db.Orders.Add(order);
        await _db.SaveChangesAsync(ct);
        return new OrderResponse(order.Id, order.CustomerName, order.Total);
    }
}

public sealed class Order
{
    public int Id { get; private set; }
    public string CustomerName { get; private set; } = "";
    public decimal Total { get; private set; }
    private Order() { }
    public Order(string customerName, decimal total)
    {
        CustomerName = customerName;
        Total = total;
    }
}

public sealed class AppDbContext : DbContext
{
    public DbSet<Order> Orders => Set<Order>();
    public AppDbContext(DbContextOptions<AppDbContext> opt) : base(opt) { }
}
```

### `templates/EntityConfiguration.cs`

```csharp
using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;

namespace Faion.Features.Orders;

public sealed class OrderConfiguration : IEntityTypeConfiguration<Order>
{
    public void Configure(EntityTypeBuilder<Order> builder)
    {
        builder.ToTable("orders");
        builder.HasKey(o => o.Id);
        builder.Property(o => o.CustomerName).IsRequired().HasMaxLength(200);
        builder.Property(o => o.Total).HasPrecision(18, 2);
        builder.HasIndex(o => o.CustomerName);
    }
}
```
